import unittest
from Geometry import Coordinates
from math import pi


class TestCoordinates(unittest.TestCase):
    def setUp(self):
        self.p0 = Coordinates(0, 0)
        self.p1 = Coordinates(1, 1)
        self.p2 = Coordinates(3, 4)

    def test__init__(self):
        self.assertEqual(Coordinates(0, 0), self.p0)
        with self.assertRaises(ValueError):
            Coordinates("a", 5)

    def test__str__(self):
        self.assertEqual(str(self.p1), "(1; 1)")

    def test__eq__(self):
        with self.assertRaises(AttributeError):
            x = self.p1 == (1, 1)
        self.assertEqual(self.p1, Coordinates(1, 1))
        self.assertNotEqual(self.p1, self.p2)

    def test__add__(self):
        self.assertEqual(self.p1 + self.p0, self.p1)
        self.assertEqual(self.p1 + self.p2, Coordinates(4, 5))

    def test__neg__(self):
        self.assertEqual(-self.p1, Coordinates(-1, -1))

    def test__sub__(self):
        self.assertEqual(self.p1 - self.p2, Coordinates(-2, -3))

    def test_dist_to(self):
        self.assertEqual(self.p2.dist_to(self.p0), 5)

    def test_in_ball(self):
        self.assertTrue(self.p1.in_ball(2, self.p0))
        self.assertFalse(self.p1.in_ball(0.5, self.p0))

    def test_get_alpha(self):
        self.assertEqual(Coordinates(1, 0).get_alpha(), 0)
        self.assertEqual(Coordinates(0, 1).get_alpha(), pi/2)
        self.assertEqual(self.p1.get_alpha(), pi/4)
        with self.assertRaises(ValueError):
            self.p0.get_alpha()

    def test_move(self):
        self.assertAlmostEqual(self.p0.move(Coordinates(2, 2), 2**.5).x, self.p1.x, places=8)
        self.assertAlmostEqual(self.p0.move(Coordinates(2, 2), 2**.5).y, self.p1.y, places=8)

    def test_tuple(self):
        self.assertEqual(self.p2.tuple, (3, 4))
        self.p2.tuple = (6, 12)
        self.assertEqual(self.p2.tuple, (6, 12))


if __name__ == "__main__":
    pass