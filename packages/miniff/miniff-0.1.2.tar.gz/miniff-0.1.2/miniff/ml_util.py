from numericalunits import aBohr, angstrom, Ry, eV
import torch
from itertools import chain
from functools import partial, wraps
from collections import namedtuple, Counter
from string import ascii_lowercase
import numpy as np
from scipy.optimize import root_scalar
import logging
from pathlib import Path
import json
import matplotlib
from matplotlib import pyplot

from .potentials import behler2_descriptor_family, lj_potential_family,\
    harmonic_repulsion_potential_family, behler_turning_point, behler4_descriptor_family
from .ml import fw_cauldron, fw_cauldron_charges, Dataset, Normalization, SequentialSoleEnergyNN,\
    potentials_from_ml_data, learn_cauldron
from .kernel import NeighborWrapper, Cell
from .util import dict_reduce, serialize_nu, load_nu
from .presentation import plot_convergence, plot_diagonal


def prepare_dataset(n, box_size, potentials=None, species=1, size=3, seed=None, min_distance=angstrom):
    """
    Prepares a set of random structures interacting through the specified potential.
    
    Parameters
    ----------
    n : int
        Sample count.
    box_size : float
        The size of the box.
    potentials : tuple, list
        Interaction potentials.
    species : int, list, tuple
        Species' names.
    size : int
        Species per sample.
    seed
        Random seed.
    min_distance : float
        Minimal distance between points.

    Returns
    -------
    cells : list
        Generated structures.
    """
    if isinstance(species, int):
        species = ascii_lowercase[:species]
    species = np.array(species)
    if species.ndim == 0:
        species = species[np.newaxis]

    def _all_pairs(_p):
        _result = []
        for _i_s1, _s1 in enumerate(species):
            for _s2 in species[_i_s1:]:
                _result.append(_p.copy(tag=f"{_s1}-{_s2}"))
        return _result

    if potentials is None:
        potentials = _all_pairs(lj_potential_family(epsilon=Ry, sigma=angstrom, a=6))
        potentials_cutoff = max(i.cutoff for i in potentials)

    if min_distance:
        relax_potentials = _all_pairs(harmonic_repulsion_potential_family(a=min_distance, epsilon=Ry))
        relax_potentials_cutoff = max(i.cutoff for i in relax_potentials)

    if seed is not None:
        np.random.seed(seed)

    coordinates = np.random.rand(n, size, 3)
    values = np.random.choice(species, (n, size))

    cells = []
    for c, v in zip(coordinates, values):
        c = Cell(np.eye(3) * box_size, c, v)
        w = NeighborWrapper(c, x=(1, 1, 1))
        if min_distance:
            w.compute_distances(relax_potentials_cutoff)
            c = w.relax(relax_potentials, normalize=False)
            w = NeighborWrapper(c, x=(1, 1, 1), normalize=False)
        w.compute_distances(potentials_cutoff)
        w.meta["total-energy"] = w.total(potentials)
        w.meta["forces"] = - w.grad(potentials)
        w.meta["classic-potentials"] = potentials
        cells.append(w)

    return cells


def default_behler_descriptors(arg, n, a, left=1, common_eta=True):
    """
    Default Behler descriptor choice.
    
    Parameters
    ----------
    arg : dict, list, tuple
        A dict with minimal distance between atoms
        per specimen pair or wrapped cells to deduce
        these distances from.
    n : int
        Descriptor count.
    a : float
        The function cutoff.
    left : float
        Left boundary factor.
    common_eta : bool
        Pick common etas.

    Returns
    -------
    descriptors : dict
        A dict with descriptors.
    """
    def _eta_for_tp(_tp):
        if _tp > a / 2:
            raise ValueError(f"The turning point requested {_tp} is more than half-way to the cutoff {a}")

        def _target(_x):
            return behler_turning_point(a, _x, 0) - _tp

        bracket = 0, 10000 / a ** 2

        return root_scalar(_target, bracket=bracket, method='bisect').root

    if not isinstance(arg, dict):
        arg = dict_reduce((
            w.pair_reduction_function(lambda x: x.min() if len(x) > 0 else None)
            for w in arg
        ), min)

    etas = {}
    for k, d in arg.items():
        d *= left
        if d > a / 2:
            raise ValueError(f"The minimal interatomic distance {d} for entity {k} "
                             f"is more than half-way to the cutoff {a}")
        etas[k] = _etas = []
        for tp in np.linspace(d, a / 2, n):
            _etas.append(_eta_for_tp(tp))

    if common_eta:
        _etas = np.mean(list(etas.values()), axis=0)
        etas = {k: _etas for k in etas}

    descriptors_raw = {
        k: list(behler2_descriptor_family(a=a, eta=eta, r_sphere=0, tag=k) for eta in v)
        for k, v in etas.items()
    }

    all_species = sorted(set(sum((i.split("-") for i in descriptors_raw), [])))

    descriptors = {}
    for i_s1, s1 in enumerate(all_species):
        for s2 in all_species[i_s1:]:
            tags = f"{s1}-{s2}", f"{s2}-{s1}"

            d = None
            for sp in tags:
                if sp in descriptors_raw:
                    d = descriptors_raw.pop(sp)

            if d is not None:
                if s1 not in descriptors:
                    descriptors[s1] = []
                descriptors[s1] += list(i.copy(tag=tags[0]) for i in d)

                if s1 != s2:
                    if s2 not in descriptors:
                        descriptors[s2] = []
                    descriptors[s2] += list(i.copy(tag=tags[1]) for i in d)
    return descriptors


def default_behler_descriptors_3(arg, a):
    """
    Default Behler descriptor choice.

    Parameters
    ----------
    arg : dict, list
        A dict with minimal distance between atoms
        per specimen pair or wrapped cells to deduce
        these distances from.
    a : float
        The function cutoff.

    Returns
    -------
    descriptors : dict
        A dict with descriptors.
    """
    if len(arg) == 0:
        raise ValueError("Empty input")
    if not isinstance(arg[0], str):
        _species = set()
        for i in arg:
            _species |= set(i.values)
        arg = _species

    arg = sorted(arg)
    descriptors = {k: [] for k in arg}
    for p1 in arg:
        for zeta in 1, 2, 4, 16:
            for l in 1, -1:
                for i, p2 in enumerate(arg):
                    for p3 in arg[i:]:
                        descriptors[p1].append(behler4_descriptor_family(eta=0, l=l, zeta=zeta, a=a,
                                                                        tag=f"{p1}-{p2}-{p3}"))
    return descriptors


def parse_runner_input(f):
    """
    Parses RuNNer input file for atomic descriptors.
    
    Parameters
    ----------
    f : str, file
        File or file name to parse.
        
    Returns
    -------
    result : list
        A list of descriptors.
    """
    result = []
    if isinstance(f, str):
        f = open(f, 'r')

    for line in f:
        line = line.strip()
        if line.startswith("#"):
            pass
        elif line.startswith("symfunction_short"):
            params = line.split()[1:]
            descriptor_id = params[1]

            if descriptor_id == '2':
                a1, descriptor_id, a2, eta, r_sphere, a = params[:6]
                eta, r_sphere, a = map(float, (eta, r_sphere, a))
                result.append(behler2_descriptor_family(
                    eta=eta / aBohr ** 2,
                    r_sphere=r_sphere * aBohr,
                    a=a * aBohr,
                    tag=f"{a1}-{a2}",
                ))

            elif descriptor_id == '3':
                a1, descriptor_id, a2, a3, eta, l, zeta, a = params[:8]
                eta, l, zeta, a = map(float, (eta, l, zeta, a))
                result.append(behler4_descriptor_family(
                    eta=eta / aBohr ** 2,
                    l=l,
                    zeta=zeta,
                    a=a * aBohr,
                    tag=f"{a1}-{a2}-{a3}",
                ))  # By fact, descriptor_id == '3' means fourth Behler function from the paper

            else:
                raise ValueError(f"Unknown descriptor {repr(descriptor_id)}")
        else:
            raise ValueError(f"Cannot parse '{line}'")

    return result


def parse_lammps_input(f):
    """
    Parse LAMMPS input for NN potential.

    Parameters
    ----------
    f : file
        Text file to parse.

    Returns
    -------
    result : dict
        A dict of potentials.
    """
    behler2_parameter_order = "a", "eta", "r_sphere"
    behler4_parameter_order = "a", "eta", "zeta", "l"

    def _array(_x, dtype=float):
        return np.array(tuple(map(dtype, _x)))

    descriptors = {}
    scales = {}
    layers = {}

    lines = iter(f)
    for line in lines:
        if line.startswith("POT"):
            _, element, _ = line.split()
            descriptors[element] = []
            scales[element] = []
            layers[element] = []
            _id, n_descriptors = next(lines).split()
            assert _id == "SYM"
            n_descriptors = int(n_descriptors)
            for i in range(n_descriptors):
                parameters_all = next(lines).split()
                parameters = _array(parameters_all[:5])
                parameters[1] *= angstrom
                parameters[2] /= angstrom ** 2
                elements = parameters_all[5:]
                if parameters[0] == 2:
                    parameters[3] *= angstrom
                    parameters = dict(zip(behler2_parameter_order, parameters[1:]))
                    descriptors[element].append(behler2_descriptor_family(
                        **parameters, tag="-".join([element] + list(elements))
                    ))
                elif parameters[0] == 4:
                    parameters = dict(zip(behler4_parameter_order, parameters[1:]))
                    if elements[0] == elements[1]:
                        parameters["epsilon"] = 0.5  # No double-counting
                    descriptors[element].append(behler4_descriptor_family(
                        **parameters, tag="-".join([element] + list(elements))
                    ))
                else:
                    raise NotImplementedError(f"Unknown descriptor {parameters[0]}")

            for block in "scale1", "scale2":
                _id, *parameters = next(lines).split()
                assert _id == block
                assert len(parameters) == n_descriptors
                scales[element].append(_array(parameters))

            _id, n_layers, *net_shape = next(lines).split()
            assert _id == "NET"
            n_layers = int(n_layers)
            net_shape = _array(net_shape, dtype=int)
            assert net_shape[n_layers] == 1
            net_shape = net_shape[:n_layers + 1]

            input_dims = n_descriptors
            for i, output_dims in enumerate(net_shape):
                _id, _ix, kind = next(lines).split()
                assert _id == "LAYER"
                assert float(_ix) == i

                weights = []
                bias = []
                for j in range(output_dims):
                    _id, *x = next(lines).split()
                    assert _id == f"w{j:d}"
                    weights.append(_array(x))

                    _id, b = next(lines).split()
                    assert _id == f"b{j:d}"
                    bias.append(float(b))

                linear = torch.nn.Linear(input_dims, output_dims, bias=True)
                linear.weight = torch.nn.Parameter(torch.tensor(np.array(weights)))
                linear.bias = torch.nn.Parameter(torch.tensor(np.array(bias)))
                layers[element].append(linear)

                if kind == "sigmoid":
                    layers[element].append(torch.nn.Sigmoid())
                elif kind == "linear":
                    pass
                else:
                    raise NotImplementedError(f"Unknown layer: {kind}")

                input_dims = int(output_dims)

    nn = []
    for _, _layers in sorted(layers.items()):
        nn.append(SequentialSoleEnergyNN(_layers))

    normalization = Normalization(
        energy_scale=torch.tensor(np.array(eV)),
        features_scale=[torch.tensor(v[1]) for _, v in sorted(scales.items())],
        energy_offsets=torch.tensor(np.zeros((len(scales), 1), dtype=float)),
        features_offsets=[torch.tensor(v[0]) for _, v in sorted(scales.items())],
    )
    return potentials_from_ml_data(nn=nn, descriptors=descriptors, normalization=normalization)


loss_result = namedtuple("stats_tuple", ("loss_id", "loss_value", "reference", "prediction", "components"))


def energy_loss(networks, data, criterion, w_energy, w_gradients, energies_p=False):
    """
    Energy loss function.

    Parameters
    ----------
    networks : list
        A list of networks to learn.
    data : Dataset
        The dataset to compute loss function of.
    criterion : torch.nn.Module
        Loss criterion, defaults to MSE.
    w_energy : float
        Energy weight in the loss function.
    w_gradients : float
        Gradients weight in the loss function.
    energies_p : bool
        If True, compares partial energies.

    Returns
    -------
    result : loss_result
        The resulting loss and accompanying information.
    """
    result = fw_cauldron(networks, data, grad=w_gradients != 0, energies_p=energies_p)
    if w_gradients != 0:
        e, g = result
    else:
        e = result
        g = None

    if energies_p:
        energy_loss_results = []
        de = 0
        for e_, data_ in zip(e, data.per_point_datasets):
            de_ = criterion(e_ * data_.mask.unsqueeze(2), data_.energies_p)
            de += de_
            energy_loss_results.append(loss_result(
                loss_id=f"partial energy {data_.tag}",
                loss_value=de_,
                reference=data_.energies_p,
                prediction=e_,
                components=None,
            ))

        energy_loss_result = loss_result(
            loss_id="energy",
            loss_value=de,
            reference=None,
            prediction=None,
            components=tuple(energy_loss_results),
        )
    else:
        de = criterion(e, data.per_cell_dataset.energy)

        energy_loss_result = loss_result(
            loss_id="energy",
            loss_value=de,
            reference=data.per_cell_dataset.energy,
            prediction=e,
            components=None,
        )

    if w_gradients == 0:
        return energy_loss_result

    else:
        dg = criterion(g, data.per_cell_dataset.energy_g)
        gradients_loss_result = loss_result(
            loss_id="gradients",
            loss_value=dg,
            reference=data.per_cell_dataset.energy_g,
            prediction=g,
            components=None,
        )

        loss = de * w_energy + dg * w_gradients

        return loss_result(
            loss_id="total",
            loss_value=loss,
            reference=None,
            prediction=None,
            components=(energy_loss_result, gradients_loss_result),
        )


def charges_loss(networks, data, criterion):
    """
    Charges loss function.

    Parameters
    ----------
    networks : list
        A list of networks to learn.
    data : Dataset
        The dataset to compute loss function of.
    criterion : torch.nn.Module
        Loss criterion, defaults to MSE.

    Returns
    -------
    result : loss_result
        The resulting loss and accompanying information.
    """
    charges = fw_cauldron_charges(networks, data)
    loss = 0
    loss_components = []
    for charge, ppd in zip(charges, data.per_point_datasets):
        l = criterion(charge, ppd.charges)
        loss_components.append(loss_result(
            loss_id=ppd.tag,
            loss_value=l,
            reference=ppd.charges,
            prediction=charge,
            components=None,
        ))
        loss += l

    return loss_result(
        loss_id="total",
        loss_value=loss,
        reference=None,
        prediction=None,
        components=tuple(loss_components),
    )


LBFGS = partial(torch.optim.LBFGS, line_search_fn="strong_wolfe")


class SimpleClosure:
    def __init__(self, networks, loss_function, dataset=None, criterion=None, optimizer=None,
                 optimizer_kwargs=None, loss_function_kwargs=None):
        """
        A simple closure for learning NN potentials.

        Parameters
        ----------
        networks : list
            A list of networks to learn.
        loss_function : Callable
            A function `loss(networks, data, criterion, **loss_kwargs)`
            returning `loss_result` tuple.
        dataset : Dataset
            Default dataset to compute the loss for.
        criterion : torch.nn.Module
            Loss criterion, defaults to MSE.
        optimizer : torch.optim.Optimizer
            Optimizer, defaults to Adam.
        optimizer_kwargs : dict
            Additional optimizer arguments.
        loss_function_kwargs : dict
            Loss function arguments.
        """
        if criterion is None:
            criterion = torch.nn.MSELoss()
        if optimizer is None:
            optimizer = LBFGS
        if optimizer_kwargs is None:
            optimizer_kwargs = {}
        if loss_function_kwargs is None:
            loss_function_kwargs = {}
        self.networks = networks
        self.loss_function = loss_function
        self.dataset = dataset
        self.criterion = criterion
        self.__optimizer__ = optimizer
        self.__optimizer_kwargs__ = optimizer_kwargs
        self.optimizer = self.optimizer_init()
        self.loss_function_kwargs = loss_function_kwargs

        self.last_loss = None

    def optimizer_init(self, optimizer=None, **kwargs):
        """
        Initialize the optimizer.

        Parameters
        ----------
        optimizer
            Optimizer class.
        kwargs
            Arguments to the constructor.

        Returns
        -------
        optimizer
            The resulting optimizer object.
        """
        if optimizer is None:
            optimizer = self.__optimizer__
        opt_args = self.__optimizer_kwargs__.copy()
        opt_args.update(kwargs)
        self.optimizer = optimizer(self.learning_parameters(), **opt_args)
        return self.optimizer

    def learning_parameters(self):
        """
        Learning parameters.

        Returns
        -------
        params : Iterable
            Parameters to learn.
        """
        return chain(*tuple(i.parameters() for i in self.networks))

    def loss(self, dataset=None):
        """
        The loss function.

        Parameters
        ----------
        dataset : Dataset
            The dataset to compute loss function of.

        Returns
        -------
        result : stats_tuple
            The resulting loss and accompanying information.
        """
        if dataset is None:
            if self.dataset is None:
                raise ValueError("No dataset provided and the default dataset is None")
            dataset = self.dataset
        self.last_loss = self.loss_function(self.networks, dataset, self.criterion, **self.loss_function_kwargs)
        return self.last_loss

    def propagate(self, dataset=None):
        """
        Propagates the closure.

        Parameters
        ----------
        dataset : torch.utils.data.Dataset
            The dataset to compute loss function of.

        Returns
        -------
        result : torch.Tensor
            The resulting loss.
        """
        self.optimizer.zero_grad()
        loss_tuple = self.loss(dataset=dataset)
        loss = loss_tuple.loss_value
        loss.backward()
        return loss

    def __call__(self, dataset=None):
        return self.propagate(dataset=dataset)

    def optimizer_step(self):
        """
        Performs an optimization step.
        """
        return self.optimizer.step(self)


def simple_energy_closure(networks, dataset=None, criterion=None, optimizer=None, optimizer_kwargs=None,
                          w_energy=1, w_gradients=0, energies_p=False):
    """
    Energy and forces closure.

    Parameters
    ----------
    networks : list
        A list of networks to learn.
    dataset : Dataset
        Default dataset to compute loss for.
    criterion : torch.nn.Module
        Loss criterion, defaults to MSE.
    optimizer : torch.optim.Optimizer
        Optimizer, defaults to Adam.
    optimizer_kwargs : dict
        Additional optimizer arguments.
    w_energy : float
        Energy weight in the loss function.
    w_gradients : float
        Gradients weight in the loss function.
    energies_p : bool
        If True, considers the loss of partial energy.

    Returns
    -------
    closure : SimpleClosure
        The closure function.
    """
    return SimpleClosure(networks, energy_loss, dataset=dataset, criterion=criterion, optimizer=optimizer,
                         optimizer_kwargs=optimizer_kwargs,
                         loss_function_kwargs=dict(w_energy=w_energy, w_gradients=w_gradients, energies_p=energies_p))


def simple_charges_closure(networks, dataset=None, criterion=None, optimizer=None, optimizer_kwargs=None):
    """
    Charges closure.

    Parameters
    ----------
    networks : list
        A list of networks to learn.
    dataset : Dataset
        Default dataset to compute loss for.
    criterion : torch.nn.Module
        Loss criterion, defaults to MSE.
    optimizer : torch.optim.Optimizer
        Optimizer, defaults to Adam.
    optimizer_kwargs : dict
        Additional optimizer arguments.

    Returns
    -------
    closure : SimpleClosure
        The closure function.
    """
    return SimpleClosure(networks, charges_loss, dataset=dataset, criterion=criterion, optimizer=optimizer,
                         optimizer_kwargs=optimizer_kwargs)


def requires_fields(*names):
    """
    A decorator to ensure that the listed class fields are set.

    Parameters
    ----------
    names
        A list of fields.

    Returns
    -------
    decorator : Callable
        The decorator.
    """
    def _decorator(_f):
        @wraps(_f)
        def _sub(_self, *_args, **_kwargs):
            for i in names:
                if getattr(_self, i) is None:
                    raise RuntimeError(f"The field '{i}' is required at this stage")
            return _f(_self, *_args, **_kwargs)
        return _sub
    return _decorator


def pull(a):
    """
    Pulls array to numpy.

    Parameters
    ----------
    a : torch.Tensor

    Returns
    -------
    result : np.ndarray
        The resulting array.
    """
    return a.detach().cpu().numpy()


class FitWorkflow:
    def __init__(self, dtype=torch.float64, log=None, seed=None, mpl_backend=None):
        """
        A class defining a typical workflow when fitting.

        Parameters
        ----------
        dtype : torch.dtype
            Default floating point data type for all tensors involved.
        log : logging.Logger
            The logger for this.
        seed
            Initialize torch and numpy with the provided seed.
        """
        self.dtype = dtype
        if log is None:
            self.log = logging.getLogger(__name__)
        else:
            self.log = log

        self.cells = None  # A list of cells to learn from
        self.descriptors = None  # a dict with descriptors
        self._cutoff = None  # descriptor cutoff
        self.cells_nw = None  # wrapped cells
        self.dataset = None  # the dataset
        self.normalization = None  # dataset normalization
        self.scale_eV_per_atom = None  # eV per atom energy scale after normalization
        self.dataset_normalized = None  # normalized dataset
        self.nn = None  # neural networks
        self.closure = None  # closure
        self.nn_potentials = None  # neural-network potentials

        self.on_plot_update = None  # action to perform whenever plot is updated
        self.figures = None  # plot figures
        self.axes = None  # plot axes

        if seed is not None:
            np.random.seed(seed)
            torch.manual_seed(seed)

        if mpl_backend is not None:
            matplotlib.use(mpl_backend)

    @property
    def cutoff(self):
        return self._cutoff

    @cutoff.setter
    def cutoff(self, cutoff):
        self.log.info(f"Cutoff: {cutoff:.3e} = {cutoff / angstrom:.3f} A = {cutoff / aBohr:.3f} Bohr")
        self._cutoff = cutoff

    @classmethod
    def load_cells_individual(cls, filename):
        """
        Load a single piece of the dataset.

        Parameters
        ----------
        filename : str, Path
            The path to load.

        Returns
        -------
        result : list
            A list of Cells.
        """
        with open(filename, 'r') as f:
            json_data = json.load(f)
            if isinstance(json_data, dict):
                json_data = [json_data]
        return list(map(Cell.from_json, json_data))

    def load_cells(self, *filenames, root=None, subset=None):
        """
        Loads Cells (structural data) from files.

        Parameters
        ----------
        filenames
            File names or patterns to load.
        root : str, Path
            The root folder to load from.
        subset : int, None
            If specified, chose a random subset of the given size.

        Returns
        -------
        result : list
            The resulting cells.
        """
        self.log.info("Loading cells ...")
        root = Path() if root is None else Path(root)
        result = []
        for pattern in filenames:
            self.log.info(f"  pattern {pattern}")
            fns = list(root.glob(pattern))
            if len(fns) == 0:
                self.log.error(f"Pattern {pattern} not found in {root}")
                raise ValueError(f"File not found or no match for pattern '{pattern}'")
            for fn in fns:
                self.log.info(f"    file {fn}")
                result.extend(self.load_cells_individual(fn))
        if subset:
            self.log.info(f"Subset of size {subset:d} requested")
            subset = np.random.choice(len(result), subset)
            result = list(result[i] for i in subset)
        self.cells = result
        self.log.info(f"Total structure count: {len(result):d}")
        return result

    @requires_fields("cells_nw")
    def init_default_descriptors(self, n=6, a=12 * aBohr, left=1, common_grid=True):
        """
        Provides a default set of descriptors.

        Parameters
        ----------
        n : int
            Descriptor radial sampling.
        a : float
            Descriptor cutoff.
        left : float
            Left descriptor edge.
        common_grid : bool
            If True, all species share the same radial grid.

        Returns
        -------
        descriptors : dict
            The resulting descriptor set.
        """
        self.log.info(f"Preparing default descriptor set ...")
        self.log.info(f"  n = {n:d}")
        self.log.info(f"  a = {a:.3e} = {a / angstrom:.3f} A = {a / aBohr:.3f} Bohr")
        self.log.info(f"  left edge = {left:f}")
        self.log.info(f"  common grid: {common_grid}")
        descriptors = default_behler_descriptors(self.cells_nw, n=n, a=a, left=left, common_eta=common_grid)
        for k, v in default_behler_descriptors_3(self.cells_nw, a=a).items():
            descriptors[k].extend(v)
        self.descriptors = descriptors
        return descriptors

    def load_descriptors(self, arg):
        """
        Load descriptors from a file or a fictionary.

        Parameters
        ----------
        arg : str, Path, dict
            File with descriptors to parse or a dictionary with descriptors.

        Returns
        -------
        descriptors : dict
            The resulting descriptors.
        """
        if isinstance(arg, (str, Path)):
            self.log.info(f"Loading descriptors from {arg} ...")
            self.descriptors = parse_runner_input(arg)
        else:
            self.descriptors = arg
        self.log.info("Descriptors:")
        for k, v in sorted(self.descriptors.items()):
            n_desc = Counter(i.coordination_number for i in v)
            spec = ' '.join(f'{_k}p {_v}' for _k, _v in sorted(n_desc.items()))
            self.log.info(f"  {k} total {len(v)} {spec}")
        return self.descriptors

    @requires_fields("descriptors")
    def compute_cutoff(self):
        """
        Computes descriptor cutoff and returns it.

        Returns
        -------
        result : float
            The cutoff value.
        """
        self.cutoff = max(max(i.cutoff for i in dsc) for dsc in self.descriptors.values())
        return self.cutoff

    @requires_fields("cells", "_cutoff")
    def compute_neighbors(self, x):
        """
        Computes neighbors (images) data.

        Parameters
        ----------
        x : list, tuple
            Neighbor orders along unit cells' vectors.


        Returns
        -------
        cells_nw : list
            A list of wrapped cells.
        """
        self.log.info(f"Computing neighbors for {len(self.cells):d} structures ...")
        cells_nw = list(NeighborWrapper(i, x=x, cutoff=self.cutoff) for i in self.cells)
        self.cells_nw = cells_nw
        return cells_nw

    @requires_fields("cells_nw", "descriptors")
    def compute_descriptors(self, parallel=False, chunksize=None, **kwargs):
        """
        Computes descriptors.

        Parameters
        ----------
        parallel : bool, str
            If True, computes in multiple processes.
        chunksize : int, None
            The size of a single task in parallel mode. Defaults to 100.
        kwargs
            Arguments to `ml.learn_cauldron`.

        Returns
        -------
        result : Dataset
            The resulting dataset.
        """
        self.log.info(f"Computing descriptors for {len(self.cells_nw):d} structures ...")
        if parallel == "openmp":
            kwargs["prefer_parallel"] = True
            parallel = False
        elif parallel:
            if "prefer_parallel" in kwargs:
                v = kwargs["prefer_parallel"]
                if v is not False:
                    self.log.warning(f"The argument 'prefer_parallel' is explicitly set to {v}. It is advised to set "
                                     f"this argument to False to avoid interference and deadlocks between "
                                     f"multiprocessing, OpenMP and torch")
            else:
                kwargs["prefer_parallel"] = False

        worker = partial(learn_cauldron, descriptors=self.descriptors, normalize=False, **kwargs)

        if parallel:
            # Disable OpenMP because it causes deadlocks
            num_omp_threads = torch.get_num_threads()
            torch.set_num_threads(1)

            if chunksize is None:
                chunksize = 100
            n_parts = int(np.ceil(len(self.cells_nw) / chunksize))
            nu = serialize_nu()
            pool = torch.multiprocessing.Pool(initializer=load_nu, initargs=(nu,))
            self.log.info(f"  chunk size: {chunksize:d} parts total: {n_parts}")
            result = Dataset.cat(pool.map(
                worker,
                (self.cells_nw[i * chunksize:(i + 1) * chunksize] for i in range(n_parts)),
                chunksize=1,
            ))
            torch.set_num_threads(num_omp_threads)
        else:
            result = worker(self.cells_nw)

        self.dataset = self.dataset_normalized = result
        return result

    @requires_fields("dataset")
    def compute_normalization(self, **kwargs):
        """
        Computes normalization.

        Parameters
        ----------
        kwargs
            Arguments to `Normalization.from_dataset`.

        Returns
        -------
        norm : Normalization
            The normalization of the dataset.
        """
        self.log.info("Computing the normalization ...")
        defaults = dict(scale_energy=1000, offset_energy=True)
        defaults.update(kwargs)
        self.normalization = Normalization.from_dataset(self.dataset, **defaults)
        self.log.info("Energy offsets:")
        for k, v in zip(sorted(self.descriptors), self.normalization.energy_offsets.numpy().squeeze()):
            self.log.info(f"  {k}:\t{v:.6e} {v / Ry:.3e} Ry {v / eV:.3e} eV")
        e_scale = self.normalization.energy_scale.item()
        self.log.info(f"Energy scale: {e_scale:.6e} {e_scale / Ry:.6e} Ry {e_scale / eV:.6e} eV")
        return self.normalization

    @requires_fields("dataset", "normalization", "cells")
    def apply_normalization(self, inplace=True):
        """
        Applies the normalization.

        Parameters
        ----------
        inplace : bool
            If True, performs the operation in-place to save memory.

        Returns
        -------
        result : Dataset
            The normalized dataset.
        """
        self.log.info("Normalizing ...")
        result = self.normalization.fw(self.dataset, inplace=inplace)
        if inplace:
            self.dataset = None
        self.dataset_normalized = result
        self.scale_eV_per_atom = self.normalization.energy_scale.item() / eV / max(i.size for i in self.cells)
        return result

    @requires_fields("dataset_normalized")
    def init_nn(self, **kwargs):
        """
        Initializes neural networks into a random state.

        Parameters
        ----------
        kwargs
            Arguments to `SequentialSoleEnergyNN`.

        Returns
        -------
        result : list
            A list of initialized networks (torch Modules).
        """
        self.log.info("Initializing neural networks ...")
        self.nn = list(
            SequentialSoleEnergyNN(i.n_features, **kwargs).to(dtype=self.dtype)
            for i in self.dataset_normalized.per_point_datasets
        )
        return self.nn

    @requires_fields("dataset_normalized", "nn")
    def cuda(self):
        """Moves data to CUDA."""
        self.log.info("Moving NNs to CUDA ...")
        for i in self.nn:
            i.cuda()
        self.log.info("Moving the dataset to CUDA ...")
        for piece in self.dataset_normalized.datasets:
            piece.tensors = list(i if i is None else i.cuda() for i in piece.tensors)

    @requires_fields("dataset_normalized", "nn")
    def init_closure(self, **kwargs):
        """
        Initializes the closure.

        Parameters
        ----------
        kwargs
            Arguments to `simple_energy_closure`.

        Returns
        -------
        result : SimpleClosure
            The closure.
        """
        self.log.info("Init closure ...")
        self.closure = simple_energy_closure(self.nn, self.dataset_normalized, **kwargs)
        self.log.info(f"  optimizer: {self.closure.optimizer}")
        self.log.info(f"  loss function: {self.closure.loss_function}")
        self.log.info(f"  loss arguments: {self.closure.loss_function_kwargs}")
        return self.closure

    def __on_plot_update__(self):
        if self.on_plot_update == "save":
            self.save_plots()
        elif self.on_plot_update == "show":
            pyplot.show()
        elif self.on_plot_update is not None:
            self.on_plot_update(self)

    @requires_fields("figures")
    def save_plots(self):
        for k, fig in self.figures.items():
            fig.savefig(f"{k}.pdf")

    @requires_fields("closure")
    def init_plots(self, on_plot_update=None):
        """
        Initializes runtime plots.

        Parameters
        ----------
        on_plot_update : str, Callable, None
            Action to perform whenever plots are updated. "save" stands
            for saving into separate pdf files.
        """
        self.on_plot_update = on_plot_update
        self.figures = f = {}
        self.axes = a = {}
        f["convergence"], (a["diagonal"], a["convergence"]) = pyplot.subplots(1, 2, figsize=(12, 6), dpi=150)
        loss = self.closure.last_loss
        if loss is None:
            self.log.info("Computing starting loss value ...")
            loss = self.closure.loss()
        plot_convergence(pull(loss.loss_value).item(), append=False, ax=a["convergence"])
        if loss.reference is None:
            loss = loss.components[0]
        plot_diagonal(
            pull(loss.reference).squeeze() * self.scale_eV_per_atom,
            pull(loss.prediction).squeeze() * self.scale_eV_per_atom,
            ax=a["diagonal"],
            replace=False,
        )
        self.__on_plot_update__()

    @requires_fields("closure")
    def update_plots(self):
        """Updates plots."""
        loss = self.closure.last_loss
        plot_convergence(pull(loss.loss_value).item(), append=True, ax=self.axes["convergence"])
        if loss.reference is None:
            loss = loss.components[0]
        plot_diagonal(
            pull(loss.reference).squeeze() * self.scale_eV_per_atom,
            pull(loss.prediction).squeeze() * self.scale_eV_per_atom,
            ax=self.axes["diagonal"],
            replace=True,
        )
        self.__on_plot_update__()

    @requires_fields("closure")
    def epoch(self, cleanup=True):
        """
        Runs an optimizer epoch.

        Parameters
        ----------
        cleanup : bool
            if True, cleans up the optimizer memory before running the epoch.

        Returns
        -------
        loss
            The resulting loss data.
        """
        self.log.info(f"Running epoch ...")
        if cleanup:
            self.closure.optimizer_init()
        self.closure.optimizer_step()
        loss = self.closure.last_loss
        self.log.info(f"  loss={pull(loss.loss_value).item():.3e}")
        return loss

    @requires_fields("nn", "descriptors", "normalization")
    def build_potentials(self):
        """
        Initializes NN potentials.

        Returns
        -------
        potentials : list
            A list of potentials.
        """
        self.nn_potentials = potentials_from_ml_data(self.nn, self.descriptors, normalization=self.normalization)
        return self.nn_potentials

    @requires_fields("nn_potentials")
    def save_potentials(self, filename="potentials.pt"):
        """
        Saves potentials as a file.

        Parameters
        ----------
        filename : str
            Save location.
        """
        torch.save(list(i.state_dict() for i in self.nn_potentials), filename)

    def prepare(self, fn_cells, neighbor_x,
                cells_subset=None,
                descriptors=None,
                cutoff=12 * aBohr,
                fn_cells_root=None,
                parallel=False,
                parallel_descriptor_chunksize=None,
                learn_cauldron_kwargs=None,
                normalization_kwargs=None,
                inplace_normalization=True,
                nn_kwargs=None, cuda=False,
                closure_kwargs=None,
                on_plot_update=None,
                default_descriptor_kwargs=None
                ):
        """
        Prepares the data for the workflow.
        """
        if isinstance(fn_cells, str):
            fn_cells = [fn_cells]
        self.load_cells(*fn_cells, root=fn_cells_root, subset=cells_subset)
        if descriptors is not None:
            self.load_descriptors(descriptors)
            self.compute_cutoff()
            self.compute_neighbors(neighbor_x)
        else:
            self.cutoff = cutoff
            self.compute_neighbors(neighbor_x)
            if default_descriptor_kwargs is None:
                default_descriptor_kwargs = dict(a=self.cutoff)
            self.init_default_descriptors(**default_descriptor_kwargs)
        if learn_cauldron_kwargs is None:
            learn_cauldron_kwargs = dict()
        self.compute_descriptors(parallel, chunksize=parallel_descriptor_chunksize, **learn_cauldron_kwargs)
        if normalization_kwargs is None:
            normalization_kwargs = dict()
        self.compute_normalization(**normalization_kwargs)
        self.apply_normalization(inplace=inplace_normalization)
        if nn_kwargs is None:
            nn_kwargs = dict()
        self.init_nn(**nn_kwargs)
        if cuda:
            self.cuda()
        if closure_kwargs is None:
            closure_kwargs = dict()
        self.init_closure(**closure_kwargs)
        self.init_plots(on_plot_update=on_plot_update)

    def run(self, n_epochs=1000, cleanup_optimizer=True, potential_fn=None):
        """
        Runs the training scenario.

        Parameters
        ----------
        n_epochs : int
            Number of epochs to run.
        cleanup_optimizer : bool
            if True, cleans up the optimizer memory before running each epoch.
        potential_fn : str, None
            If set, saves intermediate potentials data to the desired location.
        """
        for epoch in range(n_epochs):
            self.log.info(f"Epoch {epoch:d}")
            self.epoch(cleanup=cleanup_optimizer)
            self.update_plots()
            if potential_fn is not None:
                self.build_potentials()
                self.save_potentials(filename=potential_fn)
