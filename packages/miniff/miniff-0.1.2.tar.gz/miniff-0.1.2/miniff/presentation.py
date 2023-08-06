from numericalunits import nu_eval
from .potentials import behler2_descriptor_family, behler_turning_point
from .kernel import profile_directed_strain, Cell

from matplotlib import pyplot
from matplotlib.axes import Axes
import numpy as np
# from dfttools.types import UnitCell


def plot_rdf(r, data, ax=None, legend=True, length_unit="angstrom", xlabel=True, ylabel=True, **kwargs):
    """
    Plot radial distribution function.

    Parameters
    ----------
    r : np.ndarray
        Radial points.
    data : dict
        RDF.
    ax : Axes
        `matplotlib` axes to plot on.
    legend : bool
        If True, creates a legend.
    length_unit : str
        A valid `numericalunits` string expression for units.
    xlabel : bool, str
        x axis label.
    ylabel : bool, str
        y axis label.
    kwargs
        Passed to `ax.plot`.

    Returns
    -------
    ax : Axes
        `matplotlib` axes.
    """
    if ax is None:
        ax = pyplot.gca()
    scale = nu_eval(length_unit)
    for k, v in sorted(data.items()):
        ax.plot(r / scale, v * (scale ** 3), label=k, **kwargs)

    if xlabel is True:
        ax.set_xlabel(f"r ({length_unit})")
    elif xlabel:
        ax.set_xlabel(xlabel)
    if ylabel is True:
        ax.set_ylabel(f"Density (atoms / [{length_unit}]^3)")
    elif ylabel:
        ax.set_ylabel(ylabel)
    if legend:
        ax.legend()

    return ax


def plot_strain_profile(potentials, cell, x, limits=(0.9, 1.1), direction=(1, 1, 1),
                        ax=None, energy_unit="Ry", xlabel=True, ylabel=True,
                        mark_points=None, origin=None, **kwargs):
    """
    Plot energy as a function of strain.

    Parameters
    ----------
    potentials : list
        Potentials to profile.
    cell : Cell
        The original cell.
    x : tuple
        The number of cell replica included in distance calculation.
    limits : tuple
        Lower and upper strain bounds.
    direction : list, tuple, np.ndarray
        Strain direction.
    ax : Axes
        `matplotlib` axes to plot on.
    energy_unit : str
        A valid `numericalunits` string expression for units.
    xlabel : bool, str
        x axis label.
    ylabel : bool, str
        y axis label.
    mark_points : list, tuple
        Marks special points on the potential profile.
    origin : str, float
       Energy origin: either float number of 'left', 'right', or 'median'.
    kwargs
        Arguments to pyplot.plot.

    Returns
    -------
    ax : Axes
        `matplotlib` axes.
    """
    if ax is None:
        ax = pyplot.gca()

    if energy_unit is not None:
        energy_unit_val = nu_eval(energy_unit)
    else:
        energy_unit_val = 1

    strain = np.linspace(*limits)
    val = profile_directed_strain(potentials, cell, strain, direction, x=x) / energy_unit_val

    if origin is None:
        origin = 0
    elif isinstance(origin, str):
        origin = dict(
            left=val[0],
            right=val[-1],
            median=.5 * (np.max(val) + np.min(val)),
        )[origin]

    ax.plot(strain, val - origin, **kwargs)

    if mark_points is not None:
        mark_points = np.array(mark_points)
        mark_points_val = profile_directed_strain(potentials, cell, mark_points, direction, x=x) / energy_unit_val
        ax.scatter(mark_points, mark_points_val - origin, marker="x", color="black")

    if xlabel is True:
        ax.set_xlabel(f"{direction} expansion")
    elif xlabel:
        ax.set_xlabel(xlabel)
    if ylabel is True:
        ax.set_ylabel(f"Energy ({energy_unit})")
    elif ylabel:
        ax.set_ylabel(ylabel)

    return ax


def plot_potential_2(potentials, limits=None, pair=None, ax=None, energy_unit="Ry",
                     length_unit="angstrom", xlabel=True, ylabel=True, mark_points=None,
                     origin=None, **kwargs):
    """
    Plot potential profile between a pair of points.

    Parameters
    ----------
    potentials : LocalPotential, list
        The potential to plot.
    limits : tuple
        Limits in absolute units. Defaults to `(potential.cutoff / 10, potential.cutoff)`.
    pair : str
        Pair to plot.
    ax : Axes
        `matplotlib` axes to plot on.
    energy_unit : str
        A valid `numericalunits` string expression for units.
    length_unit : str
        A valid `numericalunits` string expression for units.
    xlabel : bool, str
        x axis label.
    ylabel : bool, str
        y axis label.
    mark_points : list, tuple
        Marks special points on the potential profile.
    origin : str, float
       Energy origin: either float number of 'left', 'right', or 'median'.
    kwargs
        Arguments to pyplot.plot.

    Returns
    -------
    ax : Axes
        `matplotlib` axes.
    """
    if not isinstance(potentials, (list, tuple)):
        potentials = [potentials]

    if pair is None:
        if len(potentials) == 1 and potentials[0].coordination_number == 2:
            if potentials[0].tag is None:
                potentials = [potentials[0].copy(tag="1-2")]
            pair = potentials[0].tag
        else:
            raise ValueError(f"Please specify which pair to profile using 'pair' arg")

    if xlabel is True:
        xlabel = f"r ({length_unit})"

    if limits is None:
        cutoff = max(i.cutoff for i in potentials)
        limits = (cutoff / 10, cutoff)

    a = nu_eval(length_unit)
    cell = Cell(
        [(2 * a, 0, 0), (0, 2 * a, 0), (0, 0, 2 * a)],
        [(0, 0, 0), (.5, 0, 0)],
        pair.split("-"),
    )
    return plot_strain_profile(
        potentials, cell, (1, 1, 1),
        limits=np.array(limits) / a,
        direction=(1, 0, 0), ax=ax, energy_unit=energy_unit, xlabel=xlabel, ylabel=ylabel,
        mark_points=np.array(mark_points) / a if mark_points is not None else None,
        origin=origin, **kwargs
    )


def plot_descriptors_2(descriptors, ax=None, length_unit="angstrom", xlabel=True, legend=True, **kwargs):
    """
    Plots two-point descriptor functions.

    Parameters
    ----------
    descriptors : dict
        A dictionary with atoms (keys) and descriptors.
    ax : Axes
        `matplotlib` axes to plot on.
    length_unit : str
        A valid `numericalunits` string expression for units.
    xlabel : bool, str
        x axis label.
    legend : bool
        If True, displays legend.
    kwargs
        Arguments to pyplot.plot.

    Returns
    -------
    ax : Axes
        `matplotlib` axes.
   """
    if ax is None:
        ax = pyplot.gca()

    for belongs_to, desc in sorted(descriptors.items()):
        for d in desc:

            if d.family is behler2_descriptor_family:
                special = [behler_turning_point(**d.parameters)]
            else:
                special = None

            plot_potential_2(d, ax=ax, length_unit=length_unit, energy_unit="1",
                             xlabel=xlabel, ylabel=False, label=f"{belongs_to}: {d.tag}",
                             mark_points=special, **kwargs)
    if legend:
        ax.legend()

    return ax


def plot_convergence(y=None, append=True, ax=None, xlabel="Step", ylabel="Error", comment=None, grid=True,
                     labels=None):
    """
    Prepares convergence plots.

    Parameters
    ----------
    y : tuple, list, np.ndarray, float, None
        Error values.
    append : bool
        If True and `ax` is set, appends convergence data.
    ax : Axes
        `matplotlib` axes to plot on.
    xlabel : str
        x axis label.
    ylabel : str
        y axis label.
    comment : str
        An optional comment.
    grid : bool
        Plot grid.
    labels : list, tuple
        A list of labels for the legend.

    Returns
    -------
    ax : Axes
        `matplotlib` axis.
    """
    if y is None:
        y = [np.empty(0, dtype=float)]  # None = single empty convergence plot
    elif isinstance(y, int):
        y = [np.empty(0, dtype=float)] * y  # int = n empty convergence plots
    elif isinstance(y, float):
        y = [np.array([y])]  # float = single convergence point
    elif isinstance(y, np.ndarray):
        y = [y]  # array = single convergence array

    if comment is None:
        comment = ""

    y = tuple(map(np.array, y))
    for i in y:
        i.shape = i.size,

    def _plot_data(_y, prev=None):
        if prev is not None:
            _y = np.concatenate([prev, _y])
        return np.arange(len(_y)), _y

    if ax is None or not append:
        if ax is None:
            ax = pyplot.gca()
        ax.clear()

        if labels and len(labels) != y:
            raise ValueError(f"len(labels) = {len(labels):d} != len(y) = {len(y):d}")

        for i_data, data in enumerate(y):
            ax.semilogy(*_plot_data(data), label=labels[i_data] if labels else None)
        ax.text(0.05, 0.9, comment, transform=ax.transAxes)

        if xlabel:
            ax.set_xlabel(xlabel)
        if ylabel:
            ax.set_ylabel(ylabel)
        if grid:
            ax.grid()
        if labels:
            ax.legend()

    else:
        plot_handles = ax.lines

        if len(plot_handles) < len(y):
            raise ValueError(f"len(ax.lines) = {len(plot_handles):d} < len(y) = {len(y):d}")
        if len(ax.texts) < 1:
            raise ValueError(f"len(ax.texts) = {len(ax.texts)} < 1")

        for handle, data in zip(plot_handles, y):
            if append:
                previous = handle.get_ydata()
            else:
                previous = None
            handle.set_data(*_plot_data(data, prev=previous))
        ax.texts[0].set_text(comment)

        ax.relim()
        ax.autoscale_view()

    return ax


def plot_diagonal(reference, prediction, replace=False, ax=None, xlabel="Reference", ylabel="Prediction", nmax=None, **kwargs):
    """
    Diagonal plot "reference" vs "data".

    Parameters
    ----------
    reference : np.ndarray
        Reference values.
    prediction : np.ndarray
        Predicted values.
    replace : bool
        If True and `ax` set, attempts to find previous data
        on the plot and to re-plot it.
    ax : Axes
        `matplotlib` axes to plot on.
    xlabel : str
        x axis label.
    ylabel : str
        y axis label.
    nmax : int
        Displays only few most outstanding values.
    kwargs
        Arguments to `pyplot.scatter`.

    Returns
    -------
    ax : Axes
        `matplotlib` axis.
    """
    _kwargs = dict(ls="none", marker="+")
    _kwargs.update(kwargs)

    reference = np.array(reference)
    prediction = np.array(prediction)
    reference.shape = reference.size,
    prediction.shape = prediction.size,

    mn = min(reference.min(), prediction.min())
    mx = max(reference.max(), prediction.max())
    diag = np.array([mn, mx])

    rmse = np.linalg.norm(reference - prediction) / reference.size ** .5
    rmse_text = f"RMSE = {rmse:.3e}"

    if nmax is not None:
        delta = np.abs(reference - prediction)
        ind = np.argpartition(delta, -nmax)[-nmax:]
        reference = reference[ind]
        prediction = prediction[ind]

    if ax is None or not replace:
        if ax is None:
            ax = pyplot.gca()
        ax.plot(reference, prediction, **_kwargs)
        ax.plot(diag, diag, color="black", zorder=10)

        ax.text(0.05, 0.9, rmse_text, transform=ax.transAxes, ha="left", va="top")

        if xlabel:
            ax.set_xlabel(xlabel)
        if ylabel:
            ax.set_ylabel(ylabel)
        ax.set_aspect(1)

    else:
        plot_handles = ax.lines
        if len(plot_handles) != 2:
            raise ValueError(f"Expected two lines, found: {len(plot_handles):d}")
        plot_handles[0].set_data(reference, prediction)
        plot_handles[1].set_data(diag, diag)
        ax.relim()
        ax.autoscale_view()

        text_handles = ax.texts
        if len(text_handles) != 1:
            raise ValueError(f"Expected one text, found: {len(text_handles):d}")

        text_handles[0].set_text(rmse_text)

    return ax
