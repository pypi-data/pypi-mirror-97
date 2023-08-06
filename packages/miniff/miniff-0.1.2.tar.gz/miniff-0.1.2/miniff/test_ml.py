from . import ml, kernel, potentials, ml_util

from unittest import TestCase
import numpy as np
from numpy import testing
import torch
from itertools import chain, product
import tempfile

from .test_potentials import assert_potentials_allclose


def assert_with_tensors(f):
    def _f(d1, d2, **kwargs):
        if isinstance(d1, torch.Tensor):
            d1 = d1.detach().numpy()
        if isinstance(d2, torch.Tensor):
            d2 = d2.detach().numpy()
        return f(d1, d2, **kwargs)
    return _f


assert_equal = assert_with_tensors(testing.assert_equal)
assert_allclose = assert_with_tensors(testing.assert_allclose)


def assert_datasets_equal(d1: ml.Dataset, d2: ml.Dataset, **kwargs):
    assert_equal(len(d1), len(d2))
    grad_pc = d1.per_cell_dataset.is_gradient_available()
    assert_equal(grad_pc, d2.per_cell_dataset.is_gradient_available())
    assert_allclose(d1.per_cell_dataset.energy, d2.per_cell_dataset.energy)
    if grad_pc:
        assert_allclose(d1.per_cell_dataset.energy_g, d2.per_cell_dataset.energy_g, **kwargs)
        assert_equal(d1.per_cell_dataset.mask, d2.per_cell_dataset.mask)

    for i, j in zip(d1.per_point_datasets, d2.per_point_datasets):
        assert_allclose(i.features, j.features, **kwargs)

        if i.features_g is None:
            assert_equal(i.features_g, j.features_g)
        else:
            assert_allclose(i.features_g, j.features_g, **kwargs)

        if i.charges is None:
            assert_equal(i.charges, j.charges)
        else:
            assert_allclose(i.charges, j.charges, **kwargs)

        assert_equal(i.mask, j.mask)


def assert_torch_modules_equal(a: torch.nn.Module, b: torch.nn.Module, err_msg="", **kwargs):
    p1 = tuple(a.parameters())
    p2 = tuple(b.parameters())
    testing.assert_equal(len(p1), len(p2), err_msg=err_msg)
    for i, (_p1, _p2) in enumerate(zip(p1, p2)):
        assert_equal(_p1.data, _p2.data, err_msg=f"{err_msg} #{i}", **kwargs)


def assert_normalizations_allclose(a: ml.Normalization, b: ml.Normalization, err_msg="", **kwargs):
    for field in "energy_scale", "energy_offsets", "length_scale":
        _a = getattr(a, field)
        _b = getattr(b, field)
        if _a is None or _b is None:
            testing.assert_equal(_a, _b, err_msg=f"{err_msg} {field}", **kwargs)
        else:
            assert_allclose(_a, _b, err_msg=f"{err_msg} {field}", **kwargs)

    for field in "features_scale", "features_offsets":
        _a = getattr(a, field)
        _b = getattr(b, field)
        testing.assert_equal(len(_a), len(_b), err_msg=f"{err_msg} {field}")
        for i, (_i, _j) in enumerate(zip(_a, _b)):
            assert_allclose(_i, _j, err_msg=f"{err_msg} {field} #{i}", **kwargs)


def assert_nn_potentials_allclose(a: ml.NNPotential, b: ml.NNPotential, err_msg="", **kwargs):
    pa = a.parameters.copy()
    pb = b.parameters.copy()
    testing.assert_equal(pa.keys(), pb.keys(), err_msg=err_msg)
    assert_torch_modules_equal(pa.pop("nn"), pb.pop("nn"), err_msg=err_msg)
    da = pa.pop("descriptors")
    db = pb.pop("descriptors")
    testing.assert_equal(len(da), len(db), err_msg=err_msg)
    for _d1, _d2 in zip(da, db):
        assert_potentials_allclose(_d1, _d2, err_msg=err_msg, **kwargs)
    na = pa.pop("normalization")
    nb = pb.pop("normalization")
    if na is None or nb is None:
        testing.assert_equal(na, nb, err_msg=err_msg)
    else:
        assert_normalizations_allclose(na, nb, err_msg=err_msg, **kwargs)
    nha = pa.pop("normalization_handle")
    nhb = pb.pop("normalization_handle")
    testing.assert_equal(nha, nhb, err_msg=err_msg)
    testing.assert_equal(len(pa), 0, err_msg=err_msg)
    testing.assert_equal(len(pb), 0, err_msg=err_msg)

    testing.assert_equal(a.coordination_number, b.coordination_number, err_msg=err_msg)
    testing.assert_allclose(a.cutoff, b.cutoff, err_msg=err_msg, **kwargs)


class LJBoxTest(TestCase):
    @staticmethod
    def prep_cells(cells, cutoff, interaction=None):
        result = []
        for i in cells:
            w = kernel.NeighborWrapper(i, cutoff=cutoff)
            if interaction is not None:
                w.meta["total-energy"] = w.total(interaction, ignore_missing_species=True)
                w.meta["partial-energy"] = w.eval(interaction, "kernel", ignore_missing_species=True, squeeze=False, resolved=True).sum(axis=0)
                assert_allclose(w.meta["total-energy"], w.meta["partial-energy"].sum())
                w.meta["forces"] = - w.grad(interaction, ignore_missing_species=True)
            result.append(w)
        return result

    @staticmethod
    def assign_charges(cells, p):
        for w in cells:
            w.meta["charges"] = w.eval(p, "kernel", squeeze=False, ignore_missing_species=True).sum(axis=0)

    @classmethod
    def setUpClass(cls, x_fr=10, x_to=10, y_fr=0, y_to=0, charges=False) -> None:
        cls.descriptors = dict(
            x=[
                potentials.sigmoid_descriptor_family(r0=.5, dr=.1, a=1, tag='x-x'),
                potentials.behler2_descriptor_family(r_sphere=.5, eta=1, a=3, tag='x-x'),
                potentials.behler2_descriptor_family(r_sphere=0, eta=0.01, a=3, tag='x-y'),
            ], y=[
                potentials.sigmoid_descriptor_family(r0=.5, dr=.1, a=1, tag='y-y'),
                potentials.behler2_descriptor_family(r_sphere=.5, eta=1, a=2, tag='y-y'),
            ]
        )
        cls.n_samples = 20
        cls.interaction = [
            potentials.harmonic_repulsion_potential_family(a=1.1, epsilon=1, tag='x-x'),
            potentials.harmonic_repulsion_potential_family(a=.5, epsilon=1, tag='x-y'),
            potentials.harmonic_repulsion_potential_family(a=.5, epsilon=1, tag='y-x'),
            potentials.harmonic_repulsion_potential_family(a=1.7, epsilon=1, tag='y-y'),
        ]
        np.random.seed(0)
        cls.per_cell = dict(
            x=np.random.randint(x_fr, x_to + 1, cls.n_samples),
            y=np.random.randint(y_fr, y_to + 1, cls.n_samples),
        )
        cls.n_atoms = cls.per_cell['x'] + cls.per_cell['y']
        cls.cell_offsets = np.concatenate((
            [0],
            np.cumsum(cls.per_cell["x"] + cls.per_cell["y"]),
        ))
        coords = np.random.rand(cls.cell_offsets[-1], 3)
        cls.cells = tuple(
            kernel.Cell(np.eye(3) * 3, coords[fr:to], ["x"] * n_x + ["y"] * n_y)
            for n_x, n_y, fr, to in zip(cls.per_cell["x"], cls.per_cell["y"], cls.cell_offsets[:-1], cls.cell_offsets[1:])
        )
        for c in cls.cells:
            np.random.shuffle(c.values)

        if x_fr == x_to == 0:
            del cls.descriptors["x"]
            del cls.per_cell["x"]
            cls.interaction = [i for i in cls.interaction if 'x' not in i.tag]
        if y_fr == y_to == 0:
            del cls.descriptors["y"]
            del cls.per_cell["y"]
            if "x" in cls.descriptors:
                cls.descriptors["x"] = list(i for i in cls.descriptors["x"] if "y" not in i.tag)
            cls.interaction = [i for i in cls.interaction if 'y' not in i.tag]

        cls.cells_wrapped = cls.prep_cells(cls.cells, 5.1, interaction=cls.interaction)
        if charges:
            cls.charge_descriptors = dict(
                x=[potentials.harmonic_repulsion_potential_family(a=1.1, epsilon=1, tag='x-y')],
                y=[potentials.harmonic_repulsion_potential_family(a=1.1, epsilon=-1, tag='y-x')],
            )
            cls.assign_charges(cls.cells_wrapped, [
                cls.charge_descriptors['x'][0],
                cls.charge_descriptors['y'][0],
            ])
        cls.setUpLearning(charges=charges)

    @classmethod
    def setUpLearning(cls, charges=False):
        cls.cells_wrapped_trivial = cls.prep_cells(cls.cells, 5.1, interaction=cls.descriptors.get('x', []) + cls.descriptors.get('y', []))
        if charges:
            cls.assign_charges(cls.cells_wrapped_trivial, [
                cls.charge_descriptors['x'][0],
                cls.charge_descriptors['y'][0],
            ])
        cls.descriptor_collection_trivial = cls.descriptors

    def __prep_unity_modules__(self, normalization=None, random=False, descriptors=None, n_layers=1, n_internal=15,
                               bias=True):
        if descriptors is None:
            descriptors = self.descriptor_collection_trivial
        if random:
            torch.manual_seed(0)
        modules = list(
            ml.SequentialSoleEnergyNN(len(v), n_layers=n_layers, n_internal=n_internal, bias=bias)
            for k, v in sorted(descriptors.items())
        )
        if not random:
            if n_layers != 1:
                raise ValueError("Unity module has only a single layer")
            for i, m in enumerate(modules):
                if normalization is None:
                    m[0].weight.data[:] = 1
                    m[0].bias.data[:] = 0
                else:
                    m[0].weight.data[:] = torch.diag(normalization.features_scale[i]) / normalization.energy_scale
                    m[0].bias.data[:] = (normalization.features_offsets[i].sum() - normalization.energy_offsets[i]) / normalization.energy_scale
        return modules

    def __test_shapes__(self, dataset, grad, grad_pc=True, charges=False, energies_p=False):
        assert_equal(dataset.dtype, torch.float64)
        assert_equal(len(dataset), self.n_samples)
        assert_equal(dataset.per_cell_dataset.is_gradient_available(), grad_pc)
        for i in dataset.per_point_datasets:
            assert_equal(i.is_gradient_available(), grad)

        assert_equal(dataset.per_cell_dataset.dtype, torch.float64)
        assert_equal(dataset.per_cell_dataset.n_samples, self.n_samples)
        if grad_pc:
            assert_equal(dataset.per_cell_dataset.n_atoms, self.n_atoms.max())
            assert_equal(dataset.per_cell_dataset.n_coords, 3)
        else:
            self.assertIs(dataset.per_cell_dataset.n_atoms, None)
            self.assertIs(dataset.per_cell_dataset.n_coords, None)
        assert_equal(dataset.per_cell_dataset.energy.shape, (self.n_samples, 1))
        if grad_pc:
            assert_equal(dataset.per_cell_dataset.energy_g.shape, (self.n_samples, self.n_atoms.max(), 3))
            assert_equal(dataset.per_cell_dataset.mask.shape, (self.n_samples, self.n_atoms.max()))
        n_atoms_max = max(self.n_atoms)

        assert_equal(len(dataset.per_point_datasets), len(self.descriptors))
        for i_k, k in enumerate(sorted(self.descriptors.keys())):
            n_species_max = max(self.per_cell[k])
            ppd = dataset.per_point_datasets[i_k]
            assert_equal(ppd.dtype, torch.float64)
            assert_equal(ppd.n_samples, self.n_samples)
            assert_equal(ppd.n_species, n_species_max)
            assert_equal(ppd.n_features, len(self.descriptors[k]))
            if grad:
                assert_equal(ppd.n_atoms, n_atoms_max)
                assert_equal(ppd.n_coords, 3)
            else:
                self.assertIs(ppd.n_atoms, None)
                self.assertIs(ppd.n_coords, None)

            assert_equal(ppd.features.shape, [self.n_samples, n_species_max, len(self.descriptors[k])])
            if grad:
                assert_equal(ppd.features_g.shape, [self.n_samples, n_species_max, len(self.descriptors[k]),
                                                    n_atoms_max, 3])
            if energies_p:
                assert_equal(ppd.energies_p.shape, (self.n_samples, n_species_max, 1))
            assert_equal(ppd.mask.shape, [self.n_samples, n_species_max])

            if charges:
                assert_equal(ppd.charges.shape, [self.n_samples, n_species_max, 1])
            else:
                self.assertIs(ppd.charges, None)

    def __test_ranges_std__(self, dataset, charges=False):
        assert_equal(dataset.per_cell_dataset.energy,
                             np.array(tuple(i.meta["total-energy"] for i in self.cells_wrapped))[:, np.newaxis])

        for ppd in dataset.per_point_datasets:
            assert_equal(ppd.features >= 0, np.ones_like(ppd.features))
            assert_equal(ppd.features < 6, np.ones_like(ppd.features))  # some effective coordination number
            if charges:
                assert_equal(ppd.charges > -6, np.ones_like(ppd.charges))
                assert_equal(ppd.charges < 6, np.ones_like(ppd.charges))

    def __test_ranges_nrm__(self, dataset, charges=False):
        assert_allclose(
            dataset.per_cell_dataset.energy.max().item() - dataset.per_cell_dataset.energy.min().item(), 1)

        for i_k, k in enumerate(sorted(self.descriptors.keys())):
            ppd = dataset.per_point_datasets[i_k]
            mn, _ = ppd.features[ppd.mask != 0, :].min(dim=0)
            mx, _ = ppd.features[ppd.mask != 0, :].max(dim=0)
            ref = np.ones(len(self.descriptors[k]))
            assert_allclose(mn, -ref)
            assert_allclose(mx, ref)
            if charges:
                mn = ppd.charges[ppd.mask != 0].min()
                mx = ppd.charges[ppd.mask != 0].max()
                # assert_allclose(mn, 0, atol=1e-14)  # Defaults changed
                # assert_allclose(mx, 1)  # Defaults changed
                assert_allclose(mx - mn, 1)

    def __test_mask__(self, dataset):
        for i_k, k in enumerate(sorted(self.descriptors.keys())):
            assert_equal(dataset.per_point_datasets[i_k].mask.sum(dim=1), self.per_cell[k])

    def __test_slicing__(self, dataset):
        s = slice(10, 20)
        sliced = ml.Dataset.from_tensors(dataset[s])
        dl = iter(torch.utils.data.DataLoader(dataset, batch_size=10))
        next(dl)
        sliced2 = ml.Dataset.from_tensors(next(dl))
        assert_datasets_equal(sliced, sliced2)

    def __test_slice_cat__(self, dataset):
        bounds = 0, self.n_samples // 3, self.n_samples // 2, self.n_samples
        datasets = list(ml.Dataset.from_tensors(dataset[i:j]) for i, j in zip(bounds[:-1], bounds[1:]))
        merged = ml.Dataset.cat(datasets)
        assert_datasets_equal(dataset, merged)

    def __test_normalization_reasonable__(self, normalization, grad, charges):
        self.assertIsInstance(normalization, ml.Normalization)

        testing.assert_array_less(0.1, normalization.energy_scale)
        testing.assert_array_less(normalization.energy_scale, 100)
        if grad:
            testing.assert_array_less(0.1, normalization.length_scale)
            testing.assert_array_less(normalization.length_scale, 10)
        else:
            self.assertIs(normalization.length_scale, None)

        for i_data, data in enumerate(normalization.features_scale):
            testing.assert_array_less(0.01, torch.diag(data), err_msg=f"#{i_data:d}")
            testing.assert_array_less(data, 10, err_msg=f"#{i_data:d}")

        for i_data, data in enumerate(normalization.features_offsets):
            testing.assert_array_less(0, data + 1e-12, err_msg=f"#{i_data:d}")
            testing.assert_array_less(data, 10, err_msg=f"#{i_data:d}")

        for i_data, data in enumerate(normalization.charges_scale):
            if charges:
                testing.assert_array_less(0, data + 1e-12, err_msg=f"#{i_data:d}")
                testing.assert_array_less(data, 6, err_msg=f"#{i_data:d}")
            else:
                self.assertIs(data, None)

        for i_data, data in enumerate(normalization.charges_offsets):
            if charges:
                testing.assert_array_less(-6, data + 1e-12, err_msg=f"#{i_data:d}")
                testing.assert_array_less(data - 1e-12, 0, err_msg=f"#{i_data:d}")
            else:
                self.assertIs(data, None)

        # testing.assert_array_less(0.01, normalization.energy_offsets)  # TODO Defaults changed
        # testing.assert_array_less(normalization.energy_offsets, 100)  # TODO Defaults changed
        testing.assert_equal(normalization.energy_offsets.numpy(), 0)

    def __gc__(self):
        if "charges" not in self.cells_wrapped[0].meta:
            return chain(product((False, True), (False,), (False,)), ((False, False, True),))
        else:
            return chain(product((False, True), (False, True), (False,)), ((False, False, True),))

    def test_integration(self):
        for grad, charges, energies_p in self.__gc__():
            dataset = ml.learn_cauldron(self.cells_wrapped, self.descriptors, grad=grad, normalize=False,
                                        extract_charges=charges, energies_p=energies_p)

            self.__test_shapes__(dataset, grad=grad, grad_pc=grad, charges=charges, energies_p=energies_p)
            self.__test_ranges_std__(dataset, charges=charges)
            self.__test_mask__(dataset)
            self.__test_slice_cat__(dataset)
            # self.__test_slicing__(dataset)  TODO: slicing fails because some tensors may be None

    def test_integration_norm(self):
        for grad, charges, energies_p in self.__gc__():
            dataset_ref = ml.learn_cauldron(self.cells_wrapped, self.descriptors, grad=grad, normalize=False,
                                            extract_charges=charges, energies_p=energies_p)
            if len(self.descriptors) == 1 and charges:
                # Only a single specimen: all charges are zero
                assert_equal(dataset_ref.charges, 0)
                with self.assertRaises(ValueError):
                    ml.learn_cauldron(self.cells_wrapped, self.descriptors, grad=grad, normalize=True,
                                      extract_charges=charges)
                dataset, norm_info = ml.learn_cauldron(self.cells_wrapped, self.descriptors, grad=grad, normalize=True,
                                                       extract_charges=charges, ignore_normalization_errors=True,
                                                       energies_p=energies_p)
            else:
                dataset, norm_info = ml.learn_cauldron(self.cells_wrapped, self.descriptors, grad=grad, normalize=True,
                                                       extract_charges=charges, energies_p=energies_p)

            self.__test_shapes__(dataset, grad=grad, grad_pc=grad, charges=charges)
            self.__test_ranges_nrm__(dataset, charges=charges)
            self.__test_mask__(dataset)
            self.__test_normalization_reasonable__(norm_info, grad=grad, charges=charges)

            dataset_bw = norm_info.bw(dataset, inplace=False)
            self.assertIsNot(dataset, dataset_bw)
            self.assertIsNot(dataset.per_cell_dataset.energy, dataset_bw.per_cell_dataset.energy)
            for ix1, (i, j) in enumerate(zip(dataset.per_point_datasets, dataset_bw.per_point_datasets)):
                for ix2, (k, l) in enumerate(zip(i.tensors, j.tensors)):
                    if not (k is l is None):
                        self.assertIsNot(k, l, msg=f"dataset #{ix1:d}, tensor #{ix2:d}")
            assert_datasets_equal(dataset_bw, dataset_ref, atol=1e-14)

            dataset_bw = norm_info.bw(dataset, inplace=True)
            self.assertIs(dataset, dataset_bw)
            assert_datasets_equal(dataset_bw, dataset_ref, atol=1e-14)

    def __test_modules_valid__(self, modules, normalization=None, **kwargs):
        degenerate = len(self.descriptors) == 2 and\
                     np.all(self.per_cell['x'] == self.per_cell['x'][0]) and\
                     np.all(self.per_cell['y'] == self.per_cell['y'][0])

        ref_modules = self.__prep_unity_modules__(normalization=normalization, random=False)

        for i, (module, ref_module) in enumerate(zip(modules, ref_modules)):
            assert_allclose(
                module[0].weight.detach(),
                ref_module[0].weight.detach(),
                err_msg=f"#{i}",
                **kwargs
            )
            if not degenerate:
                assert_allclose(
                    module[0].bias.detach(),
                    ref_module[0].bias.detach(),
                    err_msg=f"#{i}",
                    **kwargs
                )

        if degenerate:
            nx = self.per_cell['x'][0]
            ny = self.per_cell['y'][0]
            balance = modules[0][0].bias * nx + modules[1][0].bias * ny
            balance_ref = ref_modules[0][0].bias * nx + ref_modules[1][0].bias * ny
            assert_allclose(balance.detach(), balance_ref.detach(), **kwargs)

    def test_integration_ml_run(self):
        dataset = ml.learn_cauldron(self.cells_wrapped_trivial, self.descriptor_collection_trivial, grad=False, normalize=False)

        dataset = dataset.to(torch.float32)
        modules = self.__prep_unity_modules__(random=True)

        closure = ml_util.simple_energy_closure(modules, dataset=dataset, optimizer=torch.optim.LBFGS)
        self.assertLess(1, closure())  # Check if initial guess is not optimal

        for _ in range(2):  # Only one or two steps needed to reach convergence
            closure.optimizer_step()

        assert_allclose(closure().detach(), 0, atol=1e-6)  # TODO: this occasionally fails with atol=7.5e-5
        self.__test_modules_valid__(modules, atol=2e-3)  # TODO: this occasionally fails with atol=0.017

    def test_integration_ml_run_forces(self):
        dataset = ml.learn_cauldron(self.cells_wrapped_trivial, self.descriptor_collection_trivial, grad=True, normalize=False)
        for d in dataset.per_point_datasets:
            d.features.requires_grad = True

        dataset = dataset.to(torch.float32)
        modules = self.__prep_unity_modules__(random=True)

        closure = ml_util.simple_energy_closure(modules, dataset=dataset, optimizer=torch.optim.LBFGS, w_gradients=1)
        self.assertLess(1, closure())  # Check if initial guess is not optimal

        for _ in range(2):  # Only one or two steps needed to reach convergence
            closure.optimizer_step()

        assert_allclose(closure().detach(), 0, atol=1e-6)
        self.__test_modules_valid__(modules, atol=2e-3)

    def test_integration_dummy_ml_run_forces_slice(self):
        dataset = ml.learn_cauldron(self.cells_wrapped_trivial, self.descriptor_collection_trivial, grad=True, normalize=False)
        for d in dataset.per_point_datasets:
            d.features.requires_grad = True

        dataset = ml.Dataset.from_tensors(dataset.to(torch.float32)[10:20])
        modules = self.__prep_unity_modules__(random=True)

        closure = ml_util.simple_energy_closure(modules, dataset=dataset, optimizer=torch.optim.LBFGS, w_gradients=1)
        self.assertLess(1, closure())  # Check if initial guess is not optimal

        for _ in range(2):  # Only one or two steps needed to reach convergence
            closure.optimizer_step()

        assert_allclose(closure().detach(), 0, atol=1e-6)
        self.__test_modules_valid__(modules, atol=2e-3)

    def test_integration_ml_run_partial(self):
        dataset = ml.learn_cauldron(self.cells_wrapped_trivial, self.descriptor_collection_trivial, energies_p=True, normalize=False)

        dataset = dataset.to(torch.float32)
        modules = self.__prep_unity_modules__(random=True)

        closure = ml_util.simple_energy_closure(modules, dataset=dataset, optimizer=torch.optim.LBFGS, energies_p=True)
        self.assertLess(1, closure())  # Check if initial guess is not optimal TODO: this fails occasionally

        for _ in range(2):  # Only one or two steps needed to reach convergence
            closure.optimizer_step()

        assert_allclose(closure().detach(), 0, atol=1e-6)  # TODO: this fails occasionally at atol=5e-6
        self.__test_modules_valid__(modules, atol=2e-3)  # TODO: this fails occasionally at atol=0.02

    def test_integration_ml_run_norm(self):
        dataset, normalization = ml.learn_cauldron(
            self.cells_wrapped_trivial, self.descriptor_collection_trivial, grad=False,
            normalize=True, extract_forces=False
        )
        self.__test_normalization_reasonable__(normalization, grad=False, charges=False)

        for d in dataset.per_point_datasets:
            d.features.requires_grad = True

        dataset = dataset.to(torch.float32)
        normalization = normalization.to(torch.float32)
        modules = self.__prep_unity_modules__(normalization, random=True)

        closure = ml_util.simple_energy_closure(modules, dataset=dataset, optimizer=torch.optim.LBFGS)
        self.assertLess(.1, closure())  # Check if initial guess is not optimal

        for _ in range(2):  # Only one or two steps needed to reach convergence
            closure.optimizer_step()

        assert_allclose(closure().detach(), 0, atol=1e-6)
        self.__test_modules_valid__(modules, normalization=normalization, atol=2e-3)

    def test_cauldron_with_norm(self):
        # Test fw_cauldron w normalization
        dataset, normalization = ml.learn_cauldron(
            self.cells_wrapped_trivial, self.descriptor_collection_trivial, grad=True, normalize=True)
        dataset = dataset.to(torch.float32)
        normalization = normalization.to(torch.float32)
        dataset_not_normalized = ml.learn_cauldron(self.cells_wrapped_trivial, self.descriptor_collection_trivial,
                                                   grad=True, normalize=False).to(torch.float32)

        for d in dataset.per_point_datasets:
            d.features.requires_grad = True

        for d in dataset_not_normalized.per_point_datasets:
            d.features.requires_grad = True

        modules = self.__prep_unity_modules__(normalization)
        energy, gradients = ml.fw_cauldron(modules, dataset, grad=True, normalization=normalization)
        assert_allclose(energy.detach(), dataset_not_normalized.per_cell_dataset.energy, rtol=1e-4)
        assert_allclose(gradients.detach(), dataset_not_normalized.per_cell_dataset.energy_g, rtol=1e-4)

    def test_integration_ml_potential(self):
        modules = self.__prep_unity_modules__()

        ml_potentials = ml.potentials_from_ml_data(modules, self.descriptor_collection_trivial)
        for i in ml_potentials:
            i.kernels["kernel_gradient_d"] = potentials.num_grad_potential(i.kernels["kernel"])

        for i, cell in enumerate(self.cells_wrapped_trivial):
            energy = cell.total(ml_potentials, ignore_missing_species=True)
            assert_allclose(cell.meta["total-energy"], energy, err_msg=f"#{i:d}")

            grad = cell.grad(ml_potentials, ignore_missing_species=True)
            assert_allclose(cell.meta["forces"], - grad, err_msg=f"#{i:d}", atol=1e-6)

    def test_integration_ml_potential_norm(self):
        dataset, normalization = ml.learn_cauldron(
            self.cells_wrapped_trivial, self.descriptor_collection_trivial, grad=True, normalize=True)
        normalization = normalization.to(torch.float32)

        modules = self.__prep_unity_modules__(normalization=normalization)

        ml_potentials = ml.potentials_from_ml_data(
            modules, self.descriptor_collection_trivial, normalization=normalization)

        for i, cell in enumerate(self.cells_wrapped_trivial):
            energy = cell.total(ml_potentials, ignore_missing_species=True)
            assert_allclose(cell.meta["total-energy"], energy, err_msg=f"#{i:d}", atol=1e-6)

            grad = cell.grad(ml_potentials, ignore_missing_species=True)
            assert_allclose(cell.meta["forces"], - grad, err_msg=f"#{i:d}", atol=1e-5)

    def test_serialization_simple(self):
        ml_potentials = ml.potentials_from_ml_data(self.__prep_unity_modules__(), self.descriptor_collection_trivial)
        for p in ml_potentials:
            with tempfile.TemporaryFile() as f:
                torch.save(p, f)
                f.seek(0)
                ref = torch.load(f)
                self.assertIsNot(p, ref)
                assert_nn_potentials_allclose(p, ref, err_msg=f"{p.tag}")

    def test_serialization_state(self):
        ml_potentials = ml.potentials_from_ml_data(self.__prep_unity_modules__(), self.descriptor_collection_trivial)
        for p in ml_potentials:
            with tempfile.TemporaryFile() as f:
                torch.save(p.state_dict(), f)
                f.seek(0)
                ref = ml.NNPotential.from_state_dict(torch.load(f))
                assert_nn_potentials_allclose(p, ref, err_msg=f"{p.tag}")

    def test_serialization_state_norm(self):
        _, normalization = ml.learn_cauldron(
            self.cells_wrapped_trivial, self.descriptor_collection_trivial, grad=False, normalize=True)
        ml_potentials = ml.potentials_from_ml_data(self.__prep_unity_modules__(), self.descriptor_collection_trivial,
                                                   normalization)
        for p in ml_potentials:
            for units in False, True:
                with tempfile.TemporaryFile() as f:
                    torch.save(p.state_dict(units=units), f)
                    f.seek(0)
                    ref = ml.NNPotential.from_state_dict(torch.load(f))
                    assert_nn_potentials_allclose(p, ref, err_msg=f"{p.tag} units={units}")

    def test_serialization_non_standard(self):
        ml_potentials = ml.potentials_from_ml_data(
            self.__prep_unity_modules__(n_layers=5, random=True, n_internal=20, bias=False), self.descriptor_collection_trivial)
        for p in ml_potentials:
            with tempfile.TemporaryFile() as f:
                torch.save(p, f)
                f.seek(0)
                ref = torch.load(f)
                self.assertIsNot(p, ref)
                assert_nn_potentials_allclose(p, ref, err_msg=f"{p.tag}")
            with tempfile.TemporaryFile() as f:
                torch.save(p.state_dict(), f)
                f.seek(0)
                ref = ml.NNPotential.from_state_dict(torch.load(f))
                assert_nn_potentials_allclose(p, ref, err_msg=f"{p.tag}")


class UnalignedTestMixin:
    def test_padding_valid(self):
        # Dataset
        dataset = ml.learn_cauldron(self.cells_wrapped_trivial, self.descriptor_collection_trivial, grad=True,
                                    normalize=False)
        dataset = dataset.to(torch.float32)
        for d in dataset.per_point_datasets:
            d.features.requires_grad = True

        # Mask indicating padding entries
        mask = torch.ones(dataset.per_cell_dataset.n_samples, dataset.per_cell_dataset.n_atoms, dtype=torch.bool)
        for pp in dataset.per_point_datasets:
            mask &= dataset.per_cell_dataset.mask != pp.tag
        assert mask.sum() > 0

        # Random modules
        modules = list(ml.SequentialSoleEnergyNN(i.n_features) for i in dataset.per_point_datasets)

        # One step
        energy, gradients = ml.fw_cauldron(modules, dataset, grad=True)
        gradients = gradients.detach()

        assert_equal(gradients[mask, :], 0)


class LJBoxTestTwoComponent(LJBoxTest):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass(x_fr=4, x_to=4, y_fr=6, y_to=6)


class LJBoxTestUnaligned(UnalignedTestMixin, LJBoxTest):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass(x_fr=4, x_to=10, y_fr=0, y_to=0)


class LJBoxTestUnalignedTwoComponent(UnalignedTestMixin, LJBoxTest):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass(x_fr=4, x_to=10, y_fr=0, y_to=6)
        assert any(i == 0 for i in cls.per_cell["y"])


class LJBoxTestUnalignedTwoComponentCharges(UnalignedTestMixin, LJBoxTest):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass(x_fr=4, x_to=10, y_fr=0, y_to=6, charges=True)
        assert any(i == 0 for i in cls.per_cell["y"])
        assert any(np.abs(i.meta["charges"]).sum() > 0 for i in cls.cells_wrapped)

    def test_integration_charges(self):
        dataset, normalization = ml.learn_cauldron(
            self.cells_wrapped_trivial, self.charge_descriptors, grad=False,
            normalize=True, extract_forces=False, extract_charges=True,
        )

        for d in dataset.per_point_datasets:
            d.features.requires_grad = True

        dataset = dataset.to(torch.float32)
        normalization = normalization.to(torch.float32)
        # Following is just a duck-type: __prep_unity_modules__ won't prepare numerically correct modules
        # (i.e. random=False) for charges
        modules = self.__prep_unity_modules__(normalization=normalization, random=True,
                                              descriptors=self.charge_descriptors)

        closure = ml_util.simple_charges_closure(modules, dataset=dataset, optimizer=torch.optim.LBFGS)
        self.assertLess(.1, closure())  # Check if the initial guess is not optimal

        for _ in range(2):  # Only one or two steps needed to reach convergence
            closure.optimizer_step()

        assert_allclose(closure().detach(), 0, atol=1e-6)

        # In this test case charges are exactly equal to the corresponding descriptors up to normalization:
        # descriptors belong to [-1, 1] interval while charges belong to [0, 1] or [-1, 0] interval
        for i, module in enumerate(modules):
            assert_allclose(
                module[0].weight.detach(),
                [[.5]],
                err_msg=f"#{i}",
                atol=1e-4,
            )
            assert_allclose(
                module[0].bias.detach(),
                [[.5, -.5][i]],
                err_msg=f"#{i}",
                atol=1e-4,
            )


class PCATests(TestCase):
    def test_norm_truncation(self):
        n_samples = 100
        n_descriptors = 3
        n_atoms = 3

        descriptors = torch.rand(n_samples, n_atoms, n_descriptors, dtype=torch.float64) * 10 + 2

        # This normalization keeps first 2 descriptors and drops the last one
        norm = ml.Normalization(
            torch.scalar_tensor(1.0, dtype=torch.float64),
            [torch.tensor(np.array([(10.0, 0.0, 0.0), (0.0, 10.0, 0.0)]))],
            torch.tensor(np.array([[0.0]])),
            [torch.tensor(np.array([2.0, 2.0, 2.0]))],
        )

        descriptors_normalized = norm.fw_features(descriptors, 0)
        assert_allclose(
            descriptors_normalized,
            ((descriptors - 2) / 10)[..., :2],
        )
        descriptors_restored = norm.bw_features(descriptors_normalized, 0)
        assert_allclose(
            descriptors_restored[..., :2],
            descriptors[..., :2],
        )  # only first two descriptors can be restored

    def test_norm_pca(self):
        n_samples = 100
        n_descriptors = 2
        n_descriptors_degenerate = 3
        n_atoms = 4

        descriptors = torch.rand(n_samples, n_atoms, n_descriptors, dtype=torch.float64) * 10 + 2
        descriptors_linear = descriptors @ torch.rand(n_descriptors, n_descriptors_degenerate, dtype=torch.float64)
        descriptors = torch.cat([descriptors, descriptors_linear], dim=2)

        energies = torch.rand(n_samples, 1, dtype=torch.float64)
        mask = torch.ones(n_samples, n_atoms, dtype=torch.float64)

        dataset = ml.Dataset(
            ml.PerCellDataset(energies),
            ml.PerPointDataset(descriptors, mask),
        )

        for pca_features in (1e-8, 2, lambda u, s, v: s >= 1e-8 * s[0]):
            norm = ml.Normalization.from_dataset(dataset, offset_energy=False, scale_energy=False, pca_features=pca_features)
            assert_equal(norm.features_scale[0].shape, (2, 5))
        dataset_normalized = norm.fw(dataset)
        testing.assert_equal(dataset_normalized.per_point_datasets[0].n_features, 2)
        assert_allclose(dataset_normalized.per_point_datasets[0].features.min(), -1)
        assert_allclose(dataset_normalized.per_point_datasets[0].features.max(), 1)

        dataset_restored = norm.bw(dataset_normalized)
        descriptors_restored = dataset_restored.per_point_datasets[0].features

        assert_allclose(descriptors_restored, descriptors)
