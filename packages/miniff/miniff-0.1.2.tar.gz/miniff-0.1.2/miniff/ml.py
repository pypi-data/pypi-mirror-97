from .potentials import LocalPotential, LocalPotentialFamily, PotentialRuntimeWarning, eval_potentials
from .util import masked_unique, ParameterUnits

from typing import Tuple
import torch
import numpy as np
from scipy.sparse import csr_matrix
from functools import wraps, partial
from warnings import warn


def collect_atoms(cells):
    """
    Collects all atoms from all cells into a masked array.

    Parameters
    ----------
    cells : tuple
        Cells to process.

    Returns
    -------
    values : np.ma.masked_array
        An `[n_samples, n_atoms]` matrix with atoms.
    """
    # Work-around for varying string sizes in dtype
    max_dtype_size = max(i.cell.values.dtype.itemsize for i in cells)
    dtype = np.dtype(('U', max_dtype_size // np.dtype('U1').itemsize))

    max_cell_size = max(i.cell.size for i in cells)
    values = np.zeros((len(cells), max_cell_size), dtype=dtype)
    mask = np.ones_like(values, dtype=bool)
    for i_c, c in enumerate(cells):
        values[i_c, :c.size] = c.cell.values
        mask[i_c, :c.size] = 0
    return np.ma.masked_array(values, mask)


def encode_species(values):
    """
    Encodes species into integers.

    Parameters
    ----------
    values : tuple, np.ndarray
        An `[n_samples, n_atoms]` matrix with atoms or a
        collection of cells to process with `collect_atoms`.

    Returns
    -------
    values_torch : torch.tensor
        An `[n_samples, n_atoms]` torch matrix with integers
        encoding species.
    key : np.ndarray
        A 1D array with the key to values_torch.
    """
    if not isinstance(values, np.ndarray):
        values = collect_atoms(values)
    key, values_ = masked_unique(values, return_inverse=True, fill_value=-1)
    values_.shape = values.shape
    torch_values = torch.from_numpy(values_)
    return torch_values, key


def collect_meta(field, cells, out, mask=None):
    """
    Collects cell metadata into a tensor.

    Parameters
    ----------
    field : str
        The field to collect.
    cells : Iterable
        `NeighborWrapper`s or `UnitCell`s to process.
    out : torch.Tensor
        The output tensor.
    mask : np.ndarray
        An optional mask array for a particular specimen.

    Returns
    -------
    out : torch.Tensor
        A `[n_samples, *]` tensor with floats per each cell.
    """
    for i_c, c in enumerate(cells):
        d = c.meta[field]
        if not isinstance(d, np.ndarray):
            d = np.array(d)
        if mask is not None:
            d = d[mask[i_c, :len(d)], ...]
        if d.size > 0:
            d_slice = tuple(slice(0, i) for i in d.shape)
            out[(i_c, *d_slice)] = torch.tensor(d)
    return out


collect_energies = partial(collect_meta, "total-energy")
collect_forces = partial(collect_meta, "forces")
collect_charges = partial(collect_meta, "charges")
collect_partial_energies = partial(collect_meta, "partial-energy")


def prepare_descriptor_data(cells, descriptors, specimen, values, grad=False, dtype=torch.float64, **kwargs):
    """
    Computes descriptors of a unit cell dataset.

    This function prepares dense datasets suitable for
    operations during machine learning.

    Parameters
    ----------
    cells : Iterable
        `NeighborWrapper`s to process.
    descriptors : Iterable
        Pairs of descriptor targets (e.g. 'cu-cu') and lists of descriptors.
    specimen
        The specimen this dataset is calculated for.
    values : torch.Tensor
        A matrix `[n_samples, n_atoms]` with encoded species.
    grad : bool
        Include gradients.
    dtype : torch.dtype
        Data type of the output.
    kwargs
        Additional arguments to `NeighborWrapper.eval``.

    Returns
    -------
    descriptors : torch.Tensor
        A `[n_samples, n_species, n_descriptors]` tensor with descriptors.
    mask : torch.Tensor
        A `[n_samples, n_species]` mask array indicating meaningful entries.
    descriptor_gradients : torch.Tensor, optional
        A `[n_samples, n_species, n_descriptors, n_atoms, 3]` tensor
        with descriptor gradients if gradients requested.
    """
    n_species = (values == specimen).sum(axis=1)
    n_species_max = n_species.max().item()
    n_atoms_max = values.shape[1]

    values_mask = values == specimen

    result_descriptors = torch.zeros(len(cells), n_species_max, len(descriptors), dtype=dtype)
    buffer_descriptors = torch.zeros(len(descriptors), n_atoms_max, dtype=dtype)
    buffer_descriptors_np = buffer_descriptors.numpy()
    if grad:
        result_grad = torch.zeros(len(cells), n_species_max, len(descriptors), values.shape[1], 3, dtype=dtype)
        buffer_grad = torch.zeros(len(descriptors), n_atoms_max, n_atoms_max, 3, dtype=dtype)
        buffer_grad_np = buffer_grad.numpy()

    mask = torch.zeros(len(cells), n_species_max, dtype=dtype)

    for i_c, (c, s) in enumerate(zip(cells, n_species)):
        mask[i_c, :s] = 1
        buffer_descriptors.zero_()
        c.eval(descriptors, "kernel", resolved=True, ignore_missing_species=True, out=buffer_descriptors_np, **kwargs)
        result_descriptors[i_c, :s] = buffer_descriptors.transpose(0, 1)[values_mask[i_c], ...]
        if grad:
            buffer_grad.zero_()
            c.eval(descriptors, "kernel_gradient", resolved=True, ignore_missing_species=True, out=buffer_grad_np)
            result_grad[i_c, :s, :, :c.size] = buffer_grad.transpose(0, 1)[values_mask[i_c], :, :c.size]

    if grad:
        return result_descriptors, mask, result_grad
    else:
        return result_descriptors, mask


def __assert_same_dtype__(data, *keys, dtype=None):
    for n in keys:
        if data[n] is None:
            continue
        if not isinstance(data[n], torch.Tensor):
            raise ValueError(f"Not a tensor: {n} = {repr(data[n])}")
        if dtype is not None and data[n].dtype != dtype:
            raise ValueError(f"Data type mismatch: {n}.dtype = {data[n].dtype} != {dtype}")
        dtype = data[n].dtype
    return dtype


def __assert_dimension_count__(data, *keys):
    if len(keys) % 2:
        raise RuntimeError("Odd argument count")
    dim_i = keys[1::2]
    keys = keys[::2]
    for n, i in zip(keys, dim_i):
        if n not in data or data[n] is None:
            continue
        if data[n].ndim != i:
            raise ValueError(f"Unexpected dimension count: {n}.ndim = {data[n].ndim:d} != {i:d}")


def __assert_same_dimension__(data, name, *keys, size=None):
    if len(keys) % 2:
        raise RuntimeError("Odd argument count")
    dim_i = keys[1::2]
    keys = keys[::2]
    for n, i in zip(keys, dim_i):
        if n not in data or data[n] is None:
            continue
        if size is not None and data[n].shape[i] != size:
            raise ValueError(f"Inconsistent dimensions: {n}.shape[{i:d}] = {data[n].shape[i]:d} != {name} = {size:d}")
        size = data[n].shape[i]
    return size


def __assert_same_len__(data, *keys):
    l = len(data[keys[0]])
    for k in keys:
        if len(data[k]) != l:
            raise ValueError(f"Inconsistent length: len({k}) = {len(data[k]):d} != {l:d}")
    return l


def __maybe_to__(tensor, dtype):
    if tensor is not None:
        return tensor.to(dtype)
    else:
        return None


def same(items):
    """'Same' reduction: asserts all items are equal to the return value."""
    items = set(items)
    assert len(items) == 1
    return items.pop()


def __maybe_cat__(tensors, free_dims=None):
    if all(i is None for i in tensors):
        return None
    if free_dims is None:
        free_dims = tuple()
    if isinstance(free_dims, int):
        free_dims = free_dims,
    if len(free_dims) == 0:
        return torch.cat(tensors)

    ndims = same(i.ndim for i in tensors)
    dtype = same(i.dtype for i in tensors)
    final_dims = []
    for i in range(0, ndims):
        if i == 0:
            reduction = sum
        elif i not in free_dims:
            reduction = same
        else:
            reduction = max
        final_dims.append(reduction(t.shape[i] for t in tensors))

    result = torch.zeros(*final_dims, dtype=dtype)
    offset = 0
    for i in tensors:
        result[(slice(offset, offset + len(i)),) + tuple(slice(0, d) for d in i.shape[1:])] = i
        offset += len(i)
    return result


class NoneTolerantTensorDataset(torch.utils.data.Dataset):
    def __init__(self, *tensors):
        self.tensors = tensors
        assert all(self.__sample__.size(0) == tensor.size(0) for tensor in tensors if tensor is not None)

    @property
    def __sample__(self):
        for i in self.tensors:
            if i is not None:
                return i
        raise ValueError("All tensors are None")

    def __getitem__(self, index):
        return tuple(tensor[index] if tensor is not None else tensor for tensor in self.tensors)

    def __len__(self):
        return self.__sample__.size(0)


class PerCellDataset(NoneTolerantTensorDataset):
    def __init__(self, energy, mask=None, energy_g=None):
        """
        A dataset with total energies and gradients defined per unit cell.

        Parameters
        ----------
        energy : torch.Tensor
            A 2D tensor of shape `[n_samples, 1]` with total energies per unit cell.
        mask : torch.Tensor
            A 2D mask tensor of shape `[n_samples, n_atoms]` indicating meaningful
            gradient, charges and other "per-atom" entries.
        energy_g : torch.Tensor
            An `[n_samples, n_atoms, 3]` tensor with total energy gradients.
        """
        if energy_g is not None and mask is None:
            raise ValueError("Mask is required for energy_g")
        if energy_g is None:
            mask = None
        inputs = locals()

        self.dtype = __assert_same_dtype__(inputs, "energy", "energy_g")
        # TODO: check mask dtype
        __assert_dimension_count__(inputs, "energy", 2, "energy_g", 3, "mask", 2)
        self.n_samples = __assert_same_dimension__(inputs, "n_samples", "energy", 0, "energy_g", 0, "mask", 0)
        self.n_atoms = __assert_same_dimension__(inputs, "n_atoms", "energy_g", 1, "mask", 1)
        self.n_coords = __assert_same_dimension__(inputs, "n_coords", "energy_g", 2)
        __assert_same_dimension__(inputs, "[one]", "energy", 1, size=1)

        super(PerCellDataset, self).__init__(energy, mask, energy_g)

    @property
    def energy(self) -> torch.Tensor:
        return self.tensors[0]

    @property
    def mask(self) -> torch.Tensor:
        return self.tensors[1]

    @property
    def energy_g(self) -> torch.Tensor:
        return self.tensors[2]

    def is_gradient_available(self) -> bool:
        """Determines whether energy gradients data is present."""
        return self.energy_g is not None

    @staticmethod
    def from_cells(cells, values, grad=False, **kwargs):
        """
        Prepares a per-cell dataset with total energies
        and energy gradients.

        Parameters
        ----------
        cells : Iterable
            Cells to process.
        values : torch.Tensor
            A matrix `[n_samples, n_atoms]` with encoded species.
        grad : bool
            Include gradients.
        kwargs
            Arguments to empty tensor construction.

        Returns
        -------
        result : PerCellDataset
            The resulting dataset.
        """
        kwargs["dtype"] = kwargs.pop("dtype", torch.float64)  # TODO: get rid of this and other default dtypes
        return PerCellDataset(
            energy=collect_energies(cells, torch.zeros(len(values), 1, **kwargs)),
            mask=values,
            energy_g=-collect_forces(cells, torch.zeros(*values.shape, 3, **kwargs)) if grad else None,
        )

    @staticmethod
    def assert_compatible(items):
        """
        Checks whether input datasets are compatible to be merged into one.

        Parameters
        ----------
        items : list, tuple
            Items to merge.

        Returns
        -------
        n_samples : int
        n_atoms : int
        n_coords : int
        dtype : torch.dtype
            Resulting dataset dimensions and dtype.
        """
        assert len(items)

        # Dimensions and dtype
        n_samples = sum(i.n_samples for i in items)
        if all(i.n_atoms is None for i in items):
            n_atoms = None
        else:
            n_atoms = max(i.n_atoms for i in items)
        n_coords = same(i.n_coords for i in items)
        dtype = same(i.dtype for i in items)
        return n_samples, n_atoms, n_coords, dtype

    @staticmethod
    def cat(items):
        """
        Merges multiple datasets into a single one.

        Parameters
        ----------
        items : list, tuple
            Items to merge.

        Returns
        -------
        result : PerCellDataset
            The resulting contiguous dataset.
        """
        PerCellDataset.assert_compatible(items)
        args = {}

        def _cat(name, **kwargs):
            args[name] = __maybe_cat__(tuple(getattr(i, name) for i in items), **kwargs)

        _cat("energy")
        _cat("energy_g", free_dims=1)
        _cat("mask", free_dims=1)

        return PerCellDataset(**args)

    def to(self, dtype):
        """
        Converts this dataset to the provided type.

        Parameters
        ----------
        dtype
            The data type to convert to.

        Returns
        -------
        result : PerCellDataset
            The dataset of the given type.
        """
        if self.dtype == dtype:
            return self
        return self.__class__(*tuple(i.to(dtype) if i is not None else i for i in self.tensors))


class PerPointDataset(NoneTolerantTensorDataset):
    def __init__(self, features, mask, features_g=None, charges=None, energies_p=None, tag=None):
        """
        A dataset with descriptors defined per specimen.

        Parameters
        ----------
        features : torch.Tensor
            A 3D tensor of shape `[n_samples, n_species, n_descriptors]` with
            descriptor values.
        mask : torch.Tensor
            A 2D mask tensor of shape `[n_samples, n_species]` indicating
            meaningful descriptor entries.
        features_g : torch.Tensor
            A 5D tensor of shape `[n_samples, n_species, n_descriptors, n_atoms, n_coords]`
            with descriptor gradients per each point ∂D_i / ∂r_j. Descriptor index `i` is
            identified by dimensions 0, 1, 2 `[n_samples, n_species, n_descriptors]`;
            coordinate index `j` is identified by dimensions 0, 3, 4
            `[n_samples, n_atoms, n_coords]`.
        charges : torch.Tensor
            An `[n_samples, n_species]` tensor with charges for all atoms of the same type.
        energies_p : torch.Tensor
            An `[n_samples, n_species]` tensor with per-atom energy contributions.
        tag
            An optional tag for this dataset.
        """
        inputs = locals()

        self.dtype = __assert_same_dtype__(inputs, "features", "features_g", "mask", "charges", "energies_p")
        __assert_dimension_count__(inputs, "features", 3, "features_g", 5, "mask", 2, "charges", 3, "energies_p", 3)
        self.n_samples = __assert_same_dimension__(inputs, "n_samples", "features", 0, "features_g", 0, "mask", 0,
                                                   "charges", 0, "energies_p", 0)
        self.n_atoms = __assert_same_dimension__(inputs, "n_atoms", "features_g", 3)
        self.n_species = __assert_same_dimension__(inputs, "n_species", "features", 1, "features_g", 1, "mask", 1,
                                                   "charges", 1, "energies_p", 1)
        self.n_features = __assert_same_dimension__(inputs, "n_descriptors", "features", 2, "features_g", 2)
        self.n_coords = __assert_same_dimension__(inputs, "n_coords", "features_g", 4)
        __assert_same_dimension__(inputs, "[one]", "charges", 2, "energies_p", 2, size=1)

        self.tag = tag
        super().__init__(features, mask, features_g, charges, energies_p)

    @property
    def features(self) -> torch.Tensor:
        return self.tensors[0]

    @property
    def mask(self) -> torch.Tensor:
        return self.tensors[1]

    @property
    def features_g(self) -> torch.Tensor:
        return self.tensors[2]

    @property
    def charges(self) -> torch.Tensor:
        return self.tensors[3]

    @property
    def energies_p(self) -> torch.Tensor:
        return self.tensors[4]

    def is_gradient_available(self) -> bool:
        """Determines whether features gradients data is present."""
        return self.features_g is not None

    @staticmethod
    def from_cells(cells, descriptors, specimen, values, grad=False, charge=False, energies_p=False, tag=None,
                   dtype=torch.float64, **kwargs):
        """
        Prepares a per-point dataset with total features, feature gradients, energy gradients and partial energies.

        Parameters
        ----------
        cells : Iterable
            `NeighborWrapper`s to process.
        descriptors : list
            A plain list of tagged descriptors.
        specimen
            The specimen this dataset is calculated for.
        values : torch.Tensor
            A matrix `[n_samples, n_atoms]` with encoded species.
        grad : bool
            Include gradients.
        charge : bool
            Include atomic charges.
        energies_p : bool
            Include partial energies.
        tag
            Optional tag for the dataset.
        dtype
            Tensor data type.
        kwargs
            Additional arguments to `prepare_descriptor_data`.

        Returns
        -------
        result : PerPointDataset
            The resulting dataset.
        """
        d_data = prepare_descriptor_data(cells, descriptors, specimen, values, grad=grad, dtype=dtype, **kwargs)
        mask = d_data[1]
        mask_in = values == specimen
        return PerPointDataset(
            *d_data,
            charges=collect_charges(
                cells,
                torch.zeros(*mask.shape, dtype=dtype),
                mask=mask_in,
            ).unsqueeze(2) if charge else None,
            energies_p=collect_partial_energies(
                cells,
                torch.zeros(*mask.shape, dtype=dtype),
                mask=mask_in,
            ).unsqueeze(2) if energies_p else None,
            tag=tag)

    @staticmethod
    def assert_compatible(items):
        """
        Checks whether input datasets are compatible to be merged into one.

        Parameters
        ----------
        items : list, tuple
            Items to merge.

        Returns
        -------
        n_samples : int
        n_atoms : int
        n_species : int
        n_features : int
        n_coords : int
        dtype : torch.dtype
            Resulting dataset dimensions and dtype.
        """
        n_samples, n_atoms, n_coords, dtype = PerCellDataset.assert_compatible(items)
        n_species = max(i.n_species for i in items)
        n_features = same(i.n_features for i in items)
        return n_samples, n_atoms, n_species, n_features, n_coords, dtype

    @staticmethod
    def cat(items):
        """
        Merges multiple datasets into a single one.

        Parameters
        ----------
        items : list, tuple
            Items to merge.

        Returns
        -------
        result : PerPointDataset
            The resulting contiguous dataset.
        """
        PerPointDataset.assert_compatible(items)
        args = {}

        def _cat(name, **kwargs):
            args[name] = __maybe_cat__(tuple(getattr(i, name) for i in items), **kwargs)

        _cat("features", free_dims=1)
        _cat("mask", free_dims=1)
        _cat("features_g", free_dims=(1, 3))
        _cat("charges", free_dims=1)
        _cat("energies_p", free_dims=1)

        return PerPointDataset(**args)

    def to(self, dtype):
        """
        Converts this dataset to the provided type.

        Parameters
        ----------
        dtype
            The data type to convert to.

        Returns
        -------
        result : PerPointDataset
            The dataset of the given type.
        """
        if self.dtype == dtype:
            return self
        return self.__class__(
            features=self.features.to(dtype),
            mask=self.mask.to(dtype) if self.mask is not None else None,
            features_g=self.features_g.to(dtype) if self.features_g is not None else None,
            charges=self.charges.to(dtype) if self.charges is not None else None,
            energies_p=self.energies_p.to(dtype) if self.energies_p is not None else None,
            tag=self.tag
        )


class MergedDataset(torch.utils.data.Dataset):
    def __init__(self, *datasets):
        """
        A dataset consisting of several datasets side-by-side.

        Parameters
        ----------
        datasets
            Datasets to merge.
        """
        assert all(len(datasets[0]) == len(dataset) for dataset in datasets)
        self.datasets = tuple(datasets)

    def __getitem__(self, index):
        return tuple(dataset[index] for dataset in self.datasets)

    def __len__(self):
        return len(self.datasets[0])

    def to(self, dtype):
        """
        Converts this dataset to the provided type.

        Parameters
        ----------
        dtype
            The data type to convert to.

        Returns
        -------
        result : MergedDataset
            The dataset of the given type.
        """
        if self.dtype == dtype:
            return self
        return self.__class__(*tuple(i.to(dtype) for i in self.datasets))


class Dataset(MergedDataset):
    def __init__(self, per_cell_dataset, *per_point_datasets):
        """
        A dataset with energy, features and gradients data.

        Parameters
        ----------
        per_cell_dataset : PerCellDataset
            Energies per unit cell dataset.
        per_point_datasets
            Per-point datasets for each specimen.
        """
        for i in per_point_datasets:
            for field in "dtype", "n_samples", "n_atoms", "n_coords":
                f_pc = getattr(per_cell_dataset, field)
                f_pp = getattr(i, field)
                if f_pc is not None and f_pp is not None and f_pc != f_pp:
                    raise ValueError(f"per_point_dataset[tag={i.tag}].{field} = {f_pp} "
                                     f"!= per_cell_dataset.{field} = {f_pc}")

        super().__init__(per_cell_dataset, *per_point_datasets)

    @property
    def dtype(self):
        return self.per_cell_dataset.dtype

    @property
    def per_cell_dataset(self) -> PerCellDataset:
        return self.datasets[0]

    @property
    def per_point_datasets(self) -> Tuple[PerPointDataset, ...]:
        return self.datasets[1:]

    @staticmethod
    def from_tensors(tensors):
        """
        Constructs a dataset from nested tensor structure.

        Parameters
        ----------
        tensors : list, tuple
            Tensors (energy, features, etc).

        Returns
        -------
        dataset : Dataset
            The resulting dataset.
        """
        return Dataset(
            PerCellDataset(*tensors[0]),
            *tuple(PerPointDataset(*i) for i in tensors[1:])
        )

    @staticmethod
    def assert_compatible(items):
        """
        Checks whether input datasets are compatible to be merged into one.

        Parameters
        ----------
        items : list, tuple
            Items to merge.

        Returns
        -------
        n_samples : int
        n_atoms : int
        n_species : tuple
        n_features : tuple
        n_coords : int
        dtype : torch.dtype
            Resulting dataset dimensions and dtype.
        """
        n_samples, n_atoms, n_coords, dtype = PerCellDataset.assert_compatible(tuple(i.per_cell_dataset for i in items))
        same(len(i.per_point_datasets) for i in items)  # check species count to be the same
        n_species = []
        n_features = []
        for i in zip(*tuple(d.per_point_datasets for d in items)):
            _, _, _n_species, _n_features, _, _ = PerPointDataset.assert_compatible(i)
            n_species.append(_n_species)
            n_features.append(_n_features)
        return n_samples, n_atoms, tuple(n_species), tuple(n_features), n_coords, dtype

    @staticmethod
    def cat(items):
        """
        Merges multiple datasets into a single one.

        Parameters
        ----------
        items : list, tuple
            Items to merge.

        Returns
        -------
        result : Dataset
            The resulting contiguous dataset.
        """
        Dataset.assert_compatible(items)
        pcd = PerCellDataset.cat(tuple(i.per_cell_dataset for i in items))
        ppd = []
        for i in zip(*tuple(d.per_point_datasets for d in items)):
            ppd.append(PerPointDataset.cat(i))
        return Dataset(pcd, *ppd)


def inplace_options(f):
    """
    Decorates functions accepting inplace options only towards making a copy.

    Parameters
    ----------
    f : Callable
        A function to decorate.

    Returns
    -------
    result : Callable
        The decorated function.
    """
    @wraps(f)
    def _f(self, tensor, *secondary_arguments, inplace=False):
        if not inplace:
            tensor = tensor.clone()
        f(self, tensor, *secondary_arguments)
        return tensor
    return _f


def __default__(value, default_value):
    return value if value is not None else default_value


def __gentle_inverse__(m: torch.Tensor):
    # assumes m is a product of a scale vector s_i and truncated basis V_ij:
    # m = s_i V_ij
    # sum_j V_ij ^ 2 = 1
    # sum_j m_ij ^ 2 = s_i^2
    s2 = (m ** 2).sum(1)
    return m.T / s2[None, :]


class Normalization:
    def __init__(self, energy_scale, features_scale, energy_offsets, features_offsets, length_scale=None,
                 charges_scale=None, charges_offsets=None):
        """
        A simple normalization for individual features.

        Energy is rescaled and shifted based on atomic composition.
        Energy gradients are rescaled by a factor.
        Features are rescaled and shifted.
        Feature gradients are rescaled accordingly.

        Parameters
        ----------
        energy_scale : torch.Tensor
        features_scale : list, tuple
            Energy and features scales.
        energy_offsets : torch.Tensor
        features_offsets : list, tuple
            Offsets for energies (per specimen) and features (per feature).
        length_scale : torch.Tensor
            Length scale.
        charges_scale : list, tuple
        charges_offsets : list, tuple
            Charges scales and offsets per specimen.
        """
        features_offsets = tuple(features_offsets)
        features_scale = tuple(torch.diag(i) if i.ndim == 1 else i for i in features_scale)
        if charges_scale is not None:
            charges_scale = tuple(charges_scale)
        if charges_offsets is not None:
            charges_offsets = tuple(charges_offsets)
        if (charges_scale is not None and charges_offsets is None) or\
           (charges_scale is None and charges_offsets is not None):
            charges_scale = charges_offsets = None
        inputs = locals()
        inputs_d = {}
        for name in "features_offsets", "features_scale", "charges_offsets", "charges_scale":
            if inputs[name] is None:
                inputs_d[name] = None
            else:
                inputs_d[name] = {f"{name}[{i}]": v for i, v in enumerate(inputs[name])}

        dtype = __assert_same_dtype__(inputs, "energy_scale", "energy_offsets")
        __assert_dimension_count__(inputs, "energy_scale", 0, "energy_offsets", 2)
        __assert_same_dimension__(inputs, "[one]", "energy_offsets", 1, size=1)
        __assert_same_len__(inputs, "features_scale", "energy_offsets", "features_offsets")

        for name, v in sorted(inputs_d.items()):
            if v is not None:
                __assert_same_dtype__(v, *sorted(v.keys()), dtype=dtype)

        for name, ndim in ("features_offsets", 1), ("features_scale", 2):
            v = inputs_d[name]
            __assert_dimension_count__(v, *sum(((i, ndim) for i in sorted(v.keys())), ()))

        for name in "charges_offsets", "charges_scale":
            v = inputs_d[name]
            if v is not None:
                __assert_dimension_count__(v, *sum(((i, 0) for i in sorted(v.keys())), ()))

        for (n1, t1), (n2, t2) in zip(
                sorted(inputs_d["features_scale"].items()),
                sorted(inputs_d["features_offsets"].items()),
        ):
            __assert_same_dimension__({n1: t1, n2: t2}, "n_features", n1, 1, n2, 0)

        if length_scale is not None:
            __assert_dimension_count__(inputs, "length_scale", 0)
            dtype = __assert_same_dtype__(inputs, "length_scale", dtype=dtype)

        self.energy_scale = energy_scale
        self.features_scale = features_scale
        self.energy_offsets = energy_offsets
        self.features_offsets = features_offsets
        self.length_scale = length_scale
        self.charges_scale = charges_scale
        self.charges_offsets = charges_offsets

        self.dtype = dtype

    def is_gradient_available(self) -> bool:
        """Determines whether gradient normalization data is present."""
        return self.length_scale is not None

    def to(self, dtype):
        """
        Converts this normalization to the provided type.

        Parameters
        ----------
        dtype
            The data type to convert to.

        Returns
        -------
        result : Normalization
            The normalization of the given type.
        """
        if dtype == self.dtype:
            return self
        return Normalization(
            self.energy_scale.to(dtype),
            tuple(i.to(dtype) for i in self.features_scale),
            self.energy_offsets.to(dtype),
            tuple(i.to(dtype) for i in self.features_offsets),
            __maybe_to__(self.length_scale, dtype),
        )

    def state_dict(self):
        """
        Returns a dict of parameters describing this normalization.
        No copies are made.

        Returns
        -------
        params : dict
            A dict of parameters.
        """
        return dict(energy_scale=self.energy_scale, features_scale=self.features_scale,
                    energy_offsets=self.energy_offsets, features_offsets=self.features_offsets,
                    length_scale=self.length_scale)

    def load_state_dict(self, d):
        """
        Loads state dictionary.

        Parameters
        ----------
        d : dict
            Dictionary to load.
        """
        self.__init__(**d)

    def __repr__(self):
        return f"{self.__class__.__name__}(energy_scale={self.energy_scale}, " \
               f"features_scale={self.features_scale}, energy_offset={self.energy_offsets}, " \
               f"features_offset={self.features_offsets}, length_scale={self.length_scale})"

    @inplace_options
    def fw_energy_components(self, energy, specimen):
        """
        Rescales energy per-atom components.

        Parameters
        ----------
        energy : torch.Tensor
            Energy to rescale.
        specimen : int
            The index of the dataset energies belong to (specimen index).
        """
        energy -= self.energy_offsets[specimen]
        energy /= self.energy_scale

    @inplace_options
    def bw_energy_components(self, energy, specimen):
        """
        Rescales energy per-atom components back to their original values.

        Parameters
        ----------
        energy : torch.Tensor
            Energy to rescale.
        specimen : int
            The index of the dataset energies belong to (specimen index).
        """
        energy *= self.energy_scale
        energy += self.energy_offsets[specimen]

    @inplace_options
    def fw_energy(self, energy, atom_counts):
        """
        Rescales the energy.

        Parameters
        ----------
        energy : torch.Tensor
            Energy to rescale.
        atom_counts : torch.Tensor
            A 2D matrix with atom counts per cell.
        """
        energy -= atom_counts @ self.energy_offsets
        energy /= self.energy_scale

    @inplace_options
    def bw_energy(self, energy, atom_counts):
        """
        Rescales the energy back to its original values.

        Parameters
        ----------
        energy : torch.Tensor
            Energy to rescale.
        atom_counts : torch.Tensor
            A 2D matrix with atom counts per cell.
        """
        energy *= self.energy_scale
        energy += atom_counts @ self.energy_offsets

    @inplace_options
    def fw_energy_g(self, energy_g):
        """
        Rescales the energy gradients.

        Parameters
        ----------
        energy_g : torch.Tensor
            Energy gradients to rescale.
        """
        energy_g /= (self.energy_scale / __default__(self.length_scale, 1))

    @inplace_options
    def bw_energy_g(self, energy_g):
        """
        Rescales the energy gradients back to their original values.

        Parameters
        ----------
        energy_g : torch.Tensor
            Energy gradients to rescale.
        """
        energy_g *= (self.energy_scale / __default__(self.length_scale, 1))

    @inplace_options
    def fw_features(self, features, specimen):
        """
        Rescales features.

        Parameters
        ----------
        features : torch.Tensor
            Features to rescale.
        specimen : int
            The index of the dataset gradients belong to (specimen index).
        """
        features -= self.features_offsets[specimen][None, None, :]
        features.data = features @ __gentle_inverse__(self.features_scale[specimen])

    @inplace_options
    def bw_features(self, features, specimen):
        """
        Rescales features back to their original values.

        Parameters
        ----------
        features : torch.Tensor
            Features to rescale.
        specimen : int
            The index of the dataset gradients belong to.
        """
        features.data = features @ self.features_scale[specimen]
        features += self.features_offsets[specimen][None, None, :]

    @inplace_options
    def fw_features_g(self, features_g, specimen):
        """
        Rescales features' gradients.

        Parameters
        ----------
        features_g : torch.Tensor
            Features' gradients to rescale.
        specimen : int
            The index of the dataset gradients belong to.
        """
        inverse_scale = __gentle_inverse__(self.features_scale[specimen])
        if features_g.numel() == 0:  # torch.einsum is not capable of handling empty tensors
            i, j, _a, k, l = features_g.shape
            a, b = inverse_scale.shape
            assert a == _a
            features_g.data = torch.empty(i, j, b, k, l, dtype=features_g.dtype)
        else:
            features_g.data = torch.einsum("ijakl,ab->ijbkl", features_g, inverse_scale) * __default__(self.length_scale, 1)

    @inplace_options
    def bw_features_g(self, features_g, specimen):
        """
        Rescales features' gradients back to their original values.

        Parameters
        ----------
        features_g : torch.Tensor
            Features' gradients to rescale.
        specimen : int
            The index of the dataset gradients belong to.
        """
        if features_g.numel() == 0:  # torch.einsum is not capable of handling empty tensors
            i, j, _a, k, l = features_g.shape
            a, b = self.features_scale[specimen].shape
            assert a == _a
            features_g.data = torch.empty(i, j, b, k, l, dtype=features_g.dtype)
        else:
            features_g.data = torch.einsum(
                "ijakl,ab->ijbkl", features_g,
                self.features_scale[specimen],
            ) / __default__(self.length_scale, 1)

    @inplace_options
    def fw_charges(self, charges, specimen):
        """
        Rescales charges.

        Parameters
        ----------
        charges : torch.Tensor
            Charges to rescale.
        specimen : int
            The index of the dataset charges belong to.
        """
        charges -= __default__(self.charges_offsets[specimen], 1)
        charges /= __default__(self.charges_scale[specimen], 1)

    @inplace_options
    def bw_charges(self, charges, specimen):
        """
        Rescales charges back to their original values.

        Parameters
        ----------
        charges : torch.Tensor
            Charges to rescale.
        specimen : int
            The index of the dataset charges belong to.
        """
        charges *= __default__(self.charges_scale[specimen], 1)
        charges += __default__(self.charges_offsets[specimen], 1)

    @staticmethod
    def atom_counts(dataset):
        """
        Calculates atoms per each unit cell and assembles
        counts into a single tensor.

        Parameters
        ----------
        dataset : Dataset
            The dataset to process.

        Returns
        -------
        result : torch.Tensor
            A 2D tensor `[n_samples, len(per_point_datasets)]` with counts.
        """
        return torch.cat(tuple(
            i.mask.sum(dim=1)[:, None]
            for i in dataset.per_point_datasets
        ), dim=1)

    @staticmethod
    def __apply__(dataset, energy_op, energy_p_op, energy_g_op, features_op, features_g_op, charges_op, inplace=False):
        """
        Applies operations to a dataset.

        Parameters
        ----------
        dataset : Dataset
            The dataset to apply operations to.
        energy_op : Callable
            Operation on energies.
        energy_p_op : Callable
            Operation on partial energies.
        energy_g_op : Callable
            Operation on energy gradients.
        features_op : Callable
            Operation on features.
        features_g_op : Callable
            Operation on feature gradients.
        charges_op : Callable
            Operation on atomic charges.
        inplace : bool
            If True, performs the operation in-place and returns the same dataset.

        Returns
        -------
        result : Dataset
            The resulting dataset.
        """
        atom_counts = Normalization.atom_counts(dataset)
        energy = energy_op(dataset.per_cell_dataset.energy, atom_counts, inplace=inplace)
        if dataset.per_cell_dataset.is_gradient_available():
            energy_g = energy_g_op(dataset.per_cell_dataset.energy_g, inplace=inplace)
            mask = dataset.per_cell_dataset.mask.clone()
        else:
            energy_g = None
            mask = None

        features = []
        features_g = []
        charges = []
        energies_p = []

        for i, point_dataset in enumerate(dataset.per_point_datasets):
            features.append(features_op(point_dataset.features, i, inplace=inplace))

            if point_dataset.is_gradient_available():
                features_g.append(features_g_op(point_dataset.features_g, i, inplace=inplace))
            else:
                features_g.append(None)

            if point_dataset.charges is not None:
                charges.append(charges_op(point_dataset.charges, i, inplace=inplace))
            else:
                charges.append(None)

            if point_dataset.energies_p is not None:
                energies_p.append(energy_p_op(point_dataset.energies_p, i, inplace=inplace))
            else:
                energies_p.append(None)

        if inplace:
            return dataset
        else:
            return Dataset(
                PerCellDataset(energy=energy, mask=mask, energy_g=energy_g),
                *(
                    PerPointDataset(features=f, mask=d.mask.clone(), features_g=fg, charges=c, energies_p=pe,
                                    tag=d.tag)
                    for f, fg, d, c, pe in zip(features, features_g, dataset.per_point_datasets, charges, energies_p)
                ),
            )

    def fw(self, dataset, inplace=False):
        """
        Rescales dataset to ranges suitable for machine learning.

        Parameters
        ----------
        dataset : Dataset
            The dataset to rescale.
        inplace : bool
            If True, performs the operation in-place and returns the same dataset.

        Returns
        -------
        result : Dataset
            The resulting scaled dataset.
        """
        return self.__apply__(dataset, self.fw_energy, self.fw_energy_components, self.fw_energy_g, self.fw_features,
                              self.fw_features_g, self.fw_charges, inplace=inplace)

    def bw(self, dataset, inplace=False):
        """
        Rescales dataset back to original values.

        Parameters
        ----------
        dataset : Dataset
            The dataset to rescale.
        inplace : bool
            If True, performs the operation in-place and returns the same dataset.

        Returns
        -------
        result : Dataset
            The original dataset.
        """
        return self.__apply__(dataset, self.bw_energy, self.bw_energy_components, self.bw_energy_g, self.bw_features,
                              self.bw_features_g, self.bw_charges, inplace=inplace)

    @staticmethod
    def lsq_energy_offsets(dataset, pad=True):
        """
        Solves a least-squares problem for the best representation of
        cell energies as a sum of per-atom components.

        Parameters
        ----------
        dataset : Dataset
            The dataset to process.
        pad : bool
            If True, stabilizes energy padding by minimizing
            padding values together with the residuals.

        Returns
        -------
        energy_offsets : torch.Tensor
            A 1D tensor with per-specimen energy offsets.
        residuals : torch.Tensor
            A 2D tensor `[n_samples, 1]` with energy residuals
            after offsets have been subtracted.
        """
        atom_counts = Normalization.atom_counts(dataset)
        energy = dataset.per_cell_dataset.energy
        n = atom_counts.shape[1]

        if pad:
            atom_counts_padded = torch.cat((atom_counts, torch.eye(n, dtype=atom_counts.dtype)))
            energy_padded = torch.cat((energy, torch.zeros((n, 1), dtype=energy.dtype)))
            energy_offsets, _ = torch.lstsq(energy_padded, atom_counts_padded)
        else:
            energy_offsets, _ = torch.lstsq(energy, atom_counts)

        energy_offsets = energy_offsets[:n]
        residuals = energy - atom_counts @ energy_offsets
        return energy_offsets, residuals

    @classmethod
    def from_dataset(cls, dataset, ignore_normalization_errors=False, pad=True,
                     offset_energy=False, offset_features="mean", offset_charges=False,
                     scale_energy=1, scale_features=2, scale_charges=1, scale_energy_gradients=1,
                     pca_features=False):
        """
        Prepares normalization based on the dataset provided.

        Parameters
        ----------
        dataset : Dataset
            The dataset to pick normalization for.
        ignore_normalization_errors : bool
            Forces to ignore dataset parts which cannot be normalized.
        pad : bool
            Stabilize least-squares problem when determining per-specimen
            energy offsets.
        offset_energy : bool
        offset_features : bool
        offset_charges : bool
            If True, offsets energies, descriptors, and/or charges.
        scale_energy : float
        scale_features : float
        scale_charges : float
        scale_energy_gradients : float
            If set scales energies, descriptors, and/or charges to the value specified.
        pca_features : float, int, bool, Callable
            If set, performs principal component analysis (e.g. SVD) and prepares a truncated
            linear transformation of descriptors as a part of normalization. Float value has
            the meaning of a relative cutoff of singular values with respect to the maximal
            singular value. Integer value corresponds to the number of highest singular
            values to chose. Callable is expected to take the output of `torch.svd` and to
            return the bool mask of singular entries chosen.

        Returns
        -------
        normalization : Normalization
            The resulting normalization.
        """
        # Positive and negative infs for the data type
        finfo = torch.finfo(dataset.dtype)
        pinf = finfo.max
        ninf = finfo.min

        if offset_energy:
            # Energy offsets
            energy_offsets, energy_residuals = Normalization.lsq_energy_offsets(dataset, pad=pad)

        else:
            energy_offsets = torch.zeros(len(dataset.per_point_datasets), 1, dtype=dataset.dtype)
            energy_residuals = dataset.per_cell_dataset.energy

        # Energy scale
        if scale_energy:
            mn = torch.min(energy_residuals)
            mx = torch.max(energy_residuals)
            if mn == mx:
                if not ignore_normalization_errors:
                    raise ValueError(f"The energy dataset is constant {mn} after per-specimen components were subtracted. "
                                     f"Please check the original data of set 'force' argument to True to ignore this error.")
                energy_scale = torch.scalar_tensor(1, dtype=dataset.per_cell_dataset.energy.dtype)
            else:
                energy_scale = (mx - mn) / scale_energy

        else:
            energy_scale = torch.scalar_tensor(1, dtype=dataset.per_cell_dataset.energy.dtype)

        # Length scale
        if dataset.per_cell_dataset.is_gradient_available():
            if scale_energy_gradients:
                energy_g = dataset.per_cell_dataset.energy_g
                energy_g_mask = dataset.per_cell_dataset.mask == -1

                energy_g[energy_g_mask] = pinf
                mn = torch.min(energy_g)
                energy_g[energy_g_mask] = ninf
                mx = torch.max(energy_g)
                if mn == mx:
                    if not ignore_normalization_errors:
                        raise ValueError(f"The energy gradients dataset is constant {mn}. Please check the original data of "
                                         f"set 'force' argument to True to ignore this error.")
                    energy_gradient_scale = 1
                else:
                    energy_gradient_scale = mx - mn
                energy_g[energy_g_mask] = 0
                length_scale = energy_scale / energy_gradient_scale * scale_energy_gradients
            else:
                length_scale = 1
        else:
            length_scale = None

        # Features and charges scale
        pp = dataset.per_point_datasets
        features_scale = []
        features_offsets = []
        charges_scale = []
        charges_offsets = []

        for i in pp:
            features = i.features.reshape((-1, i.features.shape[2]))
            mask = i.mask.flatten()

            n_features = features.shape[-1]
            v_features = torch.eye(n_features, dtype=features.dtype)  # features rotation
            if pca_features:
                u, s, v_features = torch.svd(features[mask.ne(0), :])  # note v_features is transposed
                if isinstance(pca_features, int):
                    select = torch.zeros(len(s), dtype=torch.bool)
                    select[:pca_features] = 1
                elif isinstance(pca_features, float):
                    select = s >= s[0] * pca_features
                else:
                    select = pca_features(u, s, v_features)
                if not torch.all(select):
                    v_features = v_features[:, select]
                    features = features @ v_features  # further normalization is performed on transformed features

            # not_mask = torch.logical_not(mask)
            not_mask = mask == 0  # compat with old pytorch versions

            features[not_mask] = pinf
            mn, _ = torch.min(features, dim=0)

            features[not_mask] = ninf
            mx, _ = torch.max(features, dim=0)

            features[not_mask] = 0
            fs = mx - mn

            if offset_features == "mean":
                b_features = mn + fs / 2
            elif offset_features is True:
                b_features = mn
            elif not offset_features:
                b_features = torch.zeros_like(mn)
            else:
                raise ValueError(f"Unknown offset_features = '{offset_features}'")
            features_offsets.append(b_features @ v_features.T)

            if scale_features:
                if any(fs == 0):
                    if not ignore_normalization_errors:
                        which = torch.nonzero(fs == 0)
                        raise ValueError(f"Feature(s) with id(s) {which.squeeze()} "
                                         f"of dataset #{len(features_scale):d} is (are) constant: {mn[fs == 0]}. "
                                         f"Please check the original data of set 'force' argument to True to "
                                         f"ignore this.")
                    fs[fs == 0] = 1
                s_features = torch.diag(fs / scale_features)
            else:
                s_features = torch.eye(len(fs), dtype=fs.dtype)
            features_scale.append(s_features @ v_features.T)

            # Charges
            if i.charges is not None:
                charges = i.charges.reshape(-1)

                charges[not_mask] = pinf
                mn = torch.min(charges)

                charges[not_mask] = ninf
                mx = torch.max(charges)

                charges[not_mask] = 0
                cs = mx - mn

                if offset_charges == "mean":
                    charges_offsets.append(mn + cs / 2)
                elif offset_charges is True:
                    charges_offsets.append(mn)
                elif not offset_charges:
                    charges_offsets.append(torch.zeros_like(mn))
                else:
                    raise ValueError(f"Unknown offset_charges = '{offset_charges}'")

                if scale_charges:
                    if cs == 0:
                        if not ignore_normalization_errors:
                            raise ValueError(f"Charges of dataset #{len(charges_scale):d} are constant ({mn}). Please "
                                             f"check the original data or set 'force' argument to True to ignore this.")
                        cs = 1

                    charges_scale.append(torch.tensor(cs / scale_charges))
                else:
                    charges_scale.append(torch.ones_like(cs))

            else:
                charges_scale.append(None)
                charges_offsets.append(None)

        return cls(energy_scale, features_scale, energy_offsets, features_offsets, length_scale=length_scale,
                   charges_offsets=charges_offsets, charges_scale=charges_scale)


def learn_cauldron(cells, descriptors, grad=False, normalize=True, extract_forces=None, extract_charges=False,
                   energies_p=False, norm_kwargs=None, prefer_parallel=None):
    """
    A function assembling data for learning.

    Parameters
    ----------
    cells : tuple
        Cells to process.
    descriptors : dict
        A dictionary with atoms (keys) and descriptors.
    grad : bool
        Include gradients.
    normalize : class
        If set, normalizes with the given class and returns the normalization
        together with the dataset. If True, uses the `Normalization` class.
        Set to False if no normalization needed.
    extract_forces : bool, None
        If True, extracts forces from unit cell data. Defaults to `grad` value.
    extract_charges : bool
        If True, extract atomic charges from unit cell data.
    energies_p : bool
        If True, extract partial energies.
    norm_kwargs : dict
        Arguments to normalization.
    prefer_parallel : bool
        If True, computes descriptors with OpenMP whenever possible.

    Returns
    -------
    dataset : Dataset
        The dataset.
    normalization : Normalization, optional
        The normalization.
    """
    if normalize is True:
        normalize = Normalization
    if norm_kwargs is None:
        norm_kwargs = dict()
    if extract_forces is None:
        extract_forces = grad
    values, values_key = encode_species(cells)

    per_cell = PerCellDataset.from_cells(cells, values, grad=extract_forces)
    per_point = []
    for i_s, s in enumerate(values_key):
        per_point.append(PerPointDataset.from_cells(cells, descriptors[s], i_s, values, grad=grad,
                                                    charge=extract_charges, energies_p=energies_p,
                                                    tag=i_s, prefer_parallel=prefer_parallel))

    dataset = Dataset(per_cell, *per_point)

    if normalize:
        normalization = normalize.from_dataset(dataset, **norm_kwargs)
        normalization.fw(dataset, inplace=True)
        return dataset, normalization

    else:
        return dataset


def total_energy(net_output, mask=None):
    """
    Computes total energy value per unit cell.

    Parameters
    ----------
    net_output : torch.Tensor, np.ndarray
        Output from the energy learning network: a 3D tensor
        of shape `[n_samples, n_points, 1]` with per-cell
        per-point energies.
    mask : torch.Tensor, np.ndarray
        A 2D mask Tensor of shape `[n_samples, n_points]`
        distinguishing true vs padding entries.

    Returns
    -------
    result : torch.Tensor
        A 2D tensor of shape `[n_samples, 1]` with total
        energies per unit cell.
    """
    if mask is not None:
        net_output = net_output * mask[..., None]
    result = net_output.sum(dim=1)
    return result


def energy_gradients(net_output, features_g, per_sample=False):
    """
    Computes total energy gradients.

    Parameters
    ----------
    net_output : torch.Tensor, np.ndarray
        Output from the energy learning network: a 3D tensor
        of shape `[n_samples, n_species, n_descriptors]` with per-cell
        per-point energy gradients wrt descriptors.
    features_g : torch.Tensor, np.ndarray
        A 5D tensor of shape
        `[n_samples, n_species, n_descriptors, n_atoms, n_coords]`
        with per-cell per-point descriptor gradients.
    per_sample : bool
        If True, "energy" is considered to be per-point energy
        contribution. Otherwise total energy gradients are computed.

    Returns
    -------
    result : torch.Tensor
        A tensor of shape `[n_samples, n_atoms, n_coords]`
        if `per_sample == False` or a 4D tensor
        `[n_samples, n_points, n_atoms, n_coords]` if `per_sample == True`.
    """
    if isinstance(net_output, np.ndarray):
        einsum = np.einsum
        empty = np.empty
        size = net_output.size
    else:
        einsum = torch.einsum
        empty = torch.empty
        size = net_output.numel()
    if size == 0:
        _s, _p, _d = net_output.shape
        s, p, d, a, c = features_g.shape
        assert s == _s and p == _p and d == _d
    if per_sample:
        if size == 0:  # torch.einsum is not capable of handling empty tensors
            result = empty((s, p, a, c), dtype=features_g.dtype)
        else:
            result = einsum("spd,spdac->spac", net_output, features_g)
    else:
        if size == 0:  # torch.einsum is not capable of handling empty tensors
            result = empty((s, a, c), dtype=features_g.dtype)
        else:
            result = einsum("spd,spdac->sac", net_output, features_g)
    return result


class EnergyNNMixin:
    def forward(self, x, grad=False):
        """
        Computes energies and gradients.

        Parameters
        ----------
        x : torch.Tensor
            Features input.
        grad : bool
            If True, outputs gradients as well.

        Returns
        -------
        energies : torch.Tensor
        gradients : torch.Tensor
        """
        result = super().forward(x)
        if not grad:
            return result
        else:
            result_grad = torch.autograd.grad(result, x, grad_outputs=torch.ones_like(result), create_graph=True)[0]
            return result, result_grad


class SequentialSoleEnergyNN(EnergyNNMixin, torch.nn.Sequential):
    def __init__(self, arg, n_layers=3, n_internal=15, bias=True):
        """
        Sequential neural network with descriptor inputs and
        energy output.

        Parameters
        ----------
        arg : int, list
        n_layers : int
        n_internal : int
        bias : bool, list, tuple
            Bias per layer or for all layers.
        """
        if not isinstance(arg, int):
            super().__init__(*arg)

        else:
            n_features = arg
            if isinstance(bias, (list, tuple)):
                if len(bias) != n_layers:
                    raise ValueError(f"len(bias) = {len(bias)} != n_layers = {n_layers}")
            else:
                bias = (bias,) * n_layers

            if n_layers == 1:
                super().__init__(torch.nn.Linear(n_features, 1, bias=bias[0]))
            else:
                super().__init__(
                    torch.nn.Linear(n_features, n_internal, bias=bias[0]),
                    *sum((
                            (torch.nn.Sigmoid(), torch.nn.Linear(n_internal, n_internal, bias=b))
                            for b in bias[1:-1]
                    ), tuple()),
                    torch.nn.Sigmoid(),
                    torch.nn.Linear(n_internal, 1, bias=bias[-1]),
                )


def fw_cauldron(modules, dataset, grad=False, energies_p=False, normalization=None):
    """
    Propagates modules forward and assembles the total energy and gradients.

    Parameters
    ----------
    modules : list, tuple
        A list of modules mapping descriptors onto local energies.
    dataset : Dataset, list, tuple
        The dataset with descriptors or tensors to assemble the dataset from.
    grad : bool
        If True, computes gradients wrt descriptors.
    energies_p : bool
        If True, presents total energy as a sum of per-atom contributions.
    normalization : Normalization
        Optional normalization to apply (backward).

    Returns
    -------
    energy : Tensor, list
        A `[n_samples, 1]` tensor with total energies or a list of `[n_samples, n_species, 1]`
        tensors with per-atom contributions.
    gradients : Tensor, optional
        A `[n_samples, n_atoms, 3]` tensor with total energy gradients.
    """
    if not isinstance(dataset, Dataset):
        dataset = Dataset.from_tensors(dataset)
    if len(modules) != len(dataset.per_point_datasets):
        raise ValueError(f"The module count does {len(modules):d} does not coincide with "
                         f"per-point dataset count {len(dataset.per_point_datasets):d}")
    if energies_p:
        energy = []
    else:
        energy = torch.zeros_like(dataset.per_cell_dataset.energy)
    if grad:
        gradients = torch.zeros_like(dataset.per_cell_dataset.energy_g)
    for m, d in zip(modules, dataset.per_point_datasets):
        out = m(d.features, grad=grad)
        if grad:
            out, out_grad = out
        if energies_p:
            energy.append(out)
        else:
            energy += total_energy(out, d.mask)
        if grad:
            gradients += energy_gradients(out_grad, d.features_g)

    if normalization:
        atom_counts = normalization.atom_counts(dataset)
        if energies_p:
            for i, e in enumerate(energy):
                normalization.bw_energy_components(e, i, inplace=True)
        normalization.bw_energy(energy, atom_counts, inplace=True)
        if grad:
            normalization.bw_energy_g(gradients, inplace=True)

    if grad:
        return energy, gradients
    else:
        return energy


def fw_cauldron_charges(modules, dataset, normalization=None):
    """
    Propagates modules forward and assembles atomic charges.

    Parameters
    ----------
    modules : list, tuple
        A list of modules mapping descriptors onto atomic charges.
    dataset : Dataset, list, tuple
        The dataset with descriptors or tensors to assemble the dataset from.
    normalization : Normalization
        Optional normalization to apply (backward).

    Returns
    -------
    charges : list
        A list of `[n_samples, n_species]` tensors with atomic charges.
    """
    if not isinstance(dataset, Dataset):
        dataset = Dataset.from_tensors(dataset)
    if len(modules) != len(dataset.per_point_datasets):
        raise ValueError(f"The module count does {len(modules):d} does not coincide with "
                         f"per-point dataset count {len(dataset.per_point_datasets):d}")
    charges = []
    for i, (m, d) in enumerate(zip(modules, dataset.per_point_datasets)):
        charges.append(m(d.features))
        if normalization:
            normalization.bw_charges(charges[-1], i)

    return charges


def kernel_u_nn(kind, r_indptr, r_indices, r_data, cartesian_row, cartesian_col, descriptors, nn, normalization,
                normalization_handle, species_row, species_mask, out):
    """
    Neural network potential kernel.
    This technically acts as an on-site potential.

    The workflow:
    1. Compute descriptors.
    2. Normalize them.
    3. Apply the network.
    4. De-normalize the output.

    Parameters
    ----------
    kind : {'fun', 'grad'}
        Indicates to return per-point energies or energy gradients.
    r_indptr : np.ndarray
    r_indices : np.ndarray
    r_data : np.ndarray
    cartesian_row : np.ndarray
    cartesian_col : np.ndarray
        Common arguments to descriptor kernels specifying coordinates and
        neighbor relations.
    descriptors : list
        A list with atoms (keys) and descriptors (pairs of string spec
        and `LocalPotential` instance).
    nn : torch.Module
        The network mapping descriptors onto individual energies.
    normalization : Normalization
        Normalization information. Can be None.
    normalization_handle : int
        The index of the atom described in the `normalization`.
    species_row : np.ndarray
    species_mask : np.ndarray
    out : np.ndarray
    """
    assert len(species_mask) == 1
    assert kind in ("fun", "grad")
    do_grad = kind == "grad"
    sparse_pair_distances = csr_matrix((r_data, r_indices, r_indptr), shape=(len(cartesian_row), len(cartesian_col)))

    # Compute descriptors and, optionally, their gradients
    out_mask = species_row == species_mask[0]
    descriptor_values = eval_potentials(
        descriptors, "kernel", sparse_pair_distances, cartesian_row, cartesian_col, species_row,
        pre_compute_r=False, cutoff=None, out=None,
    ).swapaxes(0, 1)[None, out_mask, ...]
    if do_grad:
        descriptor_gradient_values = eval_potentials(
            descriptors, "kernel_gradient", sparse_pair_distances, cartesian_row, cartesian_col, species_row,
            pre_compute_r=False, cutoff=None, out=None,
        ).swapaxes(0, 1)[None, out_mask, ...]

    # Switch to torch  # TODO: fix dtype
    descriptor_values = torch.tensor(descriptor_values, dtype=nn[0].weight.dtype)
    if do_grad:
        descriptor_gradient_values = torch.tensor(descriptor_gradient_values, dtype=nn[0].weight.dtype)

    # Scale descriptors
    if normalization:
        normalization.fw_features(descriptor_values, normalization_handle, inplace=True)
        n_invalid = (descriptor_values < -1).sum() + (descriptor_values > 1).sum()
        if n_invalid:
            warn(f"{n_invalid:d} ({100.0 * n_invalid / descriptor_values.nelement():.0f}%) descriptors exceed the "
                 f"[-1, 1] interval after normalization. This likely means that the fit is extrapolating.",
                 PotentialRuntimeWarning)
        if do_grad:
            normalization.fw_features_g(descriptor_gradient_values, normalization_handle, inplace=True)

    # Propagate
    descriptor_values.requires_grad = do_grad
    nn_out = nn(descriptor_values, grad=do_grad)

    if do_grad:
        energy_values, energy_descriptor_gradients = nn_out
        energy_g = energy_gradients(energy_descriptor_gradients, descriptor_gradient_values, per_sample=True)
        # Un-scale the result
        if normalization:
            normalization.bw_energy_g(energy_g, inplace=True)

        out[out_mask, ...] += energy_g[0].detach().numpy()

    else:
        energy_values = nn_out
        # Un-scale the result
        if normalization:
            normalization.bw_energy_components(energy_values, normalization_handle, inplace=True)

        out[out_mask] = energy_values[0, :, 0].detach().numpy()


kernel_nn = partial(kernel_u_nn, "fun")
kernel_g_nn = partial(kernel_u_nn, "grad")


def ml_potential_cutoff(parameters):
    """
    Calculates the cutoff of ml potentials.

    Parameters
    ----------
    parameters : dict
        A dict with parameters.

    Returns
    -------
    cutoff : float
        The cutoff value.
    """
    descriptors = parameters["descriptors"]
    if len(descriptors) == 0:
        return 0
    return max(i.cutoff for i in descriptors)


normalization_atomic_units = ParameterUnits(dict(
    energy_scale="eV",
    energy_offsets="eV",
    length_scale="angstrom",
))


class NNPotential(LocalPotential):
    # Because NN potential includes much more parameters, the following (de)serialization routines are provided
    def state_dict(self, units=True):
        """
        Returns a dict of parameters describing this ml potential.
        No copies are made.

        Parameters
        ----------
        units : bool, ParameterUnits
            Units to apply. If True, default atomic (energy and length) units
            are applied.

        Returns
        -------
        params : dict
            A dict of parameters.
        """
        result = self.to_json()
        parameters = result["parameters"]
        parameters["nn"] = parameters["nn"].state_dict()
        parameters["descriptors"] = tuple(i.to_json() for i in parameters["descriptors"])
        if parameters["normalization"] is not None:
            if units is True:
                units = normalization_atomic_units
            parameters["normalization"] = parameters["normalization"].state_dict()
            if units:
                parameters["normalization"] = units.apply(parameters["normalization"])
                parameters["normalization-units"] = dict(units)
        return result

    def load_state_dict(self, d):
        """
        Loads state dict.

        Parameters
        ----------
        d : dict
            The dictionary to load.
        """
        d = d.copy()
        assert d.pop("tag") == "ml potential"
        self.tag = d.pop("ptag")
        source_parameters = d.pop("parameters").copy()
        self.parameters["nn"].load_state_dict(source_parameters.pop("nn"))
        self.parameters["descriptors"] = list(
            LocalPotentialFamily.instance_from_json(i)
            for i in source_parameters.pop("descriptors")
        )
        n = source_parameters.pop("normalization")
        n_dest = self.parameters["normalization"]
        if n is not None:
            if n_dest is None:
                raise ValueError("Normalization is present in the data but not in the object")
            units_dict = source_parameters.pop("normalization-units", None)
            if units_dict:
                n = ParameterUnits(units_dict).lift(n)
            n_dest.load_state_dict(n)
        elif n_dest is not None:
            raise ValueError("No normalization data is available")
        self.parameters["normalization_handle"] = source_parameters.pop("normalization_handle")
        assert len(source_parameters) == 0
        assert len(d) == 0
        # Restore cutoff
        self.cutoff = ml_potential_cutoff(self.parameters)

    @staticmethod
    def from_state_dict(d):
        """
        Loads from state dict.

        This function is fragile: it does its best to determine
        NN structure from the input assuming it is exactly SequentialSoleEnergyNN.

        Parameters
        ----------
        d : dict
            Data to restore from.

        Returns
        -------
        potential : NNPotential
            The resulting potential.
        """
        parameters = d["parameters"]
        nn = dict(parameters["nn"])
        args = []
        n_layers = 0
        while len(nn):
            if n_layers:
                args.append(torch.nn.Sigmoid())
            weights = nn.pop(f"{n_layers:d}.weight")
            bias = nn.pop(f"{n_layers:d}.bias", None)
            args.append(torch.nn.Linear(weights.shape[1], weights.shape[0], bias=bias is not None))
            n_layers += 2
        host = ml_potential_family(
            nn=SequentialSoleEnergyNN(args),
            descriptors=tuple(),
            normalization=None if parameters["normalization"] is None else Normalization.__new__(Normalization),
            normalization_handle=-1,
        )
        host.load_state_dict(d)
        return host


ml_potential_family = LocalPotentialFamily(
    coordination_number=1,
    parameters=dict(descriptors=None, nn=None, normalization=None, normalization_handle=None),
    cutoff=ml_potential_cutoff,
    kernel=kernel_nn,
    kernel_gradient=kernel_g_nn,
    tag='ml potential',
    proto=NNPotential,
)


def potentials_from_ml_data(nn, descriptors, normalization=None):
    """
    Constructs potentials from neural networks.

    Parameters
    ----------
    nn : list
        A list of neural networks modelling force fields per atom type.
    descriptors : dict
        A dict with descriptors.
    normalization : Normalization
        Normalization information.

    Returns
    -------
    potentials : list
        Neural-network potentials.
    """
    result = []
    for i, (n, (key, d)) in enumerate(zip(nn, sorted(descriptors.items()))):
        result.append(ml_potential_family(nn=n, descriptors=d, normalization=normalization, normalization_handle=i,
                                          tag=key))
    return result
