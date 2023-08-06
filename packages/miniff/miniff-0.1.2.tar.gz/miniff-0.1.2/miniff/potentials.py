from functools import partial
from inspect import getfullargspec

import numpy as np
from scipy.optimize import minimize_scalar, root_scalar
from scipy.sparse import csr_matrix

from . import _potentials
from ._util import calc_sparse_distances
from .util import num_grad, ParameterUnits

# This sets the default policy for preferring parallel routines over serial. It can be changed during runtime
_prefer_parallel = True


class PotentialRuntimeWarning(RuntimeWarning):
    pass


def num_grad_potential(f, pre_compute_r_functions=None, **kwargs):
    """
    Constructs a function evaluating numerical gradients of a potential.

    Parameters
    ----------
    f : Callable
        A callable computing scalar potentials.
    pre_compute_r_functions : list
        A list of r-dependent quantities to pre-compute.
    kwargs
        Keyword arguments to `num_grad`.

    Returns
    -------
    f_grad : Callable
        A callable computing numerical gradient.
    """

    def f_grad(r_indptr, r_indices, _, cartesian_row, cartesian_col, species_row, species_mask, out, **parameters):
        parameters = parameters.copy()

        def _f_row(_cartesian_row):
            _r_data = calc_sparse_distances(r_indptr, r_indices, _cartesian_row, cartesian_col)
            if pre_compute_r_functions is not None:
                parameters["pre_compute_r"] = pre_compute_r(_r_data, pre_compute_r_functions, parameters)
            _out = np.zeros(shape_for_kernel("kernel", len(_cartesian_row)), dtype=float)
            f(r_indptr, r_indices, _r_data, _cartesian_row, cartesian_col, **parameters, species_row=species_row,
              species_mask=species_mask, out=_out)
            return _out

        def _f_col(_cartesian_col):
            _r_data = calc_sparse_distances(r_indptr, r_indices, cartesian_row, _cartesian_col)
            if pre_compute_r_functions is not None:
                parameters["pre_compute_r"] = pre_compute_r(_r_data, pre_compute_r_functions, parameters)
            _out = np.zeros(shape_for_kernel("kernel", len(cartesian_row)), dtype=float)
            f(r_indptr, r_indices, _r_data, cartesian_row, _cartesian_col, **parameters, species_row=species_row,
              species_mask=species_mask, out=_out)
            return _out

        row_grad = num_grad(_f_row, cartesian_row, **kwargs)
        col_grad = num_grad(_f_col, cartesian_col, **kwargs).reshape((row_grad.shape[0], -1, *row_grad.shape[1:])).sum(
            axis=1)
        out += row_grad + col_grad

    return f_grad


def kernel_on_site(r_indptr, r_indices, r_data, cartesian_row, cartesian_col, v0, species_row, species_mask, out):
    """
    A simple constant on-site potential scalar value.
    Most input arguments are irrelevant.
    """
    out[species_row == species_mask[0]] += v0


def kernel_g_on_site(r_indptr, r_indices, r_data, cartesian_row, cartesian_col, v0, species_row, species_mask, out):
    """
    The gradient of on-site potential is zero.
    """
    pass


def repr_potential(potential, units=None):
    """
    Represents potential.

    Parameters
    ----------
    potential : LocalPotential
        The potential.
    units : ParameterUnits
        Units of parameters.

    Returns
    -------
    result : str
        Representation string.
    """
    if units is None:
        repr_p = str(potential.parameters)
    else:
        repr_p = units.repr(potential.parameters)
    return ''.join([
        f"{potential.__class__.__name__}({potential.coordination_number:d}, {repr_p}, "
        f"{potential.cutoff}",
        ''.join(
            f", {k}={repr(v)}"
            for k, v in sorted(potential.kernels.items())
        ),
        f", tag={repr(potential.tag)})",
    ])


known_families = {}  # This dict is here for restoring json representations of potentials


class LocalPotentialFamily:
    def __init__(self, coordination_number, parameters, cutoff, kernel, kernel_gradient=None, kernel_parallel=None,
                 kernel_gradient_parallel=None, parameter_units=None, parameter_defaults=None, tag=None, proto=None,
                 pre_compute_r=None):
        """
        Represents a local potential family with the same potential shape and
        arbitrary parameter values.

        Parameters
        ----------
        coordination_number : int
            The potential coordination number.
        parameters : dict
            A dictionary with keys being potential parameters and values being parameter bounds.
        cutoff : float, str, Callable
            The cutoff value, parameter name or a function of parameters.
        kernel : Callable
            A callable for evaluating potential values.
        kernel_gradient : Callable
            A callable for evaluating potential gradients.
        kernel_parallel : Callable
            A callable for evaluating potential values using OpenMP parallelizm.
        kernel_gradient_parallel : Callable
            A callable for evaluating potential gradientsusing OpenMP parallelizm.
        parameter_units : ParameterUnits
            A dictionary with units per parameter.
        parameter_defaults : dict
            A dictionary with parameter default values.
        tag : str
            Optional tag
        proto : class
            A class wrapping constructed potentials.
        pre_compute_r : list
            A list of quantities depending on inter-atomic distance r
            that can be shared across several potentials of the same
            family.
        """
        if kernel_gradient is None:
            kernel_gradient = num_grad_potential(kernel)
        if proto is None:
            proto = LocalPotential

        self.coordination_number = coordination_number
        self.parameters = parameters
        self.parameter_units = parameter_units
        self.parameter_defaults = parameter_defaults if parameter_defaults is not None else dict()
        self.__cutoff_handle__ = cutoff
        self.kernels = dict(kernel=kernel, kernel_gradient=kernel_gradient, kernel_parallel=kernel_parallel,
                            kernel_gradient_parallel=kernel_gradient_parallel)
        self.tag = tag
        self.proto = proto
        if pre_compute_r is not None:
            self.pre_compute_r = []
            for fun in pre_compute_r:
                args = getfullargspec(fun)[0]
                del args[0]
                self.pre_compute_r.append((tuple(args), fun))
            self.pre_compute_r = tuple(self.pre_compute_r)
        else:
            self.pre_compute_r = None
        if tag is not None:
            if tag in known_families:
                raise RuntimeError(f"A potential family tagged '{tag}' has already been set")
            known_families[tag] = self

    def cutoff(self, kwargs):
        if isinstance(self.__cutoff_handle__, (float, int)):
            return self.__cutoff_handle__
        elif isinstance(self.__cutoff_handle__, str):
            return kwargs[self.__cutoff_handle__]
        elif callable(self.__cutoff_handle__):
            return self.__cutoff_handle__(kwargs)
        else:
            raise RuntimeError(f"Do not recognize the cutoff handle: {self.__cutoff_handle__}")

    def instantiate(self, tag=None, **kwargs):
        """
        Instantiate this potential to a LocalPotential with parameter
        values set.

        Parameters
        ----------
        tag : str
            An optional tag.
        kwargs
            Values of parameters.

        Returns
        -------
        result : LocalPotential
            The potential.
        """
        parameters = self.parameter_defaults.copy()
        parameters.update({k: (np.array(v) if isinstance(v, (list, tuple)) else v) for k, v in kwargs.items()})
        for k, r in self.parameters.items():
            if k not in parameters:
                raise ValueError(f"Parameter '{k}' is missing from defined parameters")
            if r is not None:
                l, u = r
                p = parameters[k]
                if not np.all((l <= p) <= u):
                    raise ValueError(f"Parameter '{k}' is out of bounds: {l} <= {p} <= {u}")

        return self.proto(self.coordination_number, parameters, self.cutoff(parameters), self.kernels, family=self, tag=tag)

    def __call__(self, *args, **kwargs):
        return self.instantiate(*args, **kwargs)

    def repr_potential(self, potential):
        """
        Represents potential.

        Parameters
        ----------
        potential : LocalPotential
            The potential.

        Returns
        -------
        result : str
            Representation string.
        """
        return repr_potential(potential, self.parameter_units)

    def instance_to_json(self, potential):
        """
        Represents an instance of this family as a JSON-compatible structure.

        Parameters
        ----------
        potential : LocalPotential
            A potential to represent.

        Returns
        -------
        result : dict
            Potential parameters and other information.
        """
        if self.tag is None:
            raise ValueError("No tag set for potential family")
        parameters = potential.get_all_parameters()
        if self.parameter_units is not None:
            parameters = self.parameter_units.apply(parameters)
        return dict(
            tag=self.tag,
            parameters=parameters,
            ptag=potential.tag,
        )

    @staticmethod
    def instance_from_json(data):
        """
        Restores a potential from its json representation.

        Parameters
        ----------
        data : dict
            A dict with JSON data.

        Returns
        -------
        result : LocalPotential
            The restored potential.
        """
        family = known_families[data["tag"]]
        parameters = data["parameters"]
        if family.parameter_units is not None:
            parameters = family.parameter_units.lift(parameters)
        return family.instantiate(**parameters, tag=data["ptag"])


def call_screened_raw(kernel, coordination_number, r_indptr, r_indices, r_data, cartesian_row, cartesian_col,
                      parameters, out, species_row=None, species_mask=None, **kwargs):
    """
    Wrapper for functions evaluating potentials and gradients.

    Parameters
    ----------
    kernel : Callable
        Function driver.
    coordination_number : int
        Coordination number of the driver.
    r_indptr : np.ndarray
        Index pointers of a sparse csr pair distance array.
    r_indices : np.ndarray
        Column indices of a sparse csr pair distance array.
    r_data : np.ndarray, None
        Pre-computed distances between atom pairs corresponding to the above indices.
        If None, it will be recomputed from the cartesian coordinates data.
    cartesian_row : np.ndarray
        Cartesian coordinates corresponding to row indices.
    cartesian_col : np.ndarray
        Cartesian coordinates corresponding to column indices.
    parameters : dict
        Potential parameters.
    out : np.ndarray
        Output array.
    species_row : np.ndarray
        Atomic species with coordinates `cartesian_row` encoded as integers.
    species_mask : np.ndarray
        A mask to apply to species: for example, an array with two integers corresponding
        to specimen Bi and Se for pair potential Bi-Se.
    kwargs
        Other keyword arguments to kernel functions.

    Returns
    -------
        Results of kernel computation.
    """
    if species_mask is None or species_row is None:
        species_row = np.zeros(len(r_indptr) - 1, dtype=np.int32)
        species_mask = np.zeros(coordination_number, dtype=np.int32)
    if r_data is None:
        r_data = calc_sparse_distances(r_indptr, r_indices, cartesian_row, cartesian_col)

    kernel(
        r_indptr, r_indices, r_data, cartesian_row, cartesian_col,
        **parameters, species_row=species_row, species_mask=species_mask, out=out,
        **kwargs
    )


def call_screened_csr(kernel, coordination_number, r, cartesian_row, cartesian_col,
                      parameters, out, species_row=None, species_mask=None, **kwargs):
    """
    Wrapper for functions evaluating potentials and gradients.

    Parameters
    ----------
    kernel : Callable
        Function kernel.
    coordination_number : int
        Coordination number of the driver.
    r : csr_matrix, np.ndarray
        CSR or dense matrix with distances.
    cartesian_row : np.ndarray
        Cartesian coordinates corresponding to row indices.
    cartesian_col : np.ndarray
        Cartesian coordinates corresponding to column indices.
    parameters : dict
        Potential parameters.
    out : np.ndarray
        Output array.
    species_row : np.ndarray
        Atomic species with coordinates `cartesian_row` encoded as integers.
    species_mask : np.ndarray
        A mask to apply to species: for example, an array with two integers corresponding
        to specimen Bi and Se for pair potential Bi-Se.
    kwargs
        Other keyword arguments to kernel functions.

    Returns
    -------
        Results of kernel computation.
    """
    if isinstance(r, np.ndarray):
        r = csr_matrix(r)
    call_screened_raw(kernel, coordination_number, r.indptr, r.indices, r.data, cartesian_row, cartesian_col,
                      parameters, out, species_row=species_row, species_mask=species_mask, **kwargs)


def shape_for_kernel(kname, n_atoms, n_coords=3, like=None):
    """
    Calculates shape of an array to receive the output of kernel functions.

    Parameters
    ----------
    kname : str
        The kernel name.
    n_atoms : int
        Atoms count.
    n_coords : int
        Coordinates count.
    like : dict
        A str: str mapping indicating kname entries
        to be associated with the existing ones.

    Returns
    -------
    out : tuple
        Array shape.
    """
    if like is not None:
        kname = like.get(kname, kname)
    if kname == "kernel":
        return n_atoms,
    elif kname == "kernel_gradient":
        return n_atoms, n_atoms, n_coords
    else:
        raise ValueError(f"Unknown kernel: '{kname}'")


def pre_compute_r(r, f_r, parameters):
    """
    Pre-computes r-dependent functions.

    Some potentials may partially share pre-computed functions to
    speed up computations. This function prepares a dense array
    of pre-computed distance-dependent functions.

    Parameters
    ----------
    r : np.ndarray
        A 1D array of distances.
    f_r : list
        A list of pairs of parameters and the corresponding functions.
    parameters : dict
        A dict with potential parameters.

    Returns
    -------
    result : np.ndarray
    """
    result = np.empty((len(r), len(f_r)), dtype=float)
    for i, (params, fun) in enumerate(f_r):
        param_values = {k: parameters[k] for k in params}
        result[:, i] = fun(r, **param_values)
    return result


class LocalPotential:
    def __init__(self, coordination_number, parameters, cutoff, kernels, family=None, tag=None):
        """
        Potential wrapper.

        Parameters
        ----------
        coordination_number : int
            The coordination number of potential.
        parameters : dict
            Potential parameters.
        cutoff : Callable
            Cutoff function.
        kernels : dict
            A dictionary with potential kernels.
        family : LocalPotentialFamily
            A family this potential belongs to.
        tag : str
            Optional tag.
        """
        self.coordination_number = coordination_number
        self.parameters = {k: (np.array(v) if isinstance(v, (list, tuple)) else v) for k, v in parameters.items()}
        self.cutoff = cutoff
        self.kernels = dict(kernels)
        self.family = family
        self.tag = tag

    def get_all_parameters(self):
        """
        Retrieves a copy of a dict with all potential parameters.

        Returns
        -------
        parameters : dict
            A dict with parameters.
        """
        return {k: v.tolist() if isinstance(v, np.ndarray) else v for k, v in self.parameters.items()}

    def get_kernel_by_name(self, kname, prefer_parallel=None):
        """This one is just for a more informative exception and parallel kernel picking."""
        if prefer_parallel is None:
            prefer_parallel = _prefer_parallel
        try:
            result = self.kernels[kname]
        except KeyError:
            raise KeyError(f"Missing kernel '{kname}'. Available kernels: {', '.join(sorted(self.kernels))}")
        if prefer_parallel:
            result_parallel = self.kernels.get(f"{kname}_parallel")
            if result_parallel is not None:
                return result_parallel
        return result

    @property
    def pre_compute_r_functions(self):
        if self.family is None:
            return None
        return self.family.pre_compute_r

    def pre_compute_r(self, r_data):
        """Pre-computes quantities for this potential."""
        if self.pre_compute_r_functions is None:
            raise ValueError("Nothing to pre-compute for this potential")
        return pre_compute_r(r_data, self.pre_compute_r_functions, self.parameters)

    def fun_csr_split(self, kname, r_indptr, r_indices, r_data, cartesian_row, cartesian_col, out=None,
                      species_row=None, species_mask=None, prefer_parallel=None, **kwargs):
        """CSR-split function adapter."""
        if out is None:
            out = np.zeros(shape_for_kernel(kname, len(cartesian_row)), dtype=float)
        if self.family is not None and self.family.pre_compute_r is not None and "pre_compute_r" not in kwargs:
            f_r = self.pre_compute_r(r_data)
            kwargs["pre_compute_r"] = f_r
            kwargs["pre_compute_r_handles"] = np.arange(f_r.shape[1], dtype=np.int32)
        call_screened_raw(self.get_kernel_by_name(kname, prefer_parallel=prefer_parallel), self.coordination_number,
                          r_indptr, r_indices, r_data, cartesian_row, cartesian_col, self.parameters, out, species_row,
                          species_mask, **kwargs)
        return out

    def fun_csr(self, kname, r, cartesian_row, cartesian_col, **kwargs):
        """CSR input function adapter."""
        if isinstance(r, np.ndarray):
            r = csr_matrix(r)
        return self.fun_csr_split(kname, r.indptr, r.indices, r.data, cartesian_row, cartesian_col, **kwargs)

    def __call__(self, kind, r, *args, **kwargs):
        if isinstance(r, tuple):
            assert len(r) == 3
            return self.fun_csr_split(kind, r[0], r[1], r[2], *args, **kwargs)
        if isinstance(r, (csr_matrix, np.ndarray)):
            return self.fun_csr(kind, r, *args, **kwargs)
        else:
            raise ValueError(f"Do not recognize argument type: {r}")

    def copy(self, tag=None):
        """
        A copy.

        Parameters
        ----------
        tag : str
            An optional new tag.

        Returns
        -------
            A copy of this potential.
        """
        if tag is None:
            tag = self.tag
        return self.__class__(self.coordination_number, self.get_all_parameters(), self.cutoff, self.kernels,
                              family=self.family, tag=tag)

    def __repr__(self):
        if self.family is not None:
            return self.family.repr_potential(self)
        else:
            return repr_potential(self)

    def to_json(self):
        """A JSON representation of the potential."""
        if self.family is None:
            raise ValueError("No family assigned to this potential")
        return self.family.instance_to_json(self)


class ScaledLocalPotential(LocalPotential):
    def __init__(self, coordination_number, parameters, cutoff, kernels, family=None, tag=None):
        """
        Potential with energy and length scale.

        Parameters
        ----------
        coordination_number : int
            The coordination number of potential.
        parameters : dict
            Potential parameters.
        cutoff : Callable
            Cutoff function.
        kernels : dict
            A dictionary with potential kernels.
        family : LocalPotentialFamily
            A family this potential belongs to.
        tag : str
            Optional tag.
        """
        if "epsilon" not in parameters or "sigma" not in parameters:
            raise ValueError(f"Missing either 'epsilon' or 'sigma' from parameters: {parameters}")
        self.epsilon = parameters.pop("epsilon")
        self.sigma = parameters.pop("sigma")
        self.__out_scale__ = dict(kernel=self.epsilon, kernel_gradient=self.epsilon / self.sigma)
        super().__init__(coordination_number, parameters, cutoff * self.sigma, kernels, family=family, tag=tag)

    def get_all_parameters(self):
        """
        Retrieves a copy of a dict with all potential parameters.

        Returns
        -------
        parameters : dict
            A dict with parameters.
        """
        return {"epsilon": self.epsilon, "sigma": self.sigma, **super().get_all_parameters()}

    def fun_csr_split(self, kname, r_indptr, r_indices, r_data, cartesian_row, cartesian_col, out=None,
                      species_row=None, species_mask=None, **kwargs):
        """CSR-split function adapter."""
        out = super().fun_csr_split(kname, r_indptr, r_indices, r_data / self.sigma if r_data is not None else None,
                                    cartesian_row / self.sigma, cartesian_col / self.sigma, out, species_row,
                                    species_mask, **kwargs)
        out *= self.__out_scale__[kname]
        return out

    def copy(self, tag=None):
        """
        A copy.

        Parameters
        ----------
        tag : str
            An optional new tag.

        Returns
        -------
            A copy of this potential.
        """
        if tag is None:
            tag = self.tag
        return self.__class__(self.coordination_number, self.get_all_parameters(), self.cutoff / self.sigma,
                              self.kernels, family=self.family, tag=tag)

    def __eq__(self, other):
        if not isinstance(other, ScaledLocalPotential):
            return False
        return self.sigma == other.sigma and self.epsilon == other.epsilon and super().__eq__(other)


def _get_potentials(name, parallel=True):
    """
    Retrieves potentials functions from `_potentials` module according to the following convention:

    * `kernel_{name}` for potential;
    * `kernel_g_{name}` for potential gradients;
    * `pkernel_{name}` for parallel implementation of potential, optional;
    * `pkernel_g_{name}` for parallel implementation of potential gradients, optional;

    Parameters
    ----------
    name : str
        The name of the potential.
    parallel : bool
        If True, adds parallel routines to the output.

    Returns
    -------
    result : dict
        The resulting dict of potentials.
    """
    result = dict(kernel=f"kernel_{name}", kernel_gradient=f"kernel_g_{name}")
    if parallel:
        result.update(dict(kernel_parallel=f"pkernel_{name}", kernel_gradient_parallel=f"pkernel_g_{name}"))
    return {k: getattr(_potentials, v) for k, v in result.items()}


general_pair_potential_family = LocalPotentialFamily(
    coordination_number=2,
    parameters=dict(f=None, df_dr=None, a=(0, np.inf)),
    cutoff="a",
    tag='general pair',
    **_get_potentials("general_2", parallel=False)
)
general_triple_potential_family = LocalPotentialFamily(
    coordination_number=3,
    parameters=dict(f=None, df_dr1=None, df_dr2=None, df_dt=None, a=(0, np.inf)),
    cutoff="a",
    tag='general triple',
    **_get_potentials("general_3", parallel=False)
)
on_site_potential_family = LocalPotentialFamily(
    coordination_number=1,
    parameters=dict(v0=(-np.inf, np.inf)),
    parameter_units=ParameterUnits(dict(v0="Ry")),
    cutoff=0,
    kernel=kernel_on_site,
    kernel_gradient=kernel_g_on_site,
    tag='on-site'
)
harmonic_repulsion_potential_family = LocalPotentialFamily(
    coordination_number=2,
    parameters=dict(a=(0, np.inf), epsilon=(0, np.inf)),
    parameter_units=ParameterUnits(dict(a="angstrom", epsilon="Ry")),
    cutoff="a",
    tag="harmonic repulsion",
    **_get_potentials("harmonic_repulsion")
)

atomic_units = ParameterUnits(dict(epsilon="Ry", sigma="angstrom"))
atomic_ranges = dict(epsilon=(0, np.inf), sigma=(0, np.inf))

lj_potential_family = LocalPotentialFamily(
    coordination_number=2,
    parameters=dict(**atomic_ranges, a=(2. ** (1. / 6), np.inf)),
    parameter_units=atomic_units,
    cutoff="a",
    tag="Lennard-Jones",
    proto=ScaledLocalPotential,
    **_get_potentials("lj")
)


class SW2PotentialFamily(LocalPotentialFamily):
    def instantiate(self, min_at=(2. ** (1. / 6), -1), tag=None, **kwargs):
        if not ("gauge_a" in kwargs and "gauge_b" in kwargs):
            sigma = kwargs.pop("sigma")
            epsilon = kwargs.pop("epsilon")
            min_x, min_y = min_at
            result = root_scalar(
                lambda x: self.__get_min__(dict(gauge_a=1, gauge_b=x, **kwargs)) - min_x,
                bracket=[1e-3, 3], method='bisect')
            gauge_b = result.root
            gauge_a = min_y / self.__scalar_target__(min_x, dict(gauge_a=1, gauge_b=gauge_b, **kwargs))
            kwargs = dict(gauge_a=gauge_a, gauge_b=gauge_b, **kwargs)
            kwargs["sigma"] = sigma
            kwargs["epsilon"] = epsilon
        return super().instantiate(tag=tag, **kwargs)

    def __scalar_target__(self, x, parameters, out=None):
        c = np.array([[0, 0, 0], [x, 0, 0]])
        d = np.array([[0, x], [0, 0]])
        if out is None:
            out = np.zeros(2, dtype=float)
        else:
            out[:] = 0
        call_screened_csr(self.kernels["kernel"], 2, d, c, c, parameters, out)
        return out[0]

    def __get_min__(self, parameters):
        """
        Finds potential minimum.

        Parameters
        ----------
        parameters : dict
            Potential parameters.

        Returns
        -------
        r : float
            Radius where the potential takes the minimum.
        """
        bounds = self.__get_min_search_bounds__(parameters)
        if bounds[0] >= bounds[1]:
            return float("nan")

        out_buffer = np.zeros(2, dtype=float)
        result = minimize_scalar(partial(self.__scalar_target__, parameters=parameters, out=out_buffer), bounds=bounds,
                                 method="bounded", options=dict(xatol=1e-13))

        if not result.success:
            raise RuntimeError("Failed to find a minimum")

        return result.x

    def __get_min_search_bounds__(self, parameters):
        """
        Bounds for finding the potential minimum.

        Parameters
        ----------
        parameters : dict
            Potential parameters.

        Returns
        -------
        bounds : tuple
            Lower and upper bounds.
        """
        return parameters["gauge_b"] ** (1. / (parameters["p"] - parameters["q"])), self.cutoff(parameters)


sw2_potential_family = SW2PotentialFamily(
    coordination_number=2,
    parameters=dict(**atomic_ranges, gauge_a=(0, np.inf), gauge_b=(0, np.inf), a=(1, np.inf), p=(1, np.inf),
                    q=(-np.inf, np.inf)),
    parameter_units=atomic_units,
    cutoff="a",
    tag="Stillinger-Weber type 2",
    proto=ScaledLocalPotential,
    **_get_potentials("sw_phi2")
)
sw3_potential_family = LocalPotentialFamily(
    coordination_number=3,
    parameters=dict(**atomic_ranges, l=(0, np.inf), gamma=(0, np.inf), cos_theta0=(-1, 1), a=(1, np.inf)),
    parameter_units=atomic_units,
    cutoff="a",
    tag="Stillinger-Weber type 3",
    proto=ScaledLocalPotential,
    **_get_potentials("sw_phi3")
)


def sine_cutoff_fn(r, a):
    return .5 + np.cos(np.pi * r / a) / 2


def sine_cutoff_fp(r, a):
    return - np.pi * np.sin(np.pi * r / a) / (a * 2)


def exp_fn(r, eta):
    return np.exp(- eta * r ** 2)


behler2_descriptor_family = LocalPotentialFamily(
    coordination_number=2,
    parameters=dict(a=(0, np.inf), eta=(0, np.inf), r_sphere=(0, np.inf)),
    parameter_units=ParameterUnits(dict(a="angstrom", eta="1/angstrom**2", r_sphere="angstrom")),
    cutoff="a",
    tag="Behler type 2",
    pre_compute_r=[sine_cutoff_fn, sine_cutoff_fp],
    **_get_potentials("mlsf_g2")
)
sigmoid_descriptor_family = LocalPotentialFamily(
    coordination_number=2,
    parameters=dict(a=(0, np.inf), dr=(0, np.inf), r0=(0, np.inf)),
    parameter_units=ParameterUnits(dict(a="angstrom", dr="angstrom", r0="angstrom")),
    cutoff="a",
    tag="Sigmoid",
    **_get_potentials("sigmoid")
)
behler5_descriptor_family = LocalPotentialFamily(
    coordination_number=3,
    parameters=dict(a=(0, np.inf), eta=(0, np.inf), l=(-1, 1), zeta=(0, np.inf)),
    parameter_units=ParameterUnits(dict(a="angstrom", eta="1/angstrom**2")),
    parameter_defaults=dict(epsilon=1),
    cutoff="a",
    tag="Behler type 5",
    pre_compute_r=[sine_cutoff_fn, sine_cutoff_fp, exp_fn],
    **_get_potentials("mlsf_g5")
)
behler4_descriptor_family = LocalPotentialFamily(
    coordination_number=3,
    parameters=dict(a=(0, np.inf), eta=(0, np.inf), l=(-1, 1), zeta=(0, np.inf)),
    parameter_units=ParameterUnits(dict(a="angstrom", eta="1/angstrom**2")),
    parameter_defaults=dict(epsilon=1),
    cutoff="a",
    tag="Behler type 4",
    pre_compute_r=[sine_cutoff_fn, sine_cutoff_fp, exp_fn],
    **_get_potentials("mlsf_g4")
)


def behler2_p2(r, a, eta, r_sphere):
    """
    Second derivative of the two-point Behler descriptor.

    Parameters
    ----------
    r : float, np.ndarray
        Radial point(s).
    a : float
    eta : float
    r_sphere : float
        Behler type 2 function parameters.

    Returns
    -------
    result : float, np.ndarray
        The second derivative of the two-point descriptor.
    """
    cutoff_fn = (np.cos(r * np.pi / a) + 1) / 2
    cutoff_fn_1 = - np.sin(r * np.pi / a) * np.pi / a / 2
    cutoff_fn_2 = - np.cos(r * np.pi / a) * (np.pi / a) ** 2 / 2

    gaussian = np.exp(- eta * (r - r_sphere) ** 2)
    gaussian_1 = - gaussian * eta * 2 * (r - r_sphere)
    gaussian_2 = - gaussian_1 * eta * 2 * (r - r_sphere) - gaussian * eta * 2

    return cutoff_fn * gaussian_2 + 2 * cutoff_fn_1 * gaussian_1 + cutoff_fn_2 * gaussian


def behler_turning_point(a, eta, r_sphere):
    """
    Searches for the turning point of the two-point Behler descriptor.

    Parameters
    ----------
    a : float
    eta : float
    r_sphere : float
        Behler type 2 function parameters.

    Returns
    -------
    result : float
        The turning point.
    """
    eta = eta * a ** 2
    r_sphere = r_sphere / a
    if eta == 0:
        return a / 2
    rbound = min(.5, 1 / (2 * eta) ** .5)
    return root_scalar(behler2_p2, (1, eta, r_sphere), bracket=[0, rbound], method='bisect').root * a


def _pre_compute_r_quantities(distances, potentials):
    """
    Pre-computes r-dependent quantities for a given set of potentials.

    Parameters
    ----------
    distances : np.ndarray
        Pair distances.
    potentials : list, tuple
        Potentials to process.

    Returns
    -------
    pre_compute_r_data : np.ndarray
        A rectangular matrix `[len(distances), len(r_quantities)]` with floating point r-dependent function values.
    pre_compute_r_handles : list
        A list of integer numpy arrays with entries corresponding to columns in `pre_compute_r_data`.
    """
    signatures = []
    signature_offsets = [0]
    for p in potentials:
        p_f_r = p.pre_compute_r_functions
        if p_f_r is None:
            signature_offsets.append(0)
        else:
            signatures += list(map(hash, (
                (parameters, tuple(p.parameters[k] for k in parameters), id(fun))
                for parameters, fun in p_f_r
            )))
            signature_offsets.append(len(p_f_r))
    signatures = np.array(signatures)
    signature_offsets = np.cumsum(signature_offsets)
    if len(signatures) > 0:
        unique_signatures, signatures = np.unique(signatures, return_inverse=True)
        signatures = signatures.astype(np.int32)
        pre_compute_r_data = np.empty((len(distances), len(unique_signatures)), dtype=float)
        pre_compute_r_handles = list(
            signatures[fr:to]
            for fr, to in zip(signature_offsets[:-1], signature_offsets[1:])
        )
        computed = set()
        for p, i_fr, i_to in zip(potentials, signature_offsets[:-1], signature_offsets[1:]):
            p_f_r = p.pre_compute_r_functions
            if p_f_r is not None:
                _signatures = signatures[i_fr:i_to]
                for fun_entry, s in zip(p_f_r, _signatures):
                    if s not in computed:
                        computed.add(s)
                        pre_compute_r_data[:, s:s+1] = pre_compute_r(distances, [fun_entry], p.parameters)
        return pre_compute_r_data, pre_compute_r_handles


# Parallelization:
# encoded_potentials : list, copy
# kname : str, copy
# sparse_pair_distances : array, R, shared
# cartesian_row : array, R, shared
# cartesian_col : array, R, shared
# spec_encoded_row : array, R, shared
# pre_compute_r : tuple of two arrays, R, shared
# cutoff : float, copy
# out : array, W, shared, distributed over the first index
def eval_potentials(encoded_potentials, kname, sparse_pair_distances, cartesian_row, cartesian_col, spec_encoded_row,
                    pre_compute_r=False, cutoff=None, out=None, **kwargs):
    """
    Calculates potentials: values, gradients and more.

    Parameters
    ----------
    encoded_potentials : list, LocalPotential
        A list of potentials or a single potential.
    kname : str, None
        Function to evaluate: 'kernel', 'kernel_gradient' or whatever
        other kernel function set for all potentials in the list.
    sparse_pair_distances : csr_matrix
        Pair distances.
    cartesian_row : np.ndarray
        Cartesian coordinates of atoms inside the cell.
    cartesian_col : np.ndarray
        Cartesian coordinates of surrounding atoms.
    spec_encoded_row : np.ndarray
        Species encoded as integers inside the unit cell.
    pre_compute_r : tuple
        Optional pre-computed r-dependent quantities for this set of potentials.
    cutoff : float
        Optional cutoff to check potentials againsst.
    out : np.ndarray
        The output buffer `[n_potentials, n_atoms]` for
        kname == "kernel" and `[n_potentials, n_atoms, n_atoms, 3]`
        for kname == "kernel_gradient". Any kind of reduction including
        `resolved=False` and calls `self.total`, `self.grad` calls will
        use the buffer for intermediate results but will still allocate
        a new array for the output.
    kwargs
        Other common arguments to kernel functions.

    Returns
    -------
    result : list, np.ndarray
        The result of the potential computation given the cell data.
    """
    if cutoff is not None:
        for p in encoded_potentials:
            if p.cutoff > cutoff:
                raise ValueError(f"Potential cutoff exceeds the computed neighbors: {p.cutoff} > {cutoff}\n"
                                 f"Potential: {p}")

    if pre_compute_r is False:
        pre_compute_r = _pre_compute_r_quantities(sparse_pair_distances.data, encoded_potentials)

    if out is None:
        out = np.zeros((len(encoded_potentials),) + shape_for_kernel(kname, len(cartesian_row)), dtype=float)

    for i, (destination, potential) in enumerate(zip(out, encoded_potentials)):
        if not isinstance(potential, LocalPotential):
            raise ValueError(f'Not a LocalPotential: {repr(potential)}')
        if not isinstance(potential.tag, np.ndarray):
            raise ValueError(f'Expected array for potential.tag, found: {repr(potential.tag)}')

        _kwargs = kwargs.copy()
        # Insert pre-computed data
        if pre_compute_r is not None:
            pre_compute_r_data, pre_compute_r_handles = pre_compute_r
            if potential.pre_compute_r_functions is not None:
                _kwargs["pre_compute_r"] = pre_compute_r_data
                _kwargs["pre_compute_r_handles"] = pre_compute_r_handles[i]

        potential.fun_csr(kname, sparse_pair_distances, cartesian_row, cartesian_col, species_row=spec_encoded_row,
                          species_mask=potential.tag, out=destination, **_kwargs)
    return out
