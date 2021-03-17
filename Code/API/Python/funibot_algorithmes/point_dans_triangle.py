from __future__ import annotations

from funibot_api.funibot import Vecteur


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
