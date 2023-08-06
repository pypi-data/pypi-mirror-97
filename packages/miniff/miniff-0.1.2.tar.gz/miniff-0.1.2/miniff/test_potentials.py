from . import _util, potentials, kernel

import numpy as np
from numpy import testing
from scipy.sparse import csr_matrix
from numericalunits import angstrom, Ry
import json

from unittest import TestCase


def dummy_potential(r_indptr, r_indices, r_data,
                    cartesian_row, cartesian_col,
                    A, b, cutoff,
                    species_row, species_mask, out):
    for r, (ptr_fr, ptr_to) in enumerate(zip(r_indptr[:-1], r_indptr[1:])):
        if species_row[r] == species_mask[0]:
            for ptr in range(ptr_fr, ptr_to):
                c = r_indices[ptr]
                if species_row[c % len(species_row)] == species_mask[1]:
                    dst = r_data[ptr]
                    if dst < cutoff:
                        out[r] += A * dst ** 2 + b


def dummy_potential_gradient(r_indptr, r_indices, r_data,
                    cartesian_row, cartesian_col,
                    A, b, cutoff,
                    species_row, species_mask, out):
    for r, (ptr_fr, ptr_to) in enumerate(zip(r_indptr[:-1], r_indptr[1:])):
        if species_row[r] == species_mask[0]:
            for ptr in range(ptr_fr, ptr_to):
                c = r_indices[ptr]
                c_ = c % len(cartesian_row)
                if species_row[c_] == species_mask[1]:
                    dst = r_data[ptr]
                    if dst < cutoff:
                        force = 2 * A * dst
                        v = cartesian_row[r] - cartesian_col[c]
                        v /= r_data[ptr]
                        out[r, r] += force * v
                        out[r, c_] -= force * v


def assert_potentials_allclose(a: potentials.LocalPotential, b: potentials.LocalPotential, err_msg="", **kwargs):
    testing.assert_equal(a.__class__, b.__class__, err_msg=err_msg)
    testing.assert_equal(a.coordination_number, b.coordination_number, err_msg=err_msg)
    testing.assert_allclose(a.cutoff, b.cutoff, err_msg=err_msg, **kwargs)
    testing.assert_equal(a.parameters.keys(), b.parameters.keys(), err_msg=err_msg)
    testing.assert_equal(a.tag, b.tag)
    for k in a.parameters:
        testing.assert_allclose(a.parameters[k], b.parameters[k], err_msg=f"{err_msg} key={k}", **kwargs)


class TestMisc(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cartesian_row = np.array([[0., 0., 0.], [.1, .1, .1]])
        cls.cartesian_col = np.array([[.2, .2, .2], [.3, .3, .3]])
        cls.r = csr_matrix([[0, .27 ** .5], [0, 0]])

    def test_calc_sparse_distances(self):
        data = _util.calc_sparse_distances(
            self.r.indptr,
            self.r.indices,
            self.cartesian_row,
            self.cartesian_col,
        )
        testing.assert_allclose(
            data,
            self.r.data,
        )


class PotentialTestMixin:
    @classmethod
    def setUpClass(cls) -> None:
        cls.cartesian_row = np.array([
            [.0, .0, .0],
            [.1, .0, .0],
            [.0, .1, .0]
        ])
        cls.cartesian_col = np.concatenate([
            cls.cartesian_row + [[.2, 0., 0.]],
            cls.cartesian_row + [[0., .2, 0.]],
        ])
        # c
        #
        # c   c
        # | / |
        # r   |   c
        #     |
        # r   r---c   c
        r = np.linalg.norm(cls.cartesian_row[:, np.newaxis] - cls.cartesian_col[np.newaxis, :], axis=-1)
        mask = np.array([
            [0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 1, 0],
        ])
        r[np.logical_not(mask)] = 0
        cls.r = csr_matrix(r)

        cls.override_cutoff_check = False
        cls.is_parallel = True
        cls.setUpClassPotential()

        cls.potential.kernels["kernel_gradient_d"] = potentials.num_grad_potential(
            cls.potential.kernels["kernel"], pre_compute_r_functions=cls.potential.pre_compute_r_functions)
        cls.r_cutoff = cls.r.toarray()
        cls.potential_parameters = cls.potential.parameters.copy()
        if isinstance(cls.potential, potentials.ScaledLocalPotential):
            cls.potential_parameters["epsilon"] = cls.potential.epsilon
            cls.potential_parameters["sigma"] = cls.potential.sigma
            cls.potential.__out_scale__["kernel_gradient_d"] = cls.potential.__out_scale__["kernel_gradient"]
        mask = cls.r_cutoff >= cls.__cutoff__(**cls.potential_parameters)
        if cls.r_cutoff[mask].sum() == 0 and not cls.override_cutoff_check:
            raise RuntimeError("This test cannot check the cutoff because all distances in the test data are less than the cutoff")
        cls.r_cutoff[mask] = 0

        if cls.r_cutoff.max() == 0 and not cls.override_cutoff_check:
            raise RuntimeError("All pairs are cut off: nothing to check")

    @classmethod
    def __cutoff__(cls, **kwargs):
        raise NotImplementedError

    @classmethod
    def setUpClassPotential(cls):
        raise NotImplementedError

    @classmethod
    def __potential_fun__(cls, r, row, col, **kwargs):
        raise NotImplementedError

    @classmethod
    def __potential_grad__(cls, r, row, col, **kwargs):
        raise NotImplementedError

    @classmethod
    def __uvecs__(cls, row, col):
        v = row[:, np.newaxis, :] - col[np.newaxis, :, :]
        v /= np.linalg.norm(v, axis=-1)[..., np.newaxis]
        return v

    def test_val(self, check_nonzero=True):
        val_ref = self.__potential_fun__(self.r_cutoff, self.cartesian_row, self.cartesian_col, **self.potential_parameters)
        if check_nonzero and np.all(val_ref == 0):
            raise ValueError("Potential is misconfigured and produces zero values only")
        testing.assert_allclose(
            self.potential("kernel", self.r, self.cartesian_row, self.cartesian_col),
            val_ref,
        )

        # Buffer test
        out = np.zeros(potentials.shape_for_kernel("kernel", len(self.cartesian_row)), dtype=float)

        self.potential("kernel", self.r, self.cartesian_row, self.cartesian_col, out=out, prefer_parallel=False)
        testing.assert_allclose(out, val_ref)

        out.fill(0)
        self.potential("kernel", self.r, self.cartesian_row, self.cartesian_col, out=out, prefer_parallel=True)
        testing.assert_allclose(out, val_ref)

    def test_grad(self, check_nonzero=True):
        val_ref = self.__potential_grad__(self.r_cutoff, self.cartesian_row, self.cartesian_col, **self.potential_parameters)
        if check_nonzero and np.all(val_ref == 0):
            raise ValueError("Potential gradients are misconfigured and produce zero values only")
        testing.assert_allclose(
            self.potential("kernel_gradient", self.r, self.cartesian_row, self.cartesian_col),
            val_ref,
        )

        # Buffer test
        out = np.zeros(potentials.shape_for_kernel("kernel_gradient", len(self.cartesian_row)), dtype=float)

        self.potential("kernel_gradient", self.r, self.cartesian_row, self.cartesian_col, out=out, prefer_parallel=False)
        testing.assert_allclose(out, val_ref)

        out.fill(0)
        self.potential("kernel_gradient", self.r, self.cartesian_row, self.cartesian_col, out=out, prefer_parallel=True)
        testing.assert_allclose(out, val_ref)

    def test_numgrad(self, atol=1e-10, rtol=1e-3, debug=False):
        test = self.potential("kernel_gradient", self.r, self.cartesian_row, self.cartesian_col)
        ref = self.potential("kernel_gradient_d", self.r, self.cartesian_row, self.cartesian_col, out=np.zeros(
            potentials.shape_for_kernel("kernel_gradient", len(self.cartesian_row)), dtype=float,
        ))
        if debug:
            test_nz = np.nonzero(test)
            ref_nz = np.nonzero(ref)
            print(test_nz, ref_nz)
            print(test[test_nz], ref[ref_nz])
        testing.assert_allclose(test, ref, atol=atol, rtol=rtol)

    def test_kernel_picker(self):
        for kname in "kernel", "kernel_gradient":
            self.assertIsNot(self.potential.kernels[kname], self.potential.kernels.get(f"{kname}_parallel"))
            self.assertIs(
                self.potential.get_kernel_by_name(kname, prefer_parallel=False),
                self.potential.kernels[kname],
            )
            self.assertIs(
                self.potential.get_kernel_by_name(kname, prefer_parallel=True),
                self.potential.kernels[f"{kname}_parallel" if self.is_parallel else kname],
            )


class RefPotentialMixin:
    def _test_ref_numgrad(self, atol=1e-10, rtol=1e-3, debug=False):  # This test is not stable because of units
        self.potential_ref.kernels["kernel_gradient_d"] = potentials.num_grad_potential(self.potential_ref.kernels["kernel"])
        test = self.potential_ref("kernel_gradient", self.r, self.cartesian_row, self.cartesian_col)
        ref = self.potential_ref("kernel_gradient_d", self.r, self.cartesian_row, self.cartesian_col, out=np.zeros(
            potentials.shape_for_kernel("kernel_gradient", len(self.cartesian_row)), dtype=float,
        ))
        if debug:
            test_nz = np.nonzero(test)
            ref_nz = np.nonzero(ref)
            print(test_nz, ref_nz)
            print(test[test_nz], ref[ref_nz])
        testing.assert_allclose(test, ref, atol=atol, rtol=rtol)

    def test_val_ref(self):
        testing.assert_allclose(
            self.potential("kernel", self.r, self.cartesian_row, self.cartesian_col),
            self.potential_ref("kernel", self.r, self.cartesian_row, self.cartesian_col),
        )

    def test_grad_ref(self):
        testing.assert_allclose(
            self.potential("kernel_gradient", self.r, self.cartesian_row, self.cartesian_col),
            self.potential_ref("kernel_gradient", self.r, self.cartesian_row, self.cartesian_col),
        )


class SerializationMixin:
    def test_json_serialization(self):
        data = self.potential.to_json()
        json.dumps(data)  # This is to make sure the return object is JSON-compatible
        restored = potentials.LocalPotentialFamily.instance_from_json(data)
        assert_potentials_allclose(restored, self.potential)


class PairPotentialTestMixin(PotentialTestMixin, RefPotentialMixin):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.potential_ref = potentials.general_pair_potential_family(
            a=cls.__cutoff__(**cls.potential_parameters),
            f=lambda r: cls.__raw_fun__(r, **cls.potential_parameters),
            df_dr=lambda r: cls.__raw_fun_prime__(r, **cls.potential_parameters),
        )

    @classmethod
    def setUpClassPotential(cls):
        raise NotImplementedError

    @classmethod
    def __potential_cutoff__(cls, **kwargs):
        raise NotImplementedError

    @classmethod
    def __raw_fun__(cls, r, **kwargs):
        raise NotImplementedError

    @classmethod
    def __potential_fun__(cls, r, row, col, **kwargs):
        result = cls.__raw_fun__(r, **kwargs)
        result[r == 0] = 0
        return result.sum(axis=1)

    @classmethod
    def __raw_fun_prime__(cls, r, **kwargs):
        raise NotImplementedError

    @classmethod
    def __potential_grad__(cls, r, row, col, **kwargs):
        uvecs = cls.__uvecs__(row, col)
        result = cls.__raw_fun_prime__(r, **kwargs)  # [n_rows, n_columns]
        result[r == 0] = 0
        result = result[..., np.newaxis] * uvecs  # [n_rows, n_columns, 3]
        nr, nc, nd = result.shape
        result = result.reshape(nr, -1, nr, nd).sum(axis=1)  # [n_rows, n_rows, 3]

        result_self = np.zeros_like(result)
        a = np.arange(nr)
        result_self[a, a, :] = result.sum(axis=1)
        return result_self - result


class AnglePotentialTestMixin(PotentialTestMixin, RefPotentialMixin):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.potential_ref = potentials.general_triple_potential_family(
            a=cls.__cutoff__(**cls.potential_parameters),
            f=lambda *args: cls.__raw_fun__(*args, **cls.potential_parameters),
            df_dr1=lambda *args: cls.__raw_fun_prime_r1__(*args, **cls.potential_parameters),
            df_dr2=lambda *args: cls.__raw_fun_prime_r2__(*args, **cls.potential_parameters),
            df_dt=lambda *args: cls.__raw_fun_prime_cos__(*args, **cls.potential_parameters),
        )

    @classmethod
    def setUpClassPotential(cls):
        raise NotImplementedError

    @classmethod
    def __raw_fun__(cls, r1, r2, r12_cos, **kwargs):
        raise NotImplementedError

    @classmethod
    def __inputs__(cls, r, row, col):
        r1 = r[..., np.newaxis]
        r2 = r[:, np.newaxis, :]
        uv = cls.__uvecs__(row, col)
        c = np.einsum("ija,ika->ijk", uv, uv)
        return r1, r2, c

    @classmethod
    def __potential_fun__(cls, r, row, col, **kwargs):
        r1, r2, c = cls.__inputs__(r, row, col)
        result = cls.__raw_fun__(r1, r2, c, **kwargs)
        result[r1 * r2 == 0] = 0
        if not cls.degenerate:
            _i = np.arange(r1.shape[1])
            result[:, _i, _i] = 0
        return result.sum(axis=(1, 2))

    @classmethod
    def __raw_fun_prime_r1__(cls, r1, r2, r12_cos, **kwargs):
        raise NotImplementedError

    @classmethod
    def __raw_fun_prime_r2__(cls, r1, r2, r12_cos, **kwargs):
        raise NotImplementedError

    @classmethod
    def __raw_fun_prime_cos__(cls, r1, r2, r12_cos, **kwargs):
        raise NotImplementedError

    @classmethod
    def __potential_grad__(cls, r, row, col, **kwargs):
        r1, r2, c = cls.__inputs__(r, row, col)
        # r1: [n_rows, n_columns, n_columns]
        # r2: [n_rows, n_columns, n_columns]
        #  c: [n_rows, n_columns, n_columns]
        uvecs = cls.__uvecs__(row, col)  # [n_rows, n_columns, 3]
        dc_dr1 = (uvecs[:, np.newaxis, ...] - uvecs[:, :, np.newaxis, ...] * c[..., np.newaxis]) / r1[..., np.newaxis]  # [n_rows, n_columns, n_columns, 3]
        dc_dr2 = (uvecs[:, :, np.newaxis, ...] - uvecs[:, np.newaxis, ...] * c[..., np.newaxis]) / r2[..., np.newaxis]  # [n_rows, n_columns, n_columns, 3]
        _r1 = cls.__raw_fun_prime_r1__(r1, r2, c, **kwargs)  # [n_rows, n_columns, n_columns]
        _r2 = cls.__raw_fun_prime_r2__(r1, r2, c, **kwargs)  # [n_rows, n_columns, n_columns]
        _cos = cls.__raw_fun_prime_cos__(r1, r2, c, **kwargs)  # [n_rows, n_columns, n_columns]

        r12_filter = r1 * r2 == 0  # [n_rows, n_columns, n_columns]

        _r1[r12_filter] = 0
        _r2[r12_filter] = 0
        _cos[r12_filter] = 0
        dc_dr1[r12_filter, :] = 0
        dc_dr2[r12_filter, :] = 0

        if not cls.degenerate:
            _i = np.arange(r1.shape[1])
            _r1[:, _i, _i] = 0
            _r2[:, _i, _i] = 0
            _cos[:, _i, _i] = 0

        result_1 = _r1[..., np.newaxis] * uvecs[:, :, np.newaxis] + _cos[..., np.newaxis] * dc_dr1  # [n_rows, n_columns, n_columns, 3]
        result_2 = _r2[..., np.newaxis] * uvecs[:, np.newaxis, :] + _cos[..., np.newaxis] * dc_dr2  # [n_rows, n_columns, n_columns, 3]
        nr, nc, nc, nd = result_1.shape
        factor = nc // nr
        result_1 = result_1.reshape(nr, factor, nr, factor, nr, nd).sum(axis=(1, 3))
        result_2 = result_2.reshape(nr, factor, nr, factor, nr, nd).sum(axis=(1, 3))

        result_self = np.zeros((nr, nr, 3), dtype=float)
        a = np.arange(nr)
        result_self[a, a, :] = result_1.sum(axis=(1, 2)) + result_2.sum(axis=(1, 2))
        return result_self - result_1.sum(axis=2) - result_2.sum(axis=1)


class LocalPotentialTest(PairPotentialTestMixin, TestCase):
    @classmethod
    def setUpClassPotential(cls):
        cls.potential = potentials.LocalPotential(2, dict(A=2, b=3, cutoff=.2), .2, dict(kernel=dummy_potential, kernel_gradient=dummy_potential_gradient))
        cls.is_parallel = False

    @classmethod
    def __raw_fun__(cls, r, A, b, cutoff):
        return A * r ** 2 + b

    @classmethod
    def __raw_fun_prime__(cls, r, A, b, cutoff):
        return 2 * A * r

    @classmethod
    def __cutoff__(cls, A, b, cutoff):
        return cutoff


class TestOnSite(PotentialTestMixin, SerializationMixin, TestCase):
    @classmethod
    def setUpClassPotential(cls) -> None:
        cls.potential = potentials.on_site_potential_family(v0=3.14)
        cls.is_parallel = False
        cls.override_cutoff_check = True

    @classmethod
    def __potential_fun__(cls, r, row, col, v0):
        return v0 * np.ones(len(r))

    @classmethod
    def __potential_grad__(cls, r, row, col, v0):
        nr = len(row)
        return np.zeros((nr, nr, 3))

    @classmethod
    def __cutoff__(cls, v0):
        return 0

    def test_grad(self, check_nonzero=False):
        super().test_grad(check_nonzero=check_nonzero)


class TestHarmonic(PairPotentialTestMixin, SerializationMixin, TestCase):
    @classmethod
    def setUpClassPotential(cls):
        cls.potential = potentials.harmonic_repulsion_potential_family(a=.19, epsilon=3.4)

    @classmethod
    def __raw_fun__(cls, r, a, epsilon):
        return epsilon * (r - a) ** 2 / a / a / 2

    @classmethod
    def __raw_fun_prime__(cls, r, a, epsilon):
        return epsilon * (r - a) / a / a

    @classmethod
    def __cutoff__(cls, a, epsilon):
        return a


class TestLJ(PairPotentialTestMixin, SerializationMixin, TestCase):
    @classmethod
    def setUpClassPotential(cls):
        cls.potential = potentials.lj_potential_family(epsilon=2, sigma=.1, a=2.0)

    @classmethod
    def __raw_fun__(cls, r, a, epsilon, sigma):
        return 4 * epsilon * ((sigma / r) ** 12 - (sigma / r) ** 6)

    @classmethod
    def __raw_fun_prime__(cls, r, a, epsilon, sigma):
        return 4 * epsilon * (- 12 * (sigma / r) ** 12 + 6 * (sigma / r) ** 6) / r

    @classmethod
    def __cutoff__(cls, a, epsilon, sigma):
        return a * sigma


class TestSW2(PairPotentialTestMixin, SerializationMixin, TestCase):
    @classmethod
    def setUpClassPotential(cls):
        cls.potential = potentials.sw2_potential_family(p=4, q=0, a=2.0, epsilon=0.01*Ry, sigma=0.1 * angstrom)
        cls.cartesian_row *= angstrom
        cls.cartesian_col *= angstrom
        cls.r *= angstrom

    @classmethod
    def __raw_fun__(cls, r, a, p, q, gauge_a, gauge_b, epsilon, sigma):
        r = r / sigma
        return epsilon * gauge_a * (gauge_b * r ** (-p) - r ** (-q)) * np.exp(1. / (r - a))

    @classmethod
    def __raw_fun_prime__(cls, r, a, p, q, gauge_a, gauge_b, epsilon, sigma):
        function_value = cls.__raw_fun__(r, a, p, q, gauge_a, gauge_b, epsilon, sigma)
        r = r / sigma
        result = epsilon * (- p * gauge_a * gauge_b * r ** (- p - 1) + gauge_a * q * r ** (- q - 1)) * np.exp(1. / (r - a)) - function_value / (r - a) / (r - a)
        return result / sigma

    @classmethod
    def __cutoff__(cls, a, p, q, gauge_a, gauge_b, epsilon, sigma):
        return a * sigma


class TestBehlerSF2(PairPotentialTestMixin, SerializationMixin, TestCase):
    @classmethod
    def setUpClassPotential(cls):
        cls.potential = potentials.behler2_descriptor_family(a=.19, eta=5, r_sphere=.1)

    @classmethod
    def __raw_fun__(cls, r, a, eta, r_sphere):
        return np.exp(- eta * (r - r_sphere) * (r - r_sphere)) * (.5 + np.cos(np.pi * r / a) / 2)

    @classmethod
    def __raw_fun_prime__(cls, r, a, eta, r_sphere):
        function_value = cls.__raw_fun__(r, a, eta, r_sphere)
        return - 2 * eta * (r - r_sphere) * function_value - np.exp(- eta * (r - r_sphere) * (r - r_sphere)) * .5 * np.sin(np.pi * r / a) * np.pi / a

    @classmethod
    def __cutoff__(cls, a, eta, r_sphere):
        return a


class TestSigmoid(PairPotentialTestMixin, SerializationMixin, TestCase):
    @classmethod
    def setUpClassPotential(cls):
        cls.potential = potentials.sigmoid_descriptor_family(a=.19, dr=.05, r0=.1)

    @classmethod
    def __raw_fun__(cls, r, a, dr, r0):
        return 1. / (1 + np.exp((r - r0) / dr)) * (.5 + np.cos(np.pi * r / a) / 2)

    @classmethod
    def __raw_fun_prime__(cls, r, a, dr, r0):
        function_value = cls.__raw_fun__(r, a, dr, r0)
        return - 1. / (1 + np.exp((r - r0) / dr)) * np.exp((r - r0) / dr) / dr * function_value - 1. / (1 + np.exp((r - r0) / dr)) * .5 * np.sin(np.pi * r / a) * np.pi / a

    @classmethod
    def __cutoff__(cls, a, dr, r0):
        return a


class TestSW3(AnglePotentialTestMixin, SerializationMixin, TestCase):
    @classmethod
    def setUpClassPotential(cls):
        cls.potential = potentials.sw3_potential_family(l=1, gamma=1, cos_theta0=.5, a=2.0, epsilon=0.01 * Ry, sigma=0.1 * angstrom)
        cls.cartesian_row *= angstrom
        cls.cartesian_col *= angstrom
        cls.r *= angstrom
        cls.degenerate = False

    @classmethod
    def __raw_fun__(cls, r1, r2, r12_cos, l, gamma, cos_theta0, a, epsilon, sigma):
        r1 = r1 / sigma
        r2 = r2 / sigma
        return epsilon * l * (r12_cos - cos_theta0) * (r12_cos - cos_theta0) * np.exp(gamma * (1. / (r1 - a) + 1. / (r2 - a)))

    @classmethod
    def __raw_fun_prime_r1__(cls, r1, r2, r12_cos, l, gamma, cos_theta0, a, epsilon, sigma):
        function_value = cls.__raw_fun__(r1, r2, r12_cos, l, gamma, cos_theta0, a, epsilon, sigma)
        r1 = r1 / sigma
        return - function_value * gamma / (r1 - a) / (r1 - a) / sigma

    @classmethod
    def __raw_fun_prime_r2__(cls, r1, r2, r12_cos, l, gamma, cos_theta0, a, epsilon, sigma):
        function_value = cls.__raw_fun__(r1, r2, r12_cos, l, gamma, cos_theta0, a, epsilon, sigma)
        r2 = r2 / sigma
        return - function_value * gamma / (r2 - a) / (r2 - a) / sigma

    @classmethod
    def __raw_fun_prime_cos__(cls, r1, r2, r12_cos, l, gamma, cos_theta0, a, epsilon, sigma):
        r1 = r1 / sigma
        r2 = r2 / sigma
        # No sigma here because cos is dimension-less
        return 2 * epsilon * l * (r12_cos - cos_theta0) * np.exp(gamma * (1 / (r1 - a) + 1 / (r2 - a)))

    @classmethod
    def __cutoff__(cls, l, gamma, cos_theta0, a, epsilon, sigma):
        return a * sigma


class TestBehlerSF5(AnglePotentialTestMixin, SerializationMixin, TestCase):
    @classmethod
    def setUpClassPotential(cls):
        cls.potential = potentials.behler5_descriptor_family(a=.19, eta=5, l=0.1, zeta=4)
        cls.degenerate = False

    @classmethod
    def __raw_fun__(cls, r1, r2, r12_cos, a, eta, l, zeta, epsilon):
        return epsilon * 2 ** (1 - zeta) * (1 + l * r12_cos) ** zeta * np.exp(- eta * (r1 ** 2 + r2 ** 2)) * (.5 + np.cos(np.pi * r1 / a) / 2) * (.5 + np.cos(np.pi * r2 / a) / 2)

    @classmethod
    def __raw_fun_prime_r1__(cls, r1, r2, r12_cos, a, eta, l, zeta, epsilon):
        function_value = cls.__raw_fun__(r1, r2, r12_cos, a, eta, l, zeta, epsilon)
        return - function_value * eta * 2 * r1 - epsilon * 2 ** (1 - zeta) * (1 + l * r12_cos) ** zeta * np.exp(- eta * (r1 ** 2 + r2 ** 2)) * np.sin(np.pi * r1 / a) / 2 * (.5 + np.cos(np.pi * r2 / a) / 2) * np.pi / a

    @classmethod
    def __raw_fun_prime_r2__(cls, r1, r2, r12_cos, a, eta, l, zeta, epsilon):
        function_value = cls.__raw_fun__(r1, r2, r12_cos, a, eta, l, zeta, epsilon)
        return - function_value * eta * 2 * r2 - epsilon * 2 ** (1 - zeta) * (1 + l * r12_cos) ** zeta * np.exp(- eta * (r1 ** 2 + r2 ** 2)) * np.sin(np.pi * r2 / a) / 2 * (.5 + np.cos(np.pi * r1 / a) / 2) * np.pi / a

    @classmethod
    def __raw_fun_prime_cos__(cls, r1, r2, r12_cos, a, eta, l, zeta, epsilon):
        return epsilon * l * zeta * 2 ** (1 - zeta) * (1 + l * r12_cos) ** (zeta - 1) * np.exp(- eta * (r1 ** 2 + r2 ** 2)) * (.5 + np.cos(np.pi * r1 / a) / 2) * (.5 + np.cos(np.pi * r2 / a) / 2)

    @classmethod
    def __cutoff__(cls, a, eta, l, zeta, epsilon):
        return a


class TestBehlerSF4(AnglePotentialTestMixin, SerializationMixin, TestCase):
    @classmethod
    def setUpClassPotential(cls):
        cls.potential = potentials.behler4_descriptor_family(a=.19, eta=5, l=0.1, zeta=4)
        cls.degenerate = False

    @classmethod
    def __r3__(cls, r1, r2, r12_cos):
        return (r1 ** 2 + r2 ** 2 - 2 * r1 * r2 * r12_cos) ** .5

    @classmethod
    def __r3_factor__(cls, r1, r2, r12_cos, a, eta):
        r3 = cls.__r3__(r1, r2, r12_cos)
        return np.exp(- eta * r3 ** 2) * (.5 + np.cos(np.pi * r3 / a) / 2) * (r3 < a)

    @classmethod
    def __r3_factor_prime__(cls, r1, r2, r12_cos, a, eta):
        r3 = cls.__r3__(r1, r2, r12_cos)
        return - np.exp(- eta * r3 ** 2) * (2 * eta * r3 * (.5 + np.cos(np.pi * r3 / a) / 2) + np.pi / a * np.sin(np.pi * r3 / a) / 2) * (r3 < a)

    @classmethod
    def __raw_fun__(cls, r1, r2, r12_cos, a, eta, l, zeta, epsilon):
        return TestBehlerSF5.__raw_fun__(r1, r2, r12_cos, a, eta, l, zeta, epsilon) * cls.__r3_factor__(r1, r2, r12_cos, a, eta)

    @classmethod
    def __raw_fun_prime_r1__(cls, r1, r2, r12_cos, a, eta, l, zeta, epsilon):
        r3 = cls.__r3__(r1, r2, r12_cos)
        dr3_dr1 = (r1 - r2 * r12_cos) / r3
        return TestBehlerSF5.__raw_fun_prime_r1__(r1, r2, r12_cos, a, eta, l, zeta, epsilon) * cls.__r3_factor__(r1, r2, r12_cos, a, eta) + \
               TestBehlerSF5.__raw_fun__(r1, r2, r12_cos, a, eta, l, zeta, epsilon) * cls.__r3_factor_prime__(r1, r2, r12_cos, a, eta) * dr3_dr1

    @classmethod
    def __raw_fun_prime_r2__(cls, r1, r2, r12_cos, a, eta, l, zeta, epsilon):
        r3 = cls.__r3__(r1, r2, r12_cos)
        dr3_dr2 = (r2 - r1 * r12_cos) / r3
        return TestBehlerSF5.__raw_fun_prime_r2__(r1, r2, r12_cos, a, eta, l, zeta, epsilon) * cls.__r3_factor__(r1, r2, r12_cos, a, eta) + \
               TestBehlerSF5.__raw_fun__(r1, r2, r12_cos, a, eta, l, zeta, epsilon) * cls.__r3_factor_prime__(r1, r2, r12_cos, a, eta) * dr3_dr2

    @classmethod
    def __raw_fun_prime_cos__(cls, r1, r2, r12_cos, a, eta, l, zeta, epsilon):
        r3 = cls.__r3__(r1, r2, r12_cos)
        dr3_dcos = -r1 * r2 / r3
        return TestBehlerSF5.__raw_fun_prime_cos__(r1, r2, r12_cos, a, eta, l, zeta, epsilon) * cls.__r3_factor__(r1, r2, r12_cos, a, eta) + \
               TestBehlerSF5.__raw_fun__(r1, r2, r12_cos, a, eta, l, zeta, epsilon) * cls.__r3_factor_prime__(r1, r2, r12_cos, a, eta) * dr3_dcos

    @classmethod
    def __cutoff__(cls, a, eta, l, zeta, epsilon):
        return a


# TODO: add gradients here

class NWPotentialTestMixin:
    @classmethod
    def setUpClass(cls) -> None:
        a = 3
        cls.bond_length = 1. / 3. ** .5 * a
        cutoff = cls.bond_length * 1.1
        cell = kernel.Cell(np.array([
            (3. ** .5 / 2, .5, 0),
            (3. ** .5 / 2, -.5, 0),
            (0, 0, 1. / 3. ** .5),
        ]) * a, [(1. / 3, 1. / 3, .5), (2. / 3, 2. / 3, .5)], ("a", "b"))
        cls.nw = kernel.NeighborWrapper(cell, x=(2, 2, 2), cutoff=cutoff)

        cls.setUpClassPotential()

    def test_val(self):
        for k, v in sorted(self.reference.items()):
            testing.assert_allclose(self.nw.eval(self.potential.copy(tag=k), "kernel"), v, err_msg=k)


class PairNWPotentialTestMixin(NWPotentialTestMixin):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.reference = {
            "a-b": [3 * cls.bond_strength, 0],  # three b's per a
            "b-a": [0, 3 * cls.bond_strength],  # three a's per b
            "a-a": [2 * cls.bond_strength, 0],  # two neighbors in vertical direction
            "b-b": [0, 2 * cls.bond_strength],  # two neighbors in vertical direction
        }


class TriNWPotentialTestMixin(NWPotentialTestMixin):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        aaa = 2 * cls.tri_strength_pi  # vertical chain of bonds
        aab = 6 * cls.tri_strength_pi2  # 90-degree triples
        abb = 6 * cls.tri_strength_2pi3   # 120-degree triples in plane
        if cls.degenerate:
            aaa += 2 * cls.tri_strength_0
            abb += 3 * cls.tri_strength_0
        cls.reference = {
            "a-a-a": [aaa, 0],
            "a-a-b": [aab, 0],
            "a-b-a": [aab, 0],
            "a-b-b": [abb, 0],
            "b-a-a": [0, abb],
            "b-a-b": [0, aab],
            "b-b-a": [0, aab],
            "b-b-b": [0, aaa],
        }


class TestNWOnSite(NWPotentialTestMixin, SerializationMixin, TestCase):
    @classmethod
    def setUpClassPotential(cls):
        cls.potential = potentials.on_site_potential_family(v0=3.14)
        cls.reference = {
            "a": [3.14, 0], "b": [0, 3.14],
        }


class TestNWHarmonic(PairNWPotentialTestMixin, SerializationMixin, TestCase):
    @classmethod
    def setUpClassPotential(cls):
        cls.potential = potentials.harmonic_repulsion_potential_family(a=cls.nw.cutoff, epsilon=3.4)
        cls.bond_strength = TestHarmonic.__raw_fun__(cls.bond_length, **cls.potential.parameters)


class TestNWLJ(PairNWPotentialTestMixin, SerializationMixin, TestCase):
    @classmethod
    def setUpClassPotential(cls):
        cls.potential = potentials.lj_potential_family(epsilon=2, sigma=1, a=cls.nw.cutoff)
        cls.bond_strength = TestLJ.__raw_fun__(cls.bond_length, **cls.potential.parameters,
                                               epsilon=cls.potential.epsilon,
                                               sigma=cls.potential.sigma)


class TestNWSF2(PairNWPotentialTestMixin, SerializationMixin, TestCase):
    @classmethod
    def setUpClassPotential(cls):
        cls.potential = potentials.sw2_potential_family(p=4, q=0, a=1.8, epsilon=0.01*Ry, sigma=cls.nw.cutoff / 1.8)
        cls.bond_strength = TestSW2.__raw_fun__(cls.bond_length, **cls.potential.parameters,
                                                epsilon=cls.potential.epsilon,
                                                sigma=cls.potential.sigma)


class TestNWBehlerSF2(PairNWPotentialTestMixin, SerializationMixin, TestCase):
    @classmethod
    def setUpClassPotential(cls):
        cls.potential = potentials.behler2_descriptor_family(a=cls.nw.cutoff, eta=.3, r_sphere=.26)
        cls.bond_strength = TestBehlerSF2.__raw_fun__(cls.bond_length, **cls.potential.parameters)


class TestNWSigmoid(PairNWPotentialTestMixin, SerializationMixin, TestCase):
    @classmethod
    def setUpClassPotential(cls):
        cls.potential = potentials.sigmoid_descriptor_family(a=cls.nw.cutoff, dr=1, r0=.26)
        cls.bond_strength = TestSigmoid.__raw_fun__(cls.bond_length, **cls.potential.parameters)


class TestNWSW3(TriNWPotentialTestMixin, SerializationMixin, TestCase):
    @classmethod
    def setUpClassPotential(cls):
        cls.potential = potentials.sw3_potential_family(l=1, gamma=.1, cos_theta0=.5, a=1.8, epsilon=0.01 * Ry,
                                                        sigma=cls.nw.cutoff / 1.8)
        cls.tri_strength_pi = TestSW3.__raw_fun__(cls.bond_length, cls.bond_length, -1, **cls.potential.parameters,
                                                  epsilon=cls.potential.epsilon, sigma=cls.potential.sigma)
        cls.tri_strength_pi2 = TestSW3.__raw_fun__(cls.bond_length, cls.bond_length, 0, **cls.potential.parameters,
                                                   epsilon=cls.potential.epsilon, sigma=cls.potential.sigma)
        cls.tri_strength_2pi3 = TestSW3.__raw_fun__(cls.bond_length, cls.bond_length, -.5, **cls.potential.parameters,
                                                    epsilon=cls.potential.epsilon, sigma=cls.potential.sigma)
        cls.degenerate = False
        

class MiscTest(TestCase):
    def test_behler_p2(self, n_points=100):
        a = 1
        eta = 2
        r_sphere = .2
        r = np.linspace(0, a, n_points)
        fv = TestBehlerSF2.__raw_fun__(r, a, eta, r_sphere)
        f2 = fv[2:] + fv[:-2] - 2 * fv[1:-1]
        f2 /= (r[1] - r[0]) ** 2
        f2_test = potentials.behler2_p2(r[1:-1], a, eta, r_sphere)
        testing.assert_allclose(f2_test, f2, atol=1e-2)

    def test_behler_turning_point(self):

        def tp_approx(a, eta, r_sphere, n_points=100):
            r = np.linspace(0, a, n_points)
            fv = TestBehlerSF2.__raw_fun__(r, a, eta, r_sphere)
            num_d = fv[2:] + fv[:-2] - 2 * fv[1:-1]
            ix = np.argwhere(num_d[1:] * num_d[:-1] < 0)[0][-1]
            return (r[ix + 1] + r[ix + 2]) / 2

        testing.assert_allclose(potentials.behler_turning_point(1, 0, 0), .5)
        testing.assert_allclose(tp_approx(1, 0, 0), .5)
        testing.assert_allclose(potentials.behler_turning_point(1, 3, 0), tp_approx(1, 3, 0), atol=1e-3)
        testing.assert_allclose(potentials.behler_turning_point(1, 5e5, 0), 1e-3, atol=1e-5)
