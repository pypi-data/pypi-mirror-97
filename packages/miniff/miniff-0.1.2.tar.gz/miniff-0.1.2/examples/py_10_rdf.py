# Plots the radial distribution function

from miniff.kernel import NeighborWrapper, Cell
from miniff.presentation import plot_rdf

import numpy as np
from numericalunits import angstrom
from matplotlib import pyplot

from pathlib import Path
import json

script_location = Path(__file__).parent

with open(script_location / ".." / "datasets" / "bise.json", 'r') as f:
    c = Cell.from_json(json.load(f))

r = np.linspace(0, 10 * angstrom)
nw = NeighborWrapper(c, x=(2, 2, 2))
nw.compute_distances(max(r) + 1 * angstrom)
rdf = nw.rdf(r, r[1] - r[0])
plot_rdf(r, rdf)
pyplot.savefig(script_location / "10-rdf.svg")
