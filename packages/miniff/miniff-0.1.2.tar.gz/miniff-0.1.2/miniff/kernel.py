from .potentials import LocalPotential, PotentialRuntimeWarning, eval_potentials
from .ml import NNPotential, __assert_dimension_count__, __assert_same_dimension__  # TODO: implement kernel.py independent of this import
from .util import ParameterUnits, dict_reduce, ArrayWithUnits

import numpy as np
from scipy.sparse import coo_matrix, csr_matrix
from scipy.optimize import minimize
from scipy.spatial import cKDTree

from functools import partial
from itertools import product
from warnings import warn, catch_warnings, simplefilter


class RelaxError(RuntimeError):
    def __init__(self, *args, progress=None):
        super().__init__(*args)
        self.progress = progress


def encode_species(species, lookup, default=None):
    """
    Transforms species into an array of integers encoding species.

    Parameters
    ----------
    species : list, tuple, np.ndarray
        Species to encode.
    lookup : dict
        A lookup dictionary.
    default : int
        The default value to replace non-existing entries. If None,
        raises KeyError.

    Returns
    -------
    result : np.ndarray
        The resulting integer array.
    """
    result = []
    for i in species:
        try:
            result.append(lookup[i])
        except KeyError:
            if default is not None:
                result.append(default)
            else:
                raise KeyError(f"Could not encode specimen '{i}' with lookup {lookup}. "
                               "Set `default=-1`, for example, to assign unknown species")
    return np.array(result, dtype=np.int32)


def encode_potentials(potentials, lookup, default=None):
    """
    Encodes potentials to have species as integers.

    Parameters
    ----------
    potentials : list, tuple
        Potentials to encode.
    lookup : dict
        A lookup dictionary.
    default : int
        The default value to replace non-existing entries. If None,
        raises KeyError.

    Returns
    -------
    result : list
        The resulting list of potentials.
    """
    result = list(i.copy(tag=encode_species(i.tag.split("-"), lookup, default=default)) for i in potentials)
    for i in result:
        # TODO: avoid infinite recursion here
        if isinstance(i, NNPotential):
            i.parameters["descriptors"] = encode_potentials(i.parameters["descriptors"], lookup, default=default)
    return result


class SpeciesEncoder:
    def __init__(self, species):
        """
        A mixin for encoding species into integers.

        Parameters
        ----------
        species : list, tuple, np.ndarray
            A collection of species.
        """
        species = np.array(species)
        self.species, self.spec_encoded_row = np.unique(species, return_inverse=True)
        self.spec_encoded_row = self.spec_encoded_row.astype(np.int32)
        self.species_lookup = dict(zip(self.species, np.arange(len(self.species))))

    def encode_species(self, species, default=None):
        """
        Transforms species into an array of integers encoding species.

        Parameters
        ----------
        species : list, tuple
            Species to encode.
        default : int
            The default value to replace non-existing entries. If None,
            raises KeyError.

        Returns
        -------
        result : np.ndarray
            The resulting integer array.
        """
        return encode_species(species, self.species_lookup, default=default)
    encode = encode_species

    def encode_potentials(self, potentials, default=None):
        """
        Encodes potentials to have species as integers.

        Parameters
        ----------
        potentials : list, tuple
            Potentials to encode.
        default : int
            The default value to replace non-existing entries. If None,
            raises KeyError.

        Returns
        -------
        result : np.ndarray
            The resulting integer array.
        """
        return encode_potentials(potentials, self.species_lookup, default=default)


class Cell:
    def __init__(self, vectors, coordinates, values, meta=None):
        """
        A minimal implementation of a box with points.

        Parameters
        ----------
        vectors : np.ndarray, list, tuple
            Box vectors.
        coordinates : np.ndarray, list, tuple
            Point coordinates in the box basis.
        values : np.ndarray, list, tuple
            Point specifiers.
        meta : dict
            Optional metadata.
        """
        vectors = np.asanyarray(vectors)
        coordinates = np.asanyarray(coordinates)
        values = np.asanyarray(values)

        inputs = locals()

        __assert_dimension_count__(inputs, "vectors", 2, "coordinates", 2, "values", 1)
        __assert_same_dimension__(inputs, "basis size", "coordinates", 1, "vectors", 0)
        self.vectors = vectors
        self.coordinates = coordinates
        self.values = values
        if meta is None:
            self.meta = {}
        else:
            self.meta = dict(meta)

    @property
    def size(self):
        return len(self.coordinates)

    def copy(self):
        """
        A copy of the box.

        Returns
        -------
        copy : Cell
            The copy.
        """
        return Cell(self.vectors.copy(), self.coordinates.copy(), self.values.copy(), self.meta)

    def cartesian(self):
        """
        Cartesian coordinates of points.

        Returns
        -------
        coords : np.ndarray
            The coordinates.
        """
        return self.coordinates @ self.vectors

    def transform_from_cartesian(self, coordinates):
        """
        Transforms coordinates from cartesian.

        Parameters
        ----------
        coordinates : np.ndarray
            Coordinates to transform.

        Returns
        -------
        result : ndarray
            The transformed coordinates.
        """
        return coordinates @ np.linalg.inv(self.vectors)

    def distances(self, cutoff=None, other=None):
        """
        Computes inter-point distances.

        Parameters
        ----------
        cutoff : float
            Cutoff for obtaining distances.
        other : Cell, np.ndarray
            Other cell to compute distances to

        Returns
        -------
        result : np.ndarray, csr_matrix
            The resulting distance matrix.
        """
        this = self.cartesian()
        if other is None:
            other = this
        elif isinstance(other, Cell):
            other = other.cartesian()

        if cutoff is None:
            return np.linalg.norm(this[:, np.newaxis] - other[np.newaxis, :], axis=-1)
        else:
            this = cKDTree(this)
            other = cKDTree(other)
            return this.sparse_distance_matrix(other, max_distance=cutoff, )

    def repeated(self, *args):
        """
        Prepares a supercell.

        Parameters
        ----------
        *args
            Repeat counts along each vector.

        Returns
        -------
        supercell : Cell
            The resulting supercell.
        """
        args = np.array(args, dtype=int)
        x = np.prod(args)
        vectors = self.vectors * args[np.newaxis, :]
        coordinates = np.tile(self.coordinates, (x, 1))
        coordinates /= args[np.newaxis, :]
        coordinates.shape = (x, *self.coordinates.shape)
        values = np.tile(self.values, x)
        shifts = list(np.linspace(0, 1, i, endpoint=False) for i in args)
        shifts = np.meshgrid(*shifts)
        shifts = np.stack(shifts, axis=-1)
        shifts = shifts.reshape(-1, shifts.shape[-1])
        coordinates += shifts[:, np.newaxis, :]
        coordinates = coordinates.reshape(-1, coordinates.shape[-1])
        return Cell(vectors, coordinates, values)

    @classmethod
    def from_json(cls, data):
        assert data["type"] in ("dfttools.utypes.CrystalCell", "dfttools.types.UnitCell")
        if data["meta"] is not None:
            meta = dict()
            for k, v in data["meta"].items():
                if isinstance(v, dict) and v.get("_type", None) == "numpy":
                    v = ArrayWithUnits.from_json(v)
                meta[k] = v
        else:
            meta = None
        return Cell(
            ArrayWithUnits.from_json(data["vectors"]),
            ArrayWithUnits.from_json(data["coordinates"]),
            ArrayWithUnits.from_json(data["values"]),
            meta=meta,
        )


class NeighborWrapper(SpeciesEncoder):
    def __init__(self, cell, x=(2, 2, 2), normalize=True, cutoff=None):
        """
        Sparse inter-atomic distance data and local potential computations.

        Parameters
        ----------
        cell
            The unit cell with atom coordinates.
        x
            The number of cell replica included in distance calculation.
        normalize : bool
            Normalizes the cell if True.
        cutoff : float
            If set, computes distance information immediately.
        """
        self.shift_vectors = self.cell = self.cutoff = self.sparse_pair_distances = self.species =\
            self.spec_encoded_row = self.cartesian_row = self.cartesian_col = self.species_lookup = None
        self._cart2cry_transform_matrix = None
        self.set_x(x)
        self.set_cell(cell, normalize=normalize)
        if cutoff is not None:
            self.compute_distances(cutoff)

    @property
    def size(self) -> int:
        return self.cell.size

    @property
    def meta(self) -> dict:
        return self.cell.meta

    @property
    def vectors(self) -> np.ndarray:
        return self.cell.vectors

    @property
    def coordinates(self) -> np.ndarray:
        return self.cell.coordinates

    @property
    def values(self) -> np.ndarray:
        return self.cell.values

    def set_x(self, x):
        """
        Sets the periodic environment.

        Parameters
        ----------
        x : list
            The number of neighbors along each dimension.
        """
        x = np.array(x, dtype=int)
        x2 = 2 * x - 1
        xp = np.prod(x2)
        shift_vectors = []
        for i in range(xp):
            shift_vectors.append((np.unravel_index(i, x2) - x + 1))
        self.shift_vectors = np.array(shift_vectors)

    def set_cell(self, cell, normalize=True):
        """
        Set a new unit cell to work with.

        Parameters
        ----------
        cell
            The unit cell with atom coordinates.
        normalize : bool
            Normalizes the cell if True.
        """
        self.cell = cell.copy()
        if normalize:
            self.cell.coordinates %= 1
        self.cutoff = self.sparse_pair_distances = self.species = self.spec_encoded_row = self.cartesian_row =\
            self.cartesian_col = None
        self._cart2cry_transform_matrix = np.linalg.inv(self.cell.vectors)
        self.cartesian_row = cell.cartesian()

    def set_cell_cartesian(self, cartesian, normalize=True):
        """
        Sets new cartesian coordinates.

        Parameters
        ----------
        cartesian
            Atomic coordinates.
        normalize : bool
            Normalizes the cell if True.
        """
        self.cell.coordinates = np.array(cartesian @ self._cart2cry_transform_matrix)
        self.cartesian_row = cartesian
        if normalize:
            self.cell.coordinates %= 1
            self.cartesian_row = self.cell.coordinates @ self.cell.vectors

    def compute_distances(self, cutoff):
        """
        Compute sparse distances and masks using CKDTree by scipy.

        Parameters
        ----------
        cutoff : float
            Maximal distance computed (smaller=faster).
        """
        # Create a super-cell with neighbors
        self.cartesian_col = (self.cartesian_row[np.newaxis, :, :] +
                              (self.shift_vectors @ self.cell.vectors)[:, np.newaxis, :]).reshape(-1, 3)

        # Collect close neighbors
        t_row = cKDTree(self.cartesian_row)
        t_col = cKDTree(self.cartesian_col)

        spd = t_row.sparse_distance_matrix(t_col, cutoff, output_type="coo_matrix")

        # Get rid of the-diagonal
        mask = spd.row + len(self.shift_vectors) // 2 * len(self.cartesian_row) != spd.col
        self.sparse_pair_distances = coo_matrix((spd.data[mask], (spd.row[mask], spd.col[mask])), shape=spd.shape).tocsr()

        # Encode species in integers
        SpeciesEncoder.__init__(self, self.cell.values)

        self.cutoff = cutoff

    def pair_reduction_function(self, f):
        """
        Pair reduction function.

        Parameters
        ----------
        f : Callable
            A function reducing pair-specific distances,
            see `self.rdf` for an example.

        Returns
        -------
        result : dict
            Pair function values.
        """
        if self.species is None:
            raise ValueError("No distance information available: please run .compute_distances")
        result = {}
        distances = self.sparse_pair_distances.tocoo()
        pair_id = self.spec_encoded_row[distances.row] * len(self.species) + self.spec_encoded_row[
            distances.col % distances.shape[0]]
        for i_s1, s1 in enumerate(self.species):
            for i_s2, s2 in enumerate(self.species[i_s1:]):
                i_s2 += i_s1
                k = "-".join((s1, s2))
                pid = i_s1 * len(self.species) + i_s2
                mask = pair_id == pid
                spd = distances.data[mask]
                val = f(spd)
                if val is not None:
                    result[k] = val
        return result

    def rdf(self, r, sigma):
        """
        Computes the radial distribution function.

        Parameters
        ----------
        r : np.ndarray, float
            Radius values.
        sigma : float
            Smearing.

        Returns
        -------
        result : dict
            Radial distribution function values.
        """
        if not isinstance(r, np.ndarray):
            r = np.array([r], dtype=float)
            squeeze = True
        else:
            squeeze = False
        factor = 1 / sigma / (2 * np.pi) ** .5

        def f(spd):
            weights = np.exp(- (spd[:, np.newaxis] - r[np.newaxis, :]) ** 2 / 2 / sigma ** 2).sum(axis=0)
            return weights * factor / 4 / np.pi / r ** 2

        result = self.pair_reduction_function(f)
        if squeeze:
            return {k: v[0] for k, v in result.items()}
        else:
            return result

    def eval(self, potentials, kname, squeeze=True, resolved=True, ignore_missing_species=False, out=None, **kwargs):
        """
        Calculates potentials: values, gradients and more.

        Parameters
        ----------
        potentials : list, LocalPotential
            A list of potentials or a single potential.
        kname : str, None
            Function to evaluate: 'kernel', 'kernel_gradient' or whatever
            other kernel function set for all potentials in the list.
        squeeze : bool
            If True, returns a single array whenever a single potential
            is passed.
        resolved : bool
            If True, the first dimension of the returned arrays corresponds
            to atomic contributions. Otherwise the first dimension is summed
            over.
        ignore_missing_species : bool
            If True, no error is raised whenever a specimen in the
            potential description is not found in the cell.
        out : np.ndarray
            The output buffer `[n_potentials, n_atoms]` for
            kname == "kernel" and `[n_potentials, n_atoms, n_atoms, 3]`
            for kname == "kernel_gradient". Any kind of reduction including
            `resolved=False` and calls `self.total`, `self.grad` calls will
            use the buffer for intermediate results but will still allocate
            a new array for the output.
        kwargs
            Other arguments to `eval_potentials`.

        Returns
        -------
        result : list, np.ndarray
            The result of the potential computation given the cell data.
        """
        sole = isinstance(potentials, LocalPotential)
        if sole:
            potentials = potentials,

        encoded_potentials = self.encode_potentials(potentials, default=-1 if ignore_missing_species else None)
        out = eval_potentials(encoded_potentials, kname, self.sparse_pair_distances, self.cartesian_row,
                              self.cartesian_col, self.spec_encoded_row, pre_compute_r=False, cutoff=self.cutoff,
                              out=out, **kwargs)
        if not resolved:
            out = out.sum(axis=1)
        if sole and squeeze:
            return out[0]
        else:
            return out

    def total(self, potentials, kname="kernel", **kwargs):
        """
        Total energy as a sum of all possible potential terms.

        Note that this function totally ignores any symmetry issues related to
        double-counting, etc.

        Parameters
        ----------
        potentials : list
            Potentials to compute.
        kname : str, None
            Function to evaluate.
        kwargs
            Other keyword arguments to `eval`.

        Returns
        -------
        energy : float
            The total energy value.
        """
        return self.eval(potentials, kname, squeeze=False, resolved=False, **kwargs).sum(axis=0)

    def grad(self, potentials, kname="kernel_gradient", **kwargs):
        """
        Total energy gradients.

        Similarly to `self.total`, this function totally ignores
        any symmetry issues related to double-counting, etc.

        Parameters
        ----------
        potentials : list
            Potentials to compute.
        kname : str, None
            Function to evaluate.
        kwargs
            Other keyword arguments to `eval`.

        Returns
        -------
        gradients : np.ndarray
            Total energy gradients.
        """
        return self.eval(potentials, kname, squeeze=False, resolved=False, **kwargs).sum(axis=0)

    def relax(self, potentials, rtn_history=False, units="atomic", normalize=True, interstitial=None,
              raise_on_warning=False, inplace=False, **kwargs):
        """
        Finds the local minimum of the base cell.

        Parameters
        ----------
        potentials : list
            Potential to use.
        rtn_history : bool
            If True, returns intermediate atomic configurations.
        units : ParameterUnits, str, None
            A ParameterUnits dictionary with 'energy' and 'length' entries set.
        normalize : bool
            Normalizes the cell at each step if True.
        interstitial : Callable
            A function `interstitial(energy)` returning a modified
            energy and its derivative with respect to the old energy value;
        raise_on_warning : bool
            If True, will raise a RelaxError whenever a PotentialRuntimeWarning is caught.
        inplace : bool
            If True, modifies this wrapper to enclose the relaxed cell.
        kwargs
            Keyword arguments to `scipy.optimize.minimize`.

        Returns
        -------
        cell : CrystalCell, list
            Either final unit cell or a history of all unit cells during the relaxation.
        """
        if self.cutoff is None:
            raise ValueError("No distance information available: please run .compute_distances")
        if units is None:
            units = ParameterUnits()
        elif units == "atomic":
            units = ParameterUnits({"length": "angstrom", "energy": "Ry"})
        orig_cartesian = self.cell.cartesian()
        orig_cutoff = self.cutoff

        history = []

        def target(_cartesian, kind):
            self.set_cell_cartesian(_cartesian.reshape(-1, 3) * units.get_uv("length"), normalize=normalize)
            self.compute_distances(orig_cutoff)

            if raise_on_warning:
                with catch_warnings(record=True) as w:
                    simplefilter("always", category=PotentialRuntimeWarning)

                    _total = self.total(potentials)
                    _grad = self.grad(potentials)
            else:
                _total = self.total(potentials)
                _grad = self.grad(potentials)

            _cell = self.cell.copy()

            if "energy" in units:
                _cell.meta["total-energy"] = ArrayWithUnits(_total, units=units["energy"])
            else:
                _cell.meta["total-energy"] = _total
            if "energy" in units and "length" in units:
                _cell.meta["forces"] = ArrayWithUnits(- _grad, units=f"({units['energy']})/({units['length']})")
            else:
                _cell.meta["forces"] = - _grad
            history.append(_cell)

            if raise_on_warning and len(w) > 0:
                raise RelaxError(str(w[0]), history)

            if interstitial is not None:
                _total, _dtotal = interstitial(_total)
                _grad *= _dtotal

            if kind == "f":
                return _total / units.get_uv("energy")
            elif kind == "g":
                return _grad.reshape(-1) / (units.get_uv("energy") / units.get_uv("length"))
            elif kind is None:
                pass
            else:
                raise ValueError(f"Unknown kind='{kind}'")

        result = minimize(
            partial(target, kind="f"),
            x0=orig_cartesian.reshape(-1) / units.get_uv("length"),
            jac=partial(target, kind="g"),
            **kwargs)

        if not result.success:
            warn(result.message)

        # Set metadata for the final cell
        target(result.x, None)

        # Restore
        if not inplace:
            self.set_cell_cartesian(orig_cartesian)
            self.compute_distances(orig_cutoff)

        if rtn_history:
            return history
        else:
            return history[-1]


def batch_rdf(cells, *args, **kwargs):
    """
    Averaged radial distribution function.

    Parameters
    ----------
    cells : list, tuple
        A collection of wrapped cells to process.
    args
    kwargs
        Arguments to `NeighborWrapper.rdf`.

    Returns
    -------
    result : dict
        Radial distribution function values.
    """
    def mean(x):
        return sum(x) / len(x)
    return dict_reduce((w.rdf(*args, **kwargs) for w in cells), mean)


def profile(potentials, f, *args, x):
    """
    Profiles a collection of potentials.

    Parameters
    ----------
    potentials : list
        Potentials to profile.
    f : Callable
        A function `f(x1, ...) -> UnitCell` preparing a unit cell
        for the given set of parameters.
    args
        Sampling of `x1`, ... arguments of the function `f`.
    x : tuple
        The number of cell replica included in distance calculation.

    Returns
    -------
    energy : np.ndarray
        Energies on the multidimensional grid defined by `args`.
    """
    if not isinstance(potentials, (list, tuple)):
        potentials = potentials,

    result = np.empty(tuple(len(i) for i in args), dtype=float)
    result_shape = result.shape
    result.shape = result.size,

    cutoff = max(i.cutoff for i in potentials)

    for i, pt in enumerate(product(*args)):
        cell = f(*pt)
        wrapped = NeighborWrapper(cell, x=x, cutoff=cutoff)
        result[i] = wrapped.total(potentials, ignore_missing_species=True)

    result.shape = result_shape
    return result


def profile_strain(potentials, cell, *args, x):
    """
    Profiles a collection of potentials by applying strain.

    Parameters
    ----------
    potentials : list
        Potentials to profile.
    cell : UnitCell
        The original cell.
    args
        Relative strains along all vectors.
    x : tuple
        The number of cell replica included in distance calculation.

    Returns
    -------
    energy : np.ndarray
        Energies of strained cells.
    """
    cell_copy = cell.copy()

    def _f(*_strain):
        _s = np.ones(len(cell.vectors))
        _s[:len(_strain)] = _strain
        cell_copy.vectors = cell.vectors * _s[:, np.newaxis]
        return cell_copy

    return profile(potentials, _f, *args, x=x)


def profile_directed_strain(potentials, cell, strain, direction, x):
    """
    Profiles a collection of potentials by applying strain.

    Parameters
    ----------
    potentials : list
        Potentials to profile.
    cell : UnitCell
        The original cell.
    strain : Iterable
        The relative strain.
    direction : list, tuple, np.ndarray
        The strain direction.
    x : tuple
        The number of cell replica included in distance calculation.

    Returns
    -------
    energy : np.ndarray
        Energies of strained cells.
    """
    cell_copy = cell.copy()
    direction = np.array(direction)

    def _f(_strain):
        cell_copy.vectors = cell.vectors * (direction * _strain + (1 - direction))[:, np.newaxis]
        return cell_copy

    return profile(potentials, _f, strain, x=x)
