import numpy as np
import matplotlib.pyplot as plt
import util
import recursive_algorithm
import iterative_algorithm
import time
import sys
import json


def main():
    # runs some test to study the time depency of some implementation to n,
    # the numbers of words of the text

    big_word_list = util.import_words_from_text('recherche_complet.txt')
    nb_values = 100

    N = np.linspace(500, len(big_word_list), num=nb_values, dtype=int)
    t = np.zeros(nb_values)

    for i, n in np.ndenumerate(N):
        word_list = big_word_list[:n]  # get a word list of the wanted size
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
    pass

    # main()

    # Étude de la complexité par rapport à n
    # with open('exec iteratif.txt', mode='r') as file:  # autre fichier : exec recursif
    #     datas = file.read()

    # lines = datas.split('\n')
    # ns, ts = [], []
    # for line in lines:
    #     n_str, t_str = line.split()
    #     ns.append(float(n_str))
    #     ts.append(float(t_str))

    # ns, ts = np.array(ns), np.array(ts)

    # fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    # axes[0].plot(ns, ts)
    # axes[0].set_xlabel('Nombres de mots')
    # axes[0].set_ylabel('Temps d\'exécution (s)')
    # axes[1].plot(ns, ts / (ns))
    # axes[1].set_xlabel('Nombre de mots n')
    # axes[1].set_ylabel(r"Temps d'exécution divisé par $n$")
    # fig.suptitle('Complexité empirique de l\'algorithme itératif')
    # fig.tight_layout()

    # fig.savefig('Ignore/Complexité itératif.pdf', format='pdf', dpi=300)
    # plt.show()

    # Étude de la complexité par rapport à L, valeur dans `algorithm_L_time_testing.txt`
    # all_values = []
    # with open('algorithm_L_time_testing.txt', mode='r') as file:
    #     for line in file:
    #         all_values.append(json.loads(line.strip()))

    # # pour faire une convolution et avoir une moyenne lisée
    # # mask = np.array([1 / 5] * 5)

    # for (line_lengths, times), name in zip(all_values, ('itératif', 'récursif')):
    #     line_lengths = np.array(line_lengths)
    #     times = np.array(times)

    #     # line_lengths = np.convolve(line_lengths, mask, mode='valid')
    #     # times = np.convolve(times, mask, mode='valid')

    #     fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    #     axes[0].plot(line_lengths, times)
    #     axes[0].set_xlabel('Longueur des lignes')
    #     axes[0].set_ylabel('Temps d\'exécution (s)')
    #     axes[1].plot(line_lengths, times / line_lengths)
    #     axes[1].set_xlabel('Longueur des lignes')
    #     axes[1].set_ylabel(r"Temps d'exécution divisé par $L$")
    #     fig.suptitle(f'Complexité empirique de l\'algorithme {name}')
    #     fig.tight_layout()

    #     # fig.savefig(f'Ignore/Complexité par rapport à L {name}.pdf', format='pdf', dpi=300)
    #     plt.show()
