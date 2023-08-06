from . import util

import numpy as np
from numpy import testing
from numericalunits import angstrom, Ry

from unittest import TestCase


class TestUtil(TestCase):
    def test_num_grad(self):
        def f(_x, _a):
            return (_x ** 2).sum() * _a

        x = np.array([[1, 2, 3], [4, 5, 6]])
        testing.assert_allclose(util.num_grad(f, x, 2), 4 * x)

    def test_masked_unique(self):
        test_masked = [
            np.ma.masked_array(data=[4, 5, 2, 1], mask=[0, 0, 1, 0], fill_value=1),
            np.ma.masked_array(data=[4, 5, 1, 1], mask=[0, 0, 1, 0], fill_value=1),  # make an intentional collision
        ]

        for a in test_masked:
            key, inverse = util.masked_unique(a, return_inverse=True)
            testing.assert_equal(key, [1, 4, 5], err_msg=repr(a))
            testing.assert_equal(inverse.mask, a.mask, err_msg=repr(a))
            testing.assert_equal(inverse.data, [1, 2, 3, 0], err_msg=repr(a))
            testing.assert_equal(inverse.mask, [0, 0, 1, 0], err_msg=repr(a))

    def test_masked_unique_char(self):
        test_masked = [
            np.ma.masked_array(data=['d', 'e', 'b', ''], mask=[0, 0, 1, 0]),
            np.ma.masked_array(data=['d', 'e', '', ''], mask=[0, 0, 1, 0]),  # make an intentional collision
        ]

        for a in test_masked:
            key, inverse = util.masked_unique(a, return_inverse=True)
            testing.assert_equal(key, ['', 'd', 'e'], err_msg=repr(a))
            testing.assert_equal(inverse.mask, a.mask, err_msg=repr(a))
            testing.assert_equal(inverse.data, [1, 2, 3, 0], err_msg=repr(a))
            testing.assert_equal(inverse.mask, [0, 0, 1, 0], err_msg=repr(a))


class TestUnits(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.units = util.ParameterUnits({"a": "angstrom", "r": "Ry", "something": "1/angstrom**2"})

    def test_apply(self):
        self.assertEqual(self.units.apply({"a": 2 * angstrom, "r": (2 * Ry, 3 * Ry), "x": 2}),
                         {"a": 2 * angstrom / angstrom, "r": (2 * Ry / Ry, 3 * Ry / Ry), "x": 2})
        self.assertEqual(self.units.apply({"a": (1 * angstrom, 3 * angstrom), "r": None}),
                         {"a": (1, 3 * angstrom / angstrom), "r": None})

    def test_lift(self):
        self.assertEqual(self.units.lift({"a": 2, "r": 3, "x": 2}), {"a": 2 * angstrom, "r": 3 * Ry, "x": 2})
        self.assertEqual(self.units.lift({"a": (1, 3), "r": None}), {"a": (1 * angstrom, 3 * angstrom), "r": None})

    def test_eval(self):
        self.assertEqual(self.units.get_uv("a"), angstrom)
        self.assertEqual(self.units.get_uv("something"), 1 / angstrom ** 2)
