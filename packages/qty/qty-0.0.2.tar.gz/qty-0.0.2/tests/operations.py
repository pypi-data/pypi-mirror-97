#!/usr/bin/env python3

import math
import unittest

import numpy as np
from qty import Energy


a = Energy()
b = Energy()

a.nm = 800.
b.nm = 400.


class TestOperations(unittest.TestCase):

    def test_add(self):
        c = a + b
        self.assertIsInstance(c, a.__class__)
        self.assertIsInstance(c, b.__class__)
        self.assertRaises(Exception, lambda: a + 2)

    def test_eq(self):
        self.assertEqual(a, a)
        self.assertNotEqual(a, b)
        self.assertRaises(Exception, lambda: a == 2)

    def test_le(self):
        self.assertLessEqual(a, a)
        self.assertLessEqual(a, b)
        self.assertRaises(Exception, lambda: a <= 2)

    def test_lt(self):
        self.assertLess(a, b)
        self.assertRaises(Exception, lambda: a <= 2)

    def test_mul(self):
        c = a * 2
        self.assertIsInstance(c, a.__class__)
        self.assertTrue(c.nm == a.nm / 2)
        c = a * np.array([1, 2, 3])
        d = a.nm / np.array([1, 2, 3])
        self.assertTrue(c.nm.all() == d.all())

    def test_neg(self):
        c = -a
        self.assertTrue(c.nm == -a.nm)

    def test_pos(self):
        c = +a
        self.assertTrue(c.nm == +a.nm)

    def test_radd(self):
        c = a + b
        self.assertIsInstance(c, a.__class__)
        self.assertIsInstance(c, b.__class__)
        self.assertRaises(Exception, lambda: 2 + a)

    def test_rmul(self):
        c = 2 * a
        self.assertIsInstance(c, a.__class__)
        self.assertTrue(c.nm == a.nm / 2)
        c = np.array([1, 2, 3]) * a
        d = a.nm / np.array([1, 2, 3])
        self.assertTrue(c.nm.all() == d.all())

    def test_truediv(self):
        c = a / 2
        self.assertIsInstance(c, a.__class__)
        self.assertTrue(c.nm == 2 * a.nm)

if __name__ == '__main__':
    unittest.main()

