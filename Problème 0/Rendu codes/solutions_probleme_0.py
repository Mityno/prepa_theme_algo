import random
import time
import numpy as np
from matplotlib import pyplot as plt


def time_func(func):

    def inner(*args, **kwargs):
        bef = time.perf_counter()
        result = func(*args, **kwargs)
        aft = time.perf_counter()
        print(f'{func.__name__} took {aft - bef:.1e}s')
        return result

    return inner


# @time_func
def bruteforce(lst, start_point=None):
    curr = []
    last_end_point = float('-inf')
    lst = sorted(lst)

    def inner(last_end_point, curr):
        sub_solutions = []
        for (start, end) in lst:
            if start >= last_end_point:
                curr.append((start, end))
                sub_solutions.extend(inner(end, curr))
                curr.pop()

        solutions = sub_solutions[:]
        # le créneau actuel est possible et compte donc
        # comme une solution possible
        solutions.append(curr[:])
        return solutions

    # on ne garde que le planning qui contient le plus de créneaux
    return max(inner(last_end_point, curr), key=len)


# @time_func
def solve_efficient(lst):
    lst = lst[:]
    # tri selon la 2e composante, puis selon la 1re
    lst.sort(key=lambda x: x[::-1])

    solution = []
    # aucun créneau n'a encore été pris, donc on prend
    # une valeur de fin de créneau qui est la "plus petite" (dans R)
    last_end = float('-inf')
    for start, end in lst:
        # si le créneau commence après que le dernier sélectionné ait fini
        if start >= last_end:
            solution.append((start, end))
            last_end = end
    return solution


# Cas simple pour tester les fonctions
# lst = [(2, 5), (3, 9), (7, 10), (8, 9), (10, 11), (9, 10), (12, 13)]

# Partie vérification de l'implémentation de l'algorithme glouton
# n = 20
# lower_bound, higher_bound = 0, 15
# nb_tries = 1_000
# for _ in range(nb_tries):
#     # création de la liste de test
#     lst = []
#     for _ in range(n):
#         start = random.randrange(lower_bound, higher_bound - 1)
#         end = random.randrange(start + 1, higher_bound)
#         lst.append((start, end))

#     try:
#         assert len(bruteforce(lst)) == len(solve_efficient(lst))
#     except AssertionError:
#         # pour déboguer s'il y a une liste de créneaux pour laquelle
#         # `solve_efficient` ne renvoie pas la bonne valeur
#         print(lst)
#         exit()


# Partie vérification de l'efficacité temporelle de l'algorithme glouton
lower_bound, higher_bound = 0, 60
times = []
ns = list(map(int, np.linspace(20, 100_000, 10_000, dtype=int)))

# Création de la liste pour les tests
lst = []
for _ in range(max(ns)):
    start = random.randrange(lower_bound, higher_bound - 1)
    end = random.randrange(start + 1, higher_bound)
    lst.append((start, end))
print('Started', flush=True)

# pour vérifier le temps d'exécution pris par les manipulations sur les listes
lst_times = 0
for n in ns:
    # on réduit la taille de la liste à celle voulue
    # pour le test de paramètre n
    bef = time.perf_counter()
    temp_lst = lst[:n]
    aft = time.perf_counter()
    lst_times += aft - bef

    # on mesure le temps d'exécution de la fonction `solve_efficient`
    bef = time.perf_counter_ns()
    solve_efficient(temp_lst)
    aft = time.perf_counter_ns()

    times.append((aft - bef) * 1e-9)

# Pour enregistrer les résultats dans un fichier json
# (afin de les utiliser avec le fichier traitement_temps.py)
# import json
# with open('results.json', mode='w', encoding='utf-8') as file:
#     json.dump([ns, times], file)

# Affichage des résultats (temps en console et graphique)
print('solve time :', sum(times))
print('list manipulation time :', lst_times, flush=True)

# temps brut
plt.scatter(ns, times, s=10)

# temps divisé par n * log(n)
# plt.scatter(ns, np.array(times) / (ns * np.log2(ns)), s=10)

plt.tight_layout()
plt.show()
