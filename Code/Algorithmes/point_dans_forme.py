from __future__ import annotations

from typing import List
from funibot_api.funilib import Vecteur


def point_dans_triangle_plan_XY(A: Vecteur, B: Vecteur, C: Vecteur, P: Vecteur):
    if (A.x - B.x) == 0:
        try:
            k = (B.x - A.x) / (B.y - A.y)
            a = (P.x - A.x - k * (P.y - A.y)) / (C.x - A.x - k * (C.y - A.y))
            b = (P.y - A.y) / (B.y - A.y) - a * (C.y - A.y) / (B.y - A.y)
        except ZeroDivisionError:
            return False
    else:
        try:
            k = (B.y - A.y) / (B.x - A.x)
            a = (P.y - A.y - k * (P.x - A.x)) / (C.y - A.y - k * (C.x - A.x))
            b = (P.x - A.x) / (B.x - A.x) - a * (C.x - A.x) / (B.x - A.x)
        except ZeroDivisionError:
            return False

    c = 1 - a - b
    return (a >= 0 and b >= 0 and c >= 0)


def point_dans_polygone_convexe_plan_XY(cotes: List[Vecteur], P: Vecteur):

    if len(cotes) < 3:
        return False
    for index in range(2, len(cotes)):
        if (point_dans_triangle_plan_XY(cotes[0], cotes[index-1], cotes[index], P)):
            return True  # dans au moins 1 triangle

    return False  # dans aucun triangle
