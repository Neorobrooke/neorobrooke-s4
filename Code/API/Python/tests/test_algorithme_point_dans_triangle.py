from __future__ import annotations
from unittest.case import skip

from funibot_algorithmes.point_dans_triangle import point_dans_triangle_plan_XY as point_triangle
import unittest

from funibot_api.funibot import Vecteur

# Voir les cas de tests dans le fichier GeoGebra annexe

class TestPointDansTriangle(unittest.TestCase):

    def setUp(self) -> None:
        self.A = Vecteur(-2, -1)
        self.B = Vecteur(0, 8)
        self.C = Vecteur(4, 0)
        return super().setUp()

    def test_point_sommet(self):
        self.assertTrue(point_triangle(
            A = self.A,
            B = self.B,
            C = self.C,
            P = Vecteur(4, 0)))

    def test_point_origine(self):
        self.assertTrue(point_triangle(
            A = self.A,
            B = self.B,
            C = self.C,
            P = Vecteur(0, 0)))

    def test_point_externe_haut(self):
        self.assertFalse(point_triangle(
            A = self.A,
            B = self.B,
            C = self.C,
            P = Vecteur(0, 8.1)))

    def test_point_externe_loin(self):
        self.assertFalse(point_triangle(
            A = self.A,
            B = self.B,
            C = self.C,
            P = Vecteur(17, -3)))

    def test_point_externe_limite(self):
        self.assertFalse(point_triangle(
            A = self.A,
            B = self.B,
            C = self.C,
            P = Vecteur(-1.3, -1)))

    def test_point_externe_super_loin(self):
        self.assertFalse(point_triangle(
            A = self.A,
            B = self.B,
            C = self.C,
            P = Vecteur(100000, 100000)))

    def test_point_externe_externe_1(self):
        self.assertFalse(point_triangle(
            A = self.A,
            B = self.B,
            C = self.C,
            P = Vecteur(3, 6)))

    def test_point_externe_interne_1(self):
        self.assertTrue(point_triangle(
            A = self.A,
            B = self.B,
            C = self.C,
            P = Vecteur(1, 4)))

    def test_point_externe_interne_2(self):
        self.assertTrue(point_triangle(
            A = self.A,
            B = self.B,
            C = self.C,
            P = Vecteur(1.8, 1.8)))

    def test_point_externe_interne_3(self):
        self.assertTrue(point_triangle(
            A = self.A,
            B = self.B,
            C = self.C,
            P = Vecteur(-0.8, 1.8)))

    def test_triangle_origine(self):
        self.assertTrue(point_triangle(
            A = Vecteur(),
            B = self.B,
            C = self.C,
            P = Vecteur(1, 1)))

    def test_triangle_origine_shift(self):
        self.assertTrue(point_triangle(
            A = self.B,
            B = self.C,
            C = Vecteur(),
            P = Vecteur(1, 1)))