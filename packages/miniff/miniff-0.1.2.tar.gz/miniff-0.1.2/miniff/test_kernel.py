from . import kernel, potentials, util

import numpy as np
from numpy import testing
from scipy.integrate import quad

from numericalunits import Ry, angstrom
from unittest import TestCase
from pathlib import Path
from functools import partial
import json


def f_dummy(r, a):
    return a * r ** 2


def g_dummy(r, a):
    return 2 * a * r


class TestNW(TestCase):
    @classmethod
    def setUpClass(cls):
        cell = kernel.Cell([
            (3. ** .5 / 2, .5, 0),
            (3. ** .5 / 2, -.5, 0),
            (0, 0, 5),
        ], [(1. / 3, 1. / 3, .5), (2. / 3, 2. / 3, .5)], ("a", "b"))
        cls.bond_length = a = 1. / 3. ** .5
        cls.nw = kernel.NeighborWrapper(cell, x=(2, 2, 1), cutoff=cls.bond_length * 1.4)

        cls.delta = 1e-1
        cell_distorted = cell.copy()
        cell_distorted.coordinates[0] += [cls.delta, cls.delta, 0]
        cls.nw_distorted = kernel.NeighborWrapper(cell_distorted, x=(2, 2, 1), cutoff=cls.bond_length * 1.5)

        cls.bond_length_small = cls.bond_length - cls.delta * 3. ** .5
        cls.bond_length_large = ((.5 / 3. ** .5 + cls.delta * 3. ** .5) ** 2 + .25) ** .5

        cls.potentials_s = [
            potentials.on_site_potential_family(v0=3.14, tag="a"),
            potentials.on_site_potential_family(v0=1.59, tag="b"),
        ]
        cls.potentials_p = [
            potentials.sw2_potential_family(p=4, q=0, a=1.3, epsilon=3, sigma=a / 2. ** (1. / 6), tag="a-a"),
            potentials.sw2_potential_family(p=4, q=0, a=1.3, epsilon=7, sigma=a / 2. ** (1. / 6), tag="a-b"),
            potentials.sw2_potential_family(p=4, q=0, a=1.3, epsilon=7, sigma=a / 2. ** (1. / 6), tag="b-a"),
            potentials.sw2_potential_family(p=4, q=0, a=1.3, epsilon=11, sigma=a / 2. ** (1. / 6), tag="b-b"),
        ]
        cls.potentials_sp = cls.potentials_s + cls.potentials_p

        cls.potentials_dummy_p = [
            potentials.general_pair_potential_family(a=a * 1.3, f=partial(f_dummy, a=3), df_dr=partial(g_dummy, a=3), tag="a-a"),
            potentials.general_pair_potential_family(a=a * 1.3, f=partial(f_dummy, a=7), df_dr=partial(g_dummy, a=7), tag="a-b"),
            potentials.general_pair_potential_family(a=a * 1.3, f=partial(f_dummy, a=7), df_dr=partial(g_dummy, a=7), tag="b-a"),
            potentials.general_pair_potential_family(a=a * 1.3, f=partial(f_dummy, a=11), df_dr=partial(g_dummy, a=11), tag="b-b"),
        ]
        cls.potentials_dummy_sp = cls.potentials_s + cls.potentials_dummy_p

    def test_nw_fields_simple(self):
        a = self.bond_length
        nw = self.nw

        self.assertIsNotNone(nw.cell)
        testing.assert_equal(self.nw.cutoff, a * 1.4)
        testing.assert_equal(self.nw.species, ["a", "b"])
        testing.assert_equal(self.nw.spec_encoded_row, [0, 1])
        self.assertEqual(self.nw.spec_encoded_row.dtype, np.int32)

    def test_nw_fields_pairs(self):
        a = self.bond_length
        v1, v2, v3 = self.nw.cell.vectors
        p1 = np.array([a, 0., 0.]) + v3 / 2
        p2 = np.array([2 * a, 0., 0.]) + v3 / 2
        pairs_self_ref = np.array([p1, p1, p1, p2, p2, p2])
        pairs_other_ref = np.array([p2 - v1, p2 - v2, p2, p1, p1 + v2, p1 + v1])

        _s, _o = self.nw.sparse_pair_distances.nonzero()
        order = np.lexsort((_o, _s))
        _s = _s[order]
        _o = _o[order]
        pairs_self = self.nw.cartesian_row[_s, :]
        pairs_other = self.nw.cartesian_col[_o, :]

        testing.assert_allclose(pairs_self, pairs_self_ref, atol=1e-12)
        testing.assert_allclose(pairs_other, pairs_other_ref, atol=1e-12)

        values = list(self.nw.sparse_pair_distances[i] for i in zip(_s, _o))
        testing.assert_allclose(values, [a] * 6)

    def test_nw_fields_pairs_distorted(self):
        _s, _o = self.nw_distorted.sparse_pair_distances.nonzero()
        order = np.lexsort((_o, _s))
        _s = _s[order]
        _o = _o[order]

        values = list(self.nw_distorted.sparse_pair_distances[i] for i in zip(_s, _o))
        testing.assert_allclose(values, 2 * [self.bond_length_large] + 2 * [self.bond_length_small] + 2 * [self.bond_length_large])

    def test_eval_s(self):
        out_ref = np.array(((self.potentials_s[0].parameters["v0"], 0), (0, self.potentials_s[1].parameters["v0"])))
        testing.assert_allclose(self.nw.eval(self.potentials_s, "kernel"), out_ref)
        out = np.zeros((2, 2), dtype=float)
        out_ = self.nw.eval(self.potentials_s, "kernel", out=out)
        self.assertIs(out, out_)
        testing.assert_allclose(out, out_ref)

    def test_energy_s(self):
        testing.assert_allclose(self.nw.total(self.potentials_s), self.potentials_s[0].parameters["v0"] + self.potentials_s[1].parameters["v0"])

    def test_energy_sp(self):
        testing.assert_allclose(
            self.nw.total(self.potentials_p), - self.potentials_p[1].epsilon * 6, atol=1e-5)
        testing.assert_allclose(
            self.nw.total(self.potentials_sp),
            - self.potentials_p[1].epsilon * 6 + self.potentials_s[0].parameters["v0"] + self.potentials_s[1].parameters["v0"], atol=1e-5)

    def test_gradient_sp(self):
        testing.assert_allclose(self.nw.grad(self.potentials_sp), 0, atol=1e-10)

    def test_dummy_energy_sp(self):
        a = self.bond_length
        testing.assert_allclose(self.nw.total(self.potentials_dummy_sp),
                                self.potentials_dummy_p[1].parameters["f"].keywords["a"] * 6 * a ** 2 +  # double-counting
                                self.potentials_s[0].parameters["v0"] +
                                self.potentials_s[1].parameters["v0"])

    def test_dummy_gradient_sp(self):
        testing.assert_allclose(self.nw.grad(self.potentials_dummy_sp), 0, atol=1e-12)

    def test_dummy_energy_sp_distorted(self):
        testing.assert_allclose(self.nw_distorted.total(self.potentials_dummy_sp),
                                self.potentials_dummy_p[1].parameters["f"].keywords["a"] * 2 * (self.bond_length_small ** 2 + 2 * self.bond_length_large ** 2) +
                                self.potentials_s[0].parameters["v0"] +
                                self.potentials_s[1].parameters["v0"])

    def test_dummy_gradient_sp_distorted(self):
        def f(coords):
            cell = self.nw_distorted.cell.copy()
            cell.coordinates = cell.transform_from_cartesian(coords)
            nw = kernel.NeighborWrapper(cell)
            nw.shift_vectors = self.nw_distorted.shift_vectors
            nw.compute_distances(self.nw_distorted.cutoff)
            assert nw.sparse_pair_distances.nnz == 6
            return nw.total(self.potentials_dummy_sp)
        testing.assert_allclose(self.nw_distorted.grad(self.potentials_dummy_sp), util.num_grad(f, self.nw_distorted.cell.cartesian()), atol=1e-10)

    def test_relax(self):
        relaxed = self.nw_distorted.relax(self.potentials_p, units=None)
        d = relaxed.distances()
        testing.assert_allclose(d, [[0, self.bond_length], [self.bond_length, 0]])
        testing.assert_allclose(relaxed.meta["forces"], 0, atol=1e-5)
        testing.assert_allclose(relaxed.meta["total-energy"], - self.potentials_p[1].epsilon * 6, atol=1e-5)

    def test_relax_interstitial(self):
        def interstitial(x):
            return (x + 15) ** 2, 2 * (x + 15)
        relaxed = self.nw_distorted.relax(self.potentials_p, units=None, interstitial=interstitial)
        testing.assert_allclose(relaxed.meta["total-energy"], -15, atol=1e-5)

    def test_relax2(self):

        def f(r, dmin, dmax):
            return (dmin - r) ** 2 * (r < dmin) + (dmax - r) ** 2 * (r > dmax)

        def g(r, dmin, dmax):
            return 2 * (r - dmin) * (r < dmin) + 2 * (r - dmax) * (r > dmax)

        box_size = 1.442
        dummy_potential = potentials.general_pair_potential_family(
            a=2 * box_size,
            f=partial(f, dmin=0.8, dmax=1.2),
            df_dr=partial(g, dmin=0.8, dmax=1.2),
        )
        cell = kernel.Cell(np.eye(3) * box_size, np.array([
            [0.55301837, 1.1418651,  0.76279847],
            [0.81926202, 1.33494135, 0.10245172],
            [0.1256622,  0.02915998, 1.20084561]]) / box_size, ("x",) * 3)
        nw = kernel.NeighborWrapper(cell, x=(1, 1, 1), cutoff=2 * box_size)
        relaxed = nw.relax(dummy_potential.copy(tag="x-x"), units=None, rtn_history=True)
        testing.assert_allclose(relaxed[-1].meta["total-energy"], 0)
        testing.assert_equal(np.logical_or(0.8 > relaxed[-1].distances(), 1.2 < relaxed[-1].distances()).sum(), 3)

    def test_rdf(self):
        sigma = 0.1
        nat = quad(lambda x: self.nw.rdf(x, 0.1)["a-b"] * 4 * np.pi * x ** 2, self.bond_length - 3 * sigma, self.bond_length + 3 * sigma)
        testing.assert_allclose(nat[0], 3, atol=1e-2)

    def test_batch_rdf(self):
        r = np.linspace(0, 1)
        rdf = self.nw.rdf(r, 0.1)
        rdfb = kernel.batch_rdf([self.nw], r, 0.1)
        testing.assert_equal(rdf, rdfb)


class IntegrationTests(TestCase):
    """Various weird bugs are collected here."""
    def test_supercell_match(self):
        """
        I figured out that total energy of 2D and 3D supercells do not match
        a multiple of the total energy of a unit cell.
        """
        c1 = kernel.Cell(np.diag([1, 1, 10]), [[.5, .5, .5]], ['x'])
        c2 = c1.repeated(2, 2, 1)
        lj = potentials.lj_potential_family(epsilon=1, sigma=1, a=1.9)

        c1w = kernel.NeighborWrapper(c1, (4, 4, 1), cutoff=lj.cutoff + 0.05)

        c2w = kernel.NeighborWrapper(c2, (3, 3, 1), cutoff=lj.cutoff + 0.05)

        testing.assert_equal(
            len(c1w.sparse_pair_distances.nonzero()[0]) * 4,
            len(c2w.sparse_pair_distances.nonzero()[0])
        )
        testing.assert_allclose(c1w.total(lj.copy(tag="x-x")) * 4, c2w.total(lj.copy(tag="x-x")))

    def test_relax(self):
        """Relaxation is too slow: this test is for profiling and benchmarking the issue."""
        potential_pre = potentials.harmonic_repulsion_potential_family(a=1, epsilon=1)
        potential = potentials.lj_potential_family(epsilon=1, sigma=1, a=20)
        with open(Path(__file__).parent / ".." / "datasets" / "three-point-samples.json", 'r') as f:
            cells = list(kernel.Cell.from_json(i) for i in json.load(f))
        for i_c, c in enumerate(cells):
            nw = kernel.NeighborWrapper(c, x=(1, 1, 1), cutoff=potential.cutoff)
            # Pre-relax with harmonic repulsion
            cell = nw.relax(potential_pre.copy(tag="x-x"), units=None, method="CG")
            nw.set_cell(cell)
            nw.compute_distances(potential.cutoff)
            # Actual relax
            cell_r = nw.relax(potential.copy(tag="x-x"), units=None, method="CG")
            testing.assert_allclose(cell_r.meta["forces"], 0, atol=1e-5, err_msg=f"#{i_c}")

    def test_relax_units(self):
        """A bug with units not processed during relaxation."""
        potential_pre = potentials.harmonic_repulsion_potential_family(a=1 * angstrom, epsilon=1 * Ry)
        potential = potentials.lj_potential_family(epsilon=1 * Ry, sigma=1 * angstrom, a=20)
        cells = []
        with open(Path(__file__).parent / ".." / "datasets" / "three-point-samples.json", 'r') as f:
            for i in json.load(f):
                c = kernel.Cell.from_json(i)
                c.vectors *= angstrom
                cells.append(c)
        for c in cells:
            nw = kernel.NeighborWrapper(c, x=(1, 1, 1), cutoff=potential.cutoff)
            # Pre-relax with harmonic repulsion
            cell = nw.relax(potential_pre.copy(tag="x-x"), method="CG")
            nw.set_cell(cell)
            nw.compute_distances(potential.cutoff)
            # Actual relax
            cell_r = nw.relax(potential.copy(tag="x-x"), units="atomic", method="CG")
            testing.assert_allclose(cell_r.meta["forces"], 0, atol=1e-5 * Ry / angstrom)  # TODO: this occasionally fails with a wild error 2.2e-13 vs 5.4e-19

    def test_relax_lj(self):
        """Unphysical relaxation with LJ potential"""
        potential = potentials.lj_potential_family(epsilon=1, sigma=1, a=2.9)
        c = kernel.Cell(
            np.eye(3),
            [[0.65098689, 0.99427277, 0.22621891], [0.58800034, -0.22191917, 0.5648664], [0.29229667, 1.25826357, 1.42123495]],
            ("x",) * 3,
        )
        nw = kernel.NeighborWrapper(c, (1, 1, 1), normalize=False, cutoff=potential.cutoff)
        relaxed = nw.relax(potential.copy(tag="x-x"), units=None, normalize=False)
        testing.assert_allclose(relaxed.distances()[(0, 1, 2), (1, 2, 0)], 2.**(1./6))

    def test_forces_bise(self):
        """Unphysical interatomic distances after relaxation with HarmonicRepulsion."""
        with open(Path(__file__).parent / ".." / "datasets" / "bise.json", 'r') as f:
            c = kernel.Cell.from_json(json.load(f))
        cutoff = 2 * angstrom
        wrapped = kernel.NeighborWrapper(c, x=(3, 3, 3), cutoff=cutoff)
        p = potentials.harmonic_repulsion_potential_family(a=cutoff, epsilon=Ry)
        pots = [p.copy(tag="bi-bi"), p.copy(tag="se-bi"), p.copy(tag="bi-se"), p.copy(tag="se-se")]

        relaxed = wrapped.relax(pots)
        wrapped_relaxed = kernel.NeighborWrapper(relaxed, x=(3, 3, 3), cutoff=p.cutoff)
        testing.assert_allclose(relaxed.meta["forces"] / (Ry / angstrom), 0, atol=1e-5)
        testing.assert_array_less(1.99, wrapped_relaxed.sparse_pair_distances.data.min() / angstrom)
