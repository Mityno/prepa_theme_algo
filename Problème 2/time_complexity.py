import numpy as np
import matplotlib.pyplot as plt
import util
import recursive_algorithm
import iterative_algorithm
import time
import sys


def main() -> None:
    big_word_list = util.import_words_from_text('recherche_complet.txt')
    nb_values = 30
    N = np.linspace(500, len(big_word_list) / 15, num=nb_values, dtype=int)
    t = np.zeros(nb_values)
    for i, n in np.ndenumerate(N):
        word_list = big_word_list[:n]
        print(len(word_list))
        sys.setrecursionlimit(len(word_list)*10)
        start_time = time.perf_counter()
        iterative_algorithm.iterative_search(word_list, 80)
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

    # with open('exec iteratif.txt', mode='r') as file:
    #     datas = file.read()

    # lines = datas.split('\n')
    # ns, ts = [], []
    # for line in lines:
    #     n_str, t_str = line.split()
    #     ns.append(float(n_str))
    #     ts.append(float(t_str))

    # ns, ts = np.array(ns), np.array(ts)
    # print(ns)
    # print(ts)

    # print(ts / (ns**2))

    # fig, axes = plt.subplots(1, 2)
    # axes[0].plot(ns, ts)
    # axes[0].set_xlabel('Nombres de mots')
    # axes[0].set_ylabel('Temps d\'exécution (s)')
    # axes[1].plot(ns, ts / (ns))
    # axes[1].set_xlabel('Nombre de mots n')
    # axes[1].set_ylabel(r"Temps d'exécution divisé par $n^2$")
    # fig.suptitle('Complexité empirique de l\'algorithme récursif')
    # plt.show()