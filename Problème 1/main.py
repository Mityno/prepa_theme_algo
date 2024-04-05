# Code de base pour le problème `Tournée du jardinier`

import util
import time
from matplotlib import pyplot as plt


def calcule_tournee(coords):
    return coords  # A MODIFIER


coords = util.lire_fichier_coords("exemple_2.txt")[50:59]
# coords = util.lire_fichier_coords("exemple_1.txt")
# print(coords)

bef = time.perf_counter()
result_bruteforce = bruteforce(coords)
aft = time.perf_counter()
result_backtracking = bruteforce_backtracking(coords)

assert util.distance_totale(result_bruteforce) == util.distance_totale(result_backtracking)

print(f'Temps d\'exécution : {aft - bef:.2e}')
print('Distance finale :', util.distance_totale(result_bruteforce))
print(flush=True)

util.affiche_tournee(result_bruteforce)
