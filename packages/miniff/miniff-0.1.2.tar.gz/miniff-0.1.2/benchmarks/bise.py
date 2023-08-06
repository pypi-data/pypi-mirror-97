from miniff.ml import NNPotential
from miniff.kernel import NeighborWrapper
from torch import load
from dfttools.simple import parse

from pathlib import Path

script_location = Path(__file__).parent
data_location = script_location / ".." / "datasets"

potentials = tuple(map(NNPotential.from_state_dict, load(data_location / "bise.pt")))
cutoff = max(i.cutoff for i in potentials)

with open(data_location / "bise.json", 'r') as f:
    c = parse(f, "unit-cell")

w = NeighborWrapper(c, x=(2, 2, 2))
w.compute_distances(cutoff)
for i in range(10):
    print(w.total(potentials), w.grad(potentials))
