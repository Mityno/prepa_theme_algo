import numpy as np 
import matplotlib.pyplot as plt
from util import lire_fichier_coords


def angle(pivot, point) -> float:
    if point == pivot:
        return -1.
    
    x0,y0 = pivot
    x,y = point
    return np.arccos((x-x0)/np.sqrt((x-x0)**2 + (y-y0)**2))

def angle_sort(coords):
    pivot = coords[0]
    coords.sort(key=lambda point: angle(pivot, point))
    return

def right_turn(point1, point2, point3):
    (x1,y1),(x2,y2),(x3,y3) = point1, point2, point3
    cross_prod = (x2-x1)*(y3-y1) - (y2-y1)*(x3-x1) 
    return cross_prod < 0

def graham_scan(coords):
    coords.sort(key=lambda pt : pt[::-1])
    angle_sort(coords)
    hull = coords[:2]
    for i, point in enumerate(coords, start=2):
        if right_turn(hull[-2], hull[-1], point):
            hull.pop()
        hull.append(point)
    return hull



