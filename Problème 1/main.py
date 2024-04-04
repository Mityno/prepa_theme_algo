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


def calcule_tournee(coords):
    return coords  # A MODIFIER


coords = util.lire_fichier_coords("exemple2.txt")[:11]
# coords = util.lire_fichier_coords("exemple3.txt")
# print(coords)

bef = time.perf_counter()
tournee = bruteforce_backtracking(coords)
aft = time.perf_counter()
print(f'Temps d\'exécution : {aft - bef:.2f}')
print('Distance finale :', util.distance_totale(tournee))
util.affiche_tournee(tournee)

# tournee = calcule_tournee(coords)
# util.affiche_tournee(tournee)

