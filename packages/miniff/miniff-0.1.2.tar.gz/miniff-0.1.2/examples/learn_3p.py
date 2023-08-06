from miniff import kernel, ml, presentation, ml_util

import numpy as np
from matplotlib import pyplot
from numericalunits import Ry, angstrom
import torch

torch.set_default_dtype(torch.float64)  # to not mess with 32 <-> 64 conversion

# Generate the dataset
min_distance = 1 * angstrom
cells = ml_util.prepare_dataset(100, 1 * angstrom, seed=0, size=3, min_distance=min_distance)  # 100 samples, 10 p per sample
cells_p = cells[0].meta["classic-potentials"]  # extract the potential used in the dataset

# Plot RDF
pyplot.figure()
r = np.linspace(0.1, 6) * angstrom
dr = r[1] - r[0]  # smearing
rdf = kernel.batch_rdf(cells, r, dr)
presentation.plot_rdf(r, rdf)

# Pick pair descriptors
descriptor_cutoff = 3 * angstrom
descriptors = ml_util.default_behler_descriptors(cells, 5, descriptor_cutoff, left=0.5)  # middle arg=descriptor count per pair
presentation.plot_descriptors_2(descriptors)
pyplot.show()

# Compute the dataset
dataset, normalization = ml.learn_cauldron(cells, descriptors, norm_kwargs=dict(offset_energy=False))

# Learn
networks = list(ml.SequentialSoleEnergyNN(i.n_features, n_layers=1, bias=False) for i in dataset.per_point_datasets)
closure = ml_util.simple_energy_closure(networks, dataset, optimizer=torch.optim.LBFGS)
closure.optimizer.max_iter = 1000
for lr in 1, .1, .01:
    closure.optimizer.lr = lr
    closure.optimizer_step()

# Show diagonal plot
loss = closure.loss()
pyplot.figure()
ac = normalization.atom_counts(dataset)
presentation.plot_diagonal(
    normalization.bw_energy(loss.reference, ac).detach().numpy() / Ry,
    normalization.bw_energy(loss.prediction, ac).detach().numpy() / Ry,
    xlabel="Reference (Ry)",
    ylabel="Prediction (Ry)",
)
pyplot.show()

# Construct potential
cells_p_ml = ml.potentials_from_ml_data(networks, descriptors, normalization)

# Plot
pyplot.figure()
limits = min_distance, descriptor_cutoff
for p in cells_p:
    presentation.plot_potential_2(p, limits=limits, label=p.tag, ls="--")

for p in cells_p_ml:
    presentation.plot_potential_2(p, limits=limits, label=f"{p.tag} (ml)", pair="a-a")

pyplot.legend()
pyplot.show()
