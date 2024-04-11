import numpy as np
import matplotlib.pyplot as plt
from util import lire_fichier_coords


def angle(pivot: tuple[float], point: tuple[float]) -> float:
    """Renvoie l'angle formé entre l'horizontale et le segment [pivot, point], compté en sens trigonométrique, en le supposant compris entre 0 et pi."""

    # Si le point est le pivot, renvoie -1. pour qu'il soit compté comme ayant l'angle minimal
    if point == pivot:
        return -1.0

    x0, y0 = pivot
    x, y = point
    return np.arccos((x - x0) / np.sqrt((x - x0) ** 2 + (y - y0) ** 2))


def angle_sort(coords):
    pivot = coords[0]
    coords.sort(key=lambda point: angle(pivot, point))
    return


def right_turn(point1, point2, point3) -> bool:
    (x1, y1), (x2, y2), (x3, y3) = point1, point2, point3
    cross_prod = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
    return cross_prod < 0


def graham_scan(coords: list[tuple[float, float]]) -> list[tuple[float, float]]:
    coords = coords.copy()
    coords.sort(key=lambda pt: pt[::-1])
    angle_sort(coords)
    hull = coords[:2]
    for i, point in enumerate(coords, start=2):
        while right_turn(hull[-2], hull[-1], point):
            hull.pop()
        hull.append(point)
    return hull


if __name__ == "__main__":
    coords = lire_fichier_coords(r"Problème 1\exemple_2.txt")
    coords = list(map(tuple, coords))
    hull = graham_scan(coords)
    plt.scatter([x for x, y in coords], [y for x, y in coords])
    plt.plot([x for x, y in hull], [y for x, y in hull])
    plt.show()
