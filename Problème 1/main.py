# Code de base pour le problème `Tournée du jardinier`

import util
import time
from matplotlib import pyplot as plt
import bruteforces

# Les différents calculs de tournee se font à partir des programmes des autres
# fichiers, chaque fichier contient un code pour exécuter directement des
# tests sur les différents jeu de données disponibles.
# Ce fichier contient le test des deux algorithmes de force brute sur les
# données de l'exemple 1

coords = util.lire_fichier_coords("exemple_1.txt")
coords = list(map(tuple, coords))

bef = time.perf_counter()
result_bruteforce = bruteforces.bruteforce(coords)
aft = time.perf_counter()

bef2 = time.perf_counter()
result_backtracking = bruteforces.bruteforce_backtracking(coords)
aft2 = time.perf_counter()

print(f'Temps d\'exécution 1 : {aft - bef:.2e}s')
print(f'Temps d\'exécution 2 : {aft2 - bef2:.2e}s')
print(flush=True)

util.affiche_tournee(result_bruteforce, show=False)
util.affiche_tournee(result_backtracking)
