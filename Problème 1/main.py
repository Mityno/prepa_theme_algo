# Code de base pour le problème `Tournée du jardinier`

import util
import time
from matplotlib import pyplot as plt
import bruteforces


def calcule_tournee(coords):
    return coords  # A MODIFIER


coords = util.lire_fichier_coords("exemple_2.txt")[35:50]
coords = list(map(tuple, coords))
print(len(coords))

# coords = util.lire_fichier_coords("exemple_1.txt")
# print(coords)

<<<<<<< HEAD
# bef = time.perf_counter()
# result_backtracking = bruteforces.bruteforce_backtracking(coords)
# aft = time.perf_counter()
=======
bef = time.perf_counter()
result_bruteforce = bruteforces.bruteforce(coords)
aft = time.perf_counter()
result_backtracking = bruteforces.bruteforce_backtracking(coords)
>>>>>>> 04f1b632f7ac89da117a21511598812db8e97c18

bef2 = time.perf_counter()
result_backtracking_2 = bruteforces.bruteforce_backtracking_2(tuple(coords))
aft2 = time.perf_counter()

# result_bruteforce = bruteforces.bruteforce(coords)

# assert util.distance_avec_entree(result_bruteforce) == util.distance_avec_entree(result_backtracking)

# print(f'Temps d\'exécution 1 : {aft - bef:.2e}')
print(f'Temps d\'exécution 2 : {aft2 - bef2:.2e}')
# print('Distance finale :', util.distance_avec_entree(result_bruteforce))
print(flush=True)

# util.affiche_tournee(result_bruteforce, show=False)
util.affiche_tournee(result_backtracking_2, show=False)
# util.affiche_tournee(result_backtracking)
