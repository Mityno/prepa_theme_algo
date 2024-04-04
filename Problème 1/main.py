# Code de base pour le problème `Tournée du jardinier`

import util
import time
from matplotlib import pyplot as plt


def bruteforce(coords):
    solution = None
    sol_distance = float('inf')

    def inner(coords, curr):
        nonlocal solution, sol_distance

        if not coords:
            curr_distance = util.distance_totale(curr)
            if curr_distance < sol_distance:
                solution = curr[:]
                sol_distance = curr_distance
            return

        for coord in frozenset(coords):
            coords.discard(coord)
            curr.append(coord)
            inner(coords, curr)
            curr.pop()
            coords.add(coord)

    coords = list(map(tuple, coords))
    inner(set(coords), [])
    return solution


def bruteforce_backtracking(coords):
    solution = None
    sol_distance = float('inf')

    def inner(coords, curr):
        nonlocal solution, sol_distance

        if util.distance_totale(curr) > sol_distance:
            return

        if not coords:
            curr_distance = util.distance_totale(curr)
            if curr_distance < sol_distance:
                solution = curr[:]
                sol_distance = curr_distance
            return

        for coord in frozenset(coords):
            coords.discard(coord)
            curr.append(coord)
            inner(coords, curr)
            curr.pop()
            coords.add(coord)

    coords = list(map(tuple, coords))
    inner(set(coords), [])
    return solution


def reduction_polygone_couvrant(coords, polygon_summits):
    # on enlève les coordonnées des sommets déjà atteints
    coords = [coord for coord in coords if coord not in polygon_summits]

    while coords:
        min_coord = None
        min_updated_distance = float('inf')
        min_coord_pos = None

        # trouver le point pour lequel casser un segment
        for coord in coords:
            for i in range(1, len(polygon_summits)):
                polygon_summits.insert(i, coord)
                curr_distance = util.distance_totale(polygon_summits)
                polygon_summits.pop(i)

                if curr_distance < min_updated_distance:
                    min_coord = coord
                    min_updated_distance = curr_distance
                    min_coord_pos = i

        # ajouter le point au bon endroit du polygone
        polygon_summits.insert(min_coord_pos, min_coord)
        coords.remove(min_coord)

    return polygon_summits


def calcule_tournee(coords):
    return coords  # A MODIFIER


coords = util.lire_fichier_coords('exemple_losange_dense.txt')
coords = list(map(tuple, coords))
# plt.scatter(*zip(*coords), s=10)

# print(coords)
# util.affiche_tournee(coords)
polygon_summits = [(0, 0), (-4, 3), (0, 6), (4, 2)]

polygon_couvrant = reduction_polygone_couvrant(coords, polygon_summits)
polygon_couvrant.remove((0, 0))
print(len(polygon_couvrant))
util.affiche_tournee(polygon_couvrant)

polygon_couvrant_2 = [(0, 2), (-1, 2), (-1, 3), (-4, 3), (0, 6), (0, 4), (1, 4), (1, 3), (0, 3), (1, 2), (4, 2)]
print(len(polygon_couvrant_2))
util.affiche_tournee(polygon_couvrant_2)

result_backtracking = bruteforce_backtracking(coords)
util.affiche_tournee(result_backtracking)

plt.show()
# coords = util.lire_fichier_coords("exemple_2.txt")[20:29]
# coords = util.lire_fichier_coords("exemple_1.txt")
# print(coords)

# bef = time.perf_counter()
# result_bruteforce = bruteforce(coords)
# aft = time.perf_counter()
# result_backtracking = bruteforce_backtracking(coords)

# assert util.distance_totale(result_bruteforce) == util.distance_totale(result_backtracking)

# print(f'Temps d\'exécution : {aft - bef:.2e}')
# print('Distance finale :', util.distance_totale(result_bruteforce))
# print(flush=True)

# util.affiche_tournee(result_bruteforce)

# tournee = calcule_tournee(coords)
# util.affiche_tournee(tournee)

