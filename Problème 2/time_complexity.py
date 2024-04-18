import numpy as np
import matplotlib.pyplot as plt
import util
import recursive_algorithm
import algo_iteratif
import time
import sys


def main() -> None:
    big_word_list = util.import_text_as_list('./Problème 2/recherche_complet.txt')
    nb_values = 100
    N = np.linspace(500, len(big_word_list), num=nb_values, dtype=int)
    t = np.zeros(nb_values)
    for i, n in np.ndenumerate(N):
        word_list = big_word_list[:n]
        sys.setrecursionlimit(len(word_list)*10)
        start_time = time.perf_counter()
        algo_iteratif.iterative_search(word_list, 80)
        end_time = time.perf_counter()
        t[i] = end_time - start_time
        print(f'Itération {i[0]} ; Taille {n} ; Temps {t[i]}', flush=True)

    print('Temps total :', sum(t), flush=True)
    fig, axes = plt.subplots(1, 2)
    axes[0].plot(N, t)
    axes[0].set_xlabel('Nombres de mots')
    axes[0].set_ylabel('Temps d\'exécution (s)')
    axes[1].plot(N, t/(N**2))
    axes[1].set_xlabel('Nombre de mots n')
    axes[1].set_ylabel(r"Temps d'exécution divisé par $n^2$")
    fig.suptitle('Complexité empirique de l\'algorithme récursif')
    plt.show()

    return


if __name__ == '__main__':
    main()
