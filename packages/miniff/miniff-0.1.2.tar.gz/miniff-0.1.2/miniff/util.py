import numpy as np
import numericalunits
from numericalunits import nu_eval


def num_grad(f, x, *args, eps=1e-4):
    """
    Numerical gradient.

    Parameters
    ----------
    f : function
        A function computing a scalar.
    x : np.ndarray
        The point to compute gradient at.
    *args
        Other arguments to the function.
    eps : float
        Numerical gradient step.

    Returns
    -------
    gradient : np.ndarray
        The gradient value(s).
    """
    x = np.array(x, dtype=float)
    y = np.array(f(x, *args))
    gradient = np.empty(y.shape + x.shape, dtype=y.dtype)

    for i in np.ndindex(*x.shape):
        x[i] += eps
        e2 = f(x, *args)
        x[i] -= 2 * eps
        gradient[(Ellipsis,) + i] = (e2 - f(x, *args)) / 2 / eps
        x[i] += eps
    return gradient


class ParameterUnits(dict):
    def get_uv(self, key, default=1):
        """
        Retrieves a unit value assigned to the key.

        Parameters
        ----------
        key
            A valid dictionary key.
        default : float
            Default value.

        Returns
        -------
        result : float
            The unit value.
        """
        if key not in self:
            return default
        return nu_eval(self[key])

    def apply(self, parameters):
        """
        Applies units to parameters.

        Parameters
        ----------
        parameters : dict
            A dict of potential parameters where units have to be applied.

        Returns
        -------
        result : dict
            A dict of potential parameters with units applied.
        """
        def _apply(_v, _u):
            if _v is None:
                return None
            elif isinstance(_v, tuple):
                return tuple(_i / _u for _i in _v)
            else:
                return _v / _u
        return {k: _apply(v, self.get_uv(k)) for k, v in parameters.items()}

    def lift(self, parameters):
        """
        Lift units from parameters (inverse to `self.apply_units`).

        Parameters
        ----------
        parameters : dict
            A dict of potential parameters where units have to be lifted.

        Returns
        -------
        result : dict
            A dict of potential parameters with units lifted.
        """
        def _apply(_v, _u):
            if _v is None:
                return None
            elif isinstance(_v, tuple):
                return tuple(_i * _u for _i in _v)
            else:
                return _v * _u
        return {k: _apply(v, self.get_uv(k)) for k, v in parameters.items()}

    def repr(self, parameters):
        """
        Represents parameters with the units specified.

        Parameters
        ----------
        parameters : dict
            Parameters to represent.

        Returns
        -------
        result : str
            The string representation.
        """
        parameters = self.apply(parameters)
        result = []

        for k in sorted(parameters):
            v = parameters[k]
            if k in self:
                result.append(f'{k}={v:.3e}*{self[k]}')
            else:
                result.append(f'{k}={v:.3e}')
        return f"dict({', '.join(result)})"


def masked_unique(a, return_inverse=False, fill_value=None):
    """
    A proper implementation of `np.unique` for masked arrays.

    Parameters
    ----------
    a : np.ma.masked_array
        The array to process.
    return_inverse : bool
        If True, returns the masked inverse.
    fill_value : int
        An optional value to fill the `return_inverse` array.

    Returns
    -------
    key : np.ndarray
        Unique entries.
    inverse : np.ma.masked_array, optional
        Integer masked array with the inverse.
    """
    key = np.unique(a, return_inverse=return_inverse)
    if return_inverse:
        key, inverse = key
        barrier = np.argwhere(key.mask)
        if len(barrier) > 0:
            barrier = barrier.squeeze()  # all indices after the barrier have to be shifted (char only?)
            inverse[inverse > barrier] -= 1  # shift everything after the barrier
            if fill_value is None:
                inverse[a.mask.reshape(-1)] = len(key) - 1  # shift masked stuff to the end
            else:
                inverse[a.mask.reshape(-1)] = fill_value
        inverse = np.ma.masked_array(data=inverse, mask=a.mask)
    key = key.data[np.logical_not(key.mask)]
    if return_inverse:
        return key, inverse
    else:
        return key


def dict_reduce(d, operation):
    """
    Reduces dictionary values.

    Parameters
    ----------
    d : Iterable
        Dictionaries to process.
    operation : Callable
        Operation on values.

    Returns
    -------
    result : dict
        A dictionary with reduced values.
    """
    result = {}

    for _d in d:
        for k, v in _d.items():
            if k not in result:
                result[k] = [v]
            else:
                result[k].append(v)

    return {k: operation(v) for k, v in result.items()}


def array_to_json(a):
    """
    Writes numpy array to json-compatible object.

    Parameters
    ----------
    a : np.ndarray
        Array to serialize.

    Returns
    -------
    result : dict
        The serialized array.
    """
    if not isinstance(a, ArrayWithUnits):
        a = np.asarray(a).view(ArrayWithUnits)
    if a.units is None:
        a = a.view()
    else:
        a = a / nu_eval(a.units)
    is_complex = np.iscomplexobj(a)
    if is_complex:
        _a = np.concatenate((a.real[..., np.newaxis], a.imag[..., np.newaxis]), axis=-1)
    else:
        _a = a
    return dict(
        _type="numpy",
        data=_a.tolist(),
        complex=is_complex,
        units=a.units,
    )


class ArrayWithUnits(np.ndarray):
    """Enhances numpy array with units from `numericalunits`."""

    def __new__(cls, *args, **kwargs):
        units = kwargs.pop("units", None)
        obj = np.asarray(*args, **kwargs).view(cls)
        obj.units = units
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.units = getattr(obj, 'units', None)

    @classmethod
    def from_json(cls, data):
        """
        Recovers the serialized data with units.

        Parameters
        ----------
        data : dict
            The serialized data.

        Returns
        -------
        result : ArrayWithUnits
            The resulting array.
        """
        assert data["_type"] == "numpy"

        a = np.asarray(data["data"])
        if data["complex"]:
            a = a[..., 0] + 1j * a[..., 1]

        if data["units"] is not None:
            a *= nu_eval(data["units"])

        return cls(a, units=data["units"])

    def __reduce__(self):
        if self.units is None:
            state = super(ArrayWithUnits, self).__reduce__()
        else:
            state = np.ndarray.__reduce__(self / nu_eval(self.units))
        return state[:2] + (state[2] + (self.units,),)

    def __setstate__(self, state):
        super(ArrayWithUnits, self).__setstate__(state[:-1])
        self.units = state[-1]
        if self.units is not None:
            self *= nu_eval(self.units)


def serialize_nu():
    """
    Retrieves the current state of `numericalunits` package and saves it into dict.

    Returns
    -------
    units : dict
        A dictionary with units.
    """
    return {k: v for k, v in numericalunits.__dict__.items() if isinstance(v, float) and not k.startswith("_")}


def load_nu(data):
    """
    Loads previously saved `numericalunits` values.

    Parameters
    ----------
    data : dict
        A dictionary with the serialized data.
    """
    numericalunits.__dict__.update(data)
