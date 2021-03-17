from __future__ import annotations
from unittest.case import skip

from funibot_algorithmes.point_dans_forme import point_dans_triangle_plan_XY as point_triangle
from funibot_algorithmes.point_dans_forme import point_dans_polygone_convexe_plan_XY as point_carre
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
            A=self.A,
            B=self.B,
            C=self.C,
            P=Vecteur(4, 0)))

    def test_point_origine(self):
        self.assertTrue(point_triangle(
            A=self.A,
            B=self.B,
            C=self.C,
            P=Vecteur(0, 0)))

    def test_point_externe_haut(self):
        self.assertFalse(point_triangle(
            A=self.A,
            B=self.B,
            C=self.C,
            P=Vecteur(0, 8.1)))

    def test_point_externe_loin(self):
        self.assertFalse(point_triangle(
            A=self.A,
            B=self.B,
            C=self.C,
            P=Vecteur(17, -3)))

    def test_point_externe_limite(self):
        self.assertFalse(point_triangle(
            A=self.A,
            B=self.B,
            C=self.C,
            P=Vecteur(-1.3, -1)))

    def test_point_externe_super_loin(self):
        self.assertFalse(point_triangle(
            A=self.A,
            B=self.B,
            C=self.C,
            P=Vecteur(100000, 100000)))

    def test_point_externe_externe_1(self):
        self.assertFalse(point_triangle(
            A=self.A,
            B=self.B,
            C=self.C,
            P=Vecteur(3, 6)))

    def test_point_externe_interne_1(self):
        self.assertTrue(point_triangle(
            A=self.A,
            B=self.B,
            C=self.C,
            P=Vecteur(1, 4)))

    def test_point_externe_interne_2(self):
        self.assertTrue(point_triangle(
            A=self.A,
            B=self.B,
            C=self.C,
            P=Vecteur(1.8, 1.8)))

    def test_point_externe_interne_3(self):
        self.assertTrue(point_triangle(
            A=self.A,
            B=self.B,
            C=self.C,
            P=Vecteur(-0.8, 1.8)))

    def test_triangle_origine(self):
        self.assertTrue(point_triangle(
            A=Vecteur(),
            B=self.B,
            C=self.C,
            P=Vecteur(1, 1)))

    def test_triangle_origine_shift(self):
        self.assertTrue(point_triangle(
            A=self.B,
            B=self.C,
            C=Vecteur(),
            P=Vecteur(1, 1)))

    def test_triangle_origine_symetrie(self):
        self.assertTrue(point_triangle(
            A=Vecteur(),
            B=self.C,
            C=self.B,
            P=Vecteur(1, 1)))


class TestPointDansCarre(unittest.TestCase):

    def setUp(self) -> None:
        self.A = Vecteur(0, 0)
        self.B = Vecteur(0, 1000)
        self.C = Vecteur(1000, 0)
        self.D = Vecteur(1000, 1000)
        return super().setUp()

    def test_carre_dans(self):
        self.assertTrue(point_carre(
            [
                self.A,
                self.B,
                self.C,
                self.D
            ],
            P = Vecteur(1, 1)))

    def test_carre_dans_centre(self):
        self.assertTrue(point_carre(
            [
                self.A,
                self.B,
                self.C,
                self.D
            ],
            P = Vecteur(500, 500)))

    def test_carre_hors(self):
        self.assertFalse(point_carre(
            [
                self.A,
                self.B,
                self.C,
                self.D
            ],
            P = Vecteur(1001, 1001)))


class TestPointDansTriangleDemies(unittest.TestCase):

    def setUp(self) -> None:
        self.A = Vecteur(0, 0)
        self.B1 = Vecteur(1000, 0)
        self.B2 = Vecteur(0, 1000)
        self.C = Vecteur(1000, 1000)

        self.point_in_1 = Vecteur(700, 200)
        self.point_in_2 = Vecteur(200, 700)

        return super().setUp()

    def test_demi_triangle_1_dans(self):
        self.assertTrue(point_triangle(
            self.A,
            self.B1,
            self.C, 
            P = self.point_in_1))

    def test_demi_triangle_2_dans(self):
        self.assertTrue(point_triangle(
            self.A,
            self.B2, 
            self.C,
            P = self.point_in_2))

    def test_demi_triangle_1_hors(self):
        self.assertFalse(point_triangle(
            self.A,
            self.B1,
            self.C, 
            P = self.point_in_2))

    def test_demi_triangle_2_hors(self):
        self.assertFalse(point_triangle(
            self.A,
            self.B2, 
            self.C,
            P = self.point_in_1))