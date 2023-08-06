from . import ml_util
from .ml import NNPotential, Normalization, SequentialSoleEnergyNN
from .potentials import behler2_descriptor_family as behler2, behler4_descriptor_family as behler4

from .test_ml import assert_datasets_equal

from unittest import TestCase
from pathlib import Path
from numericalunits import aBohr, angstrom, eV
from collections import Counter
import numpy as np
from numpy import testing
import torch

test_location = Path(__file__).parent
dataset_location = test_location.parent / "datasets"


class RunnerParserTest(TestCase):
    def test_file(self):
        with open(dataset_location / "bise-descriptors-runner.txt", 'r') as f:
            d_parsed = ml_util.parse_runner_input(f)

        # Descriptors excluded from the long list
        d_blacklisted = [
            # Both two-point descriptors eta=0.3 targeting Te
            behler2(eta=0.3 / aBohr ** 2, r_sphere=0, a=12.0 * aBohr, tag=f"Ge-Te"),
            behler2(eta=0.3 / aBohr ** 2, r_sphere=0, a=12.0 * aBohr, tag=f"Te-Te"),
            # A single one for eta=0.2, zeta=4, l=-1
            behler4(eta=0.2 / aBohr ** 2, l=-1, zeta=4.0, a=12 * aBohr, tag=f"Te-Te-Te"),
            # A block at eta=0.2, zeta=16, l=-1 (except Te-Te-Ge)
            behler4(eta=0.2 / aBohr ** 2, l=-1, zeta=16.0, a=12 * aBohr, tag=f"Ge-Ge-Ge"),
            behler4(eta=0.2 / aBohr ** 2, l=-1, zeta=16.0, a=12 * aBohr, tag=f"Ge-Te-Ge"),
            behler4(eta=0.2 / aBohr ** 2, l=-1, zeta=16.0, a=12 * aBohr, tag=f"Ge-Te-Te"),
            behler4(eta=0.2 / aBohr ** 2, l=-1, zeta=16.0, a=12 * aBohr, tag=f"Te-Ge-Ge"),
            behler4(eta=0.2 / aBohr ** 2, l=-1, zeta=16.0, a=12 * aBohr, tag=f"Te-Te-Te"),
            # Two "Te" descriptors eta=0.001, zeta=16, l=1
            behler4(eta=0.001 / aBohr ** 2, l=1, zeta=16.0, a=13 * aBohr, tag=f"Te-Ge-Ge"),
            behler4(eta=0.001 / aBohr ** 2, l=1, zeta=16.0, a=13 * aBohr, tag=f"Te-Te-Te"),
            # All eta=0.3, zeta=4, l=-1 descriptors in the last block
            behler4(eta=0.3 / aBohr ** 2, l=-1, zeta=4.0, a=12 * aBohr, tag=f"Ge-Ge-Ge"),
            behler4(eta=0.3 / aBohr ** 2, l=-1, zeta=4.0, a=12 * aBohr, tag=f"Te-Ge-Ge"),
        ]

        d_full = []
        # 2-point
        # =======
        # cutoff=12
        for eta in 0.3, 0.2, 0.07, 0.03, 0.01, 0.001:
            for a1 in "Ge", "Te":
                for a2 in "Ge", "Te":
                    d_full.append(behler2(eta=eta / aBohr ** 2, r_sphere=0, a=12.0 * aBohr, tag=f"{a1}-{a2}"))

        # cutoff=13 eta=0.001
        for a1 in "Ge", "Te":
            for a2 in "Ge", "Te":
                d_full.append(behler2(eta=0.001 / aBohr ** 2, r_sphere=0, a=13.0 * aBohr, tag=f"{a1}-{a2}"))

        # 3-point
        # =======
        # primary block, cutoff=12 eta!=0.3
        for eta in 0.2, 0.07, 0.03, 0.01, 0.001:
            for zeta in 1, 4, 2, 16:
                for l in 1, -1:
                    for a1 in "Ge", "Te":
                        for a23 in "Ge-Ge", "Te-Ge", "Te-Te":
                            d_full.append(behler4(eta=eta / aBohr ** 2, l=l, zeta=zeta, a=12 * aBohr, tag=f"{a1}-{a23}"))

        # cutoff=13 eta=0.001
        for zeta in 1, 4, 2, 16:
            for l in 1, -1:
                for a1 in "Ge", "Te":
                    for a23 in "Ge-Ge", "Te-Ge", "Te-Te":
                        d_full.append(behler4(eta=0.001 / aBohr ** 2, l=l, zeta=zeta, a=13 * aBohr, tag=f"{a1}-{a23}"))

        # eta=0.3 cutoff=12 *-Ge-Ge
        for zeta in 1, 4, 2:
            for l in 1, -1:
                for a1 in "Ge", "Te":
                    d_full.append(behler4(eta=0.3 / aBohr ** 2, l=l, zeta=zeta, a=12 * aBohr, tag=f"{a1}-Ge-Ge"))

        # remove blacklisted
        id_parsed = tuple(map(repr, d_parsed))
        id_blacklisted = tuple(map(repr, d_blacklisted))
        id_full = tuple(map(repr, d_full))

        self.assertEqual(set(id_full), set(id_parsed) | set(id_blacklisted))


class LAMMPSParserTest(TestCase):
    def test_file(self):
        with open(dataset_location / "sio2-lammps", 'r') as f:
            potentials = ml_util.parse_lammps_input(f)

        self.assertEqual(len(potentials), 2)

        potential_sample = potentials[0]
        self.assertIsInstance(potential_sample, NNPotential)
        self.assertEqual(potential_sample.tag, "O")
        self.assertEqual(len(potential_sample.parameters["descriptors"]), 70)

        descriptor_sample = potential_sample.parameters["descriptors"][4]
        self.assertIs(descriptor_sample.family, behler2)
        testing.assert_equal(descriptor_sample.parameters["eta"], 0.214264 / angstrom ** 2)
        testing.assert_equal(descriptor_sample.parameters["a"], 6 * angstrom)
        testing.assert_equal(descriptor_sample.parameters["r_sphere"], 0)
        testing.assert_equal(descriptor_sample.tag, "O-Si")

        descriptor_sample = potential_sample.parameters["descriptors"][37]
        self.assertIs(descriptor_sample.family, behler4)
        testing.assert_equal(descriptor_sample.parameters["eta"], 0.000357 / angstrom ** 2)
        testing.assert_equal(descriptor_sample.parameters["a"], 6 * angstrom)
        testing.assert_equal(descriptor_sample.parameters["zeta"], 2)
        testing.assert_equal(descriptor_sample.parameters["l"], -1)
        testing.assert_equal(descriptor_sample.tag, "O-Si-O")

        potential_sample = potentials[1]
        self.assertIsInstance(potential_sample, NNPotential)
        self.assertEqual(potential_sample.tag, "Si")
        self.assertEqual(len(potential_sample.parameters["descriptors"]), 70)

        descriptor_sample = potential_sample.parameters["descriptors"][10]
        self.assertIs(descriptor_sample.family, behler2)
        testing.assert_equal(descriptor_sample.parameters["eta"], 0.071421 / angstrom ** 2)
        testing.assert_equal(descriptor_sample.parameters["a"], 6 * angstrom)
        testing.assert_equal(descriptor_sample.parameters["r_sphere"], 0)
        testing.assert_equal(descriptor_sample.tag, "Si-O")

        descriptor_sample = potential_sample.parameters["descriptors"][42]
        self.assertIs(descriptor_sample.family, behler4)
        testing.assert_equal(descriptor_sample.parameters["eta"], 0.089277 / angstrom ** 2)
        testing.assert_equal(descriptor_sample.parameters["a"], 6 * angstrom)
        testing.assert_equal(descriptor_sample.parameters["zeta"], 4)
        testing.assert_equal(descriptor_sample.parameters["l"], -1)
        testing.assert_equal(descriptor_sample.tag, "Si-Si-O")

        self.assertIs(potentials[0].parameters["normalization"], potentials[1].parameters["normalization"])
        self.assertEqual(potentials[0].parameters["normalization_handle"], 0)
        self.assertEqual(potentials[1].parameters["normalization_handle"], 1)

        normalization = potentials[0].parameters["normalization"]
        self.assertIs(normalization.dtype, torch.float64)
        testing.assert_equal(normalization.energy_scale.item(), eV)
        testing.assert_equal(normalization.energy_offsets.numpy(), np.zeros((2, 1)))
        # O
        testing.assert_equal(normalization.features_offsets[0].numpy()[15:20],
            [0.001286592108231314, 1.615018174190524, 0.8992337695059681, 0.2891024449138566, 0.9410533294211596])
        testing.assert_equal(normalization.features_scale[0].numpy()[40:45, 40:45], np.diag(
            [0.690412761572473, 0.33830388432626607, 0.08148770379598626, 5.344496403824106, 2.9638922703877952]))
        # Si
        testing.assert_equal(normalization.features_offsets[1].numpy()[0:5],
            [2.9579656875347435, 2.010843911436129, 1.3495712305969263, 0.7817472414666415, 0.3489072530470396])
        testing.assert_equal(normalization.features_scale[1].numpy()[0:5, 0:5], np.diag(
            [0.7019746179904176, 0.530114971386907, 0.40562997229952297, 0.2792499782562679, 0.16943875861884494]))

        nn_sample = potentials[0].parameters["nn"]
        self.assertEqual(len(nn_sample), 5)
        for i in range(0, 5, 2):
            layer = nn_sample[i]
            self.assertIsInstance(layer, torch.nn.Linear, msg=f"#{i:d}")
            self.assertIs(layer.weight.dtype, torch.float64, msg=f"#{i:d}")
            self.assertIs(layer.bias.dtype, torch.float64, msg=f"#{i:d}")
        for i in range(1, 5, 2):
            self.assertIsInstance(nn_sample[i], torch.nn.Sigmoid, msg=f"#{i:d}")

        linear_sample = nn_sample[2]
        testing.assert_equal(linear_sample.weight.detach().numpy()[2, 3:6], [0.5721273035047503, 0.10739355013492079,
                                                                             0.5264601494420822])
        testing.assert_equal(linear_sample.bias.detach().numpy()[4:6], [-0.194013890882, -0.691780401616])

        nn_sample = potentials[1].parameters["nn"]
        linear_sample = nn_sample[4]
        testing.assert_equal(linear_sample.weight.detach().numpy()[0, 5:7], [-0.1973799972276568, 0.4005192115707977])
        testing.assert_equal(linear_sample.bias.detach().item(), 0.132187475486)


class UtilTest(TestCase):
    def test_default_behler_choice(self):
        descriptors = ml_util.default_behler_descriptors({"a-a": 2, "a-b": 3, "b-b": 4}, 6, 12)
        self.assertEqual(len(descriptors), 2)

        self.assertEqual(Counter(i.tag for i in descriptors['a']), {"a-a": 6, "a-b": 6})
        self.assertEqual(Counter(i.tag for i in descriptors['b']), {"b-a": 6, "b-b": 6})

    def test_default_behler_choice_3(self):
        descriptors = ml_util.default_behler_descriptors_3(("a", "b"), 12)
        self.assertEqual(len(descriptors), 2)

        self.assertEqual(Counter(i.tag for i in descriptors['a']), {"a-a-a": 8, "a-a-b": 8, "a-b-b": 8})
        self.assertEqual(Counter(i.tag for i in descriptors['b']), {"b-a-a": 8, "b-a-b": 8, "b-b-b": 8})


class WorkflowTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = workflow = ml_util.FitWorkflow(seed=0)
        workflow.prepare(
            fn_cells=["bise-50.json"],
            neighbor_x=(2, 2, 2),
            fn_cells_root=Path(__file__).parent / ".." / "datasets",
            cells_subset=100,
        )
        workflow.run(n_epochs=1)

    def test_default(self):
        workflow = self.workflow

        self.assertEqual(len(workflow.cells), 100)
        self.assertEqual(len(workflow.descriptors), 2)
        for k, v in workflow.descriptors.items():
            self.assertEqual(len(v), 36, msg=k)
        testing.assert_allclose(workflow.cutoff, 12 * aBohr)
        self.assertEqual(len(workflow.cells_nw), 100)
        self.assertIs(workflow.dataset, None)
        self.assertIsInstance(workflow.normalization, Normalization)
        self.assertIsInstance(workflow.scale_eV_per_atom, float)
        self.assertEqual(workflow.dataset_normalized.per_cell_dataset.n_samples, 100)
        self.assertEqual(len(workflow.dataset_normalized.per_point_datasets), 2)
        for i in workflow.dataset_normalized.per_point_datasets:
            self.assertEqual(i.n_samples, 100)
            self.assertIn(i.n_species, (26, 39))
            self.assertEqual(i.n_features, 36)
        self.assertEqual(len(workflow.nn), 2)
        for i in workflow.nn:
            self.assertIsInstance(i, SequentialSoleEnergyNN)
        self.assertIsInstance(workflow.closure, ml_util.SimpleClosure)
        self.assertIsInstance(workflow.closure.last_loss.loss_value.detach().item(), float)
        self.assertIs(workflow.nn_potentials, None)

    def test_parallel(self):
        workflow = ml_util.FitWorkflow(seed=0)
        workflow.prepare(
            fn_cells=["bise-50.json"],
            neighbor_x=(2, 2, 2),
            fn_cells_root=Path(__file__).parent / ".." / "datasets",
            cells_subset=100,
            parallel=True,
            parallel_descriptor_chunksize=50,
        )

        assert_datasets_equal(self.workflow.dataset_normalized, workflow.dataset_normalized)
