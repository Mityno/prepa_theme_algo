import numpy as np
import matplotlib.pyplot as plt
import util
import marche_aleatoire
import time


def main() -> None:
    nb_values = 70
    N = np.linspace(20, 200, num=nb_values, dtype=int)
    t = np.zeros(nb_values)
    for i, n in np.ndenumerate(N):
        coords = util.random_coords(n)
        start_time = time.perf_counter()
        marche_aleatoire.desirability_path_search(coords)
        end_time = time.perf_counter()
        t[i] = end_time - start_time
        print(f'Itération {i[0]} ; Taille {n} ; Temps {t[i]}', flush=True)

    print('Temps total :', sum(t), flush=True)
    fig, axes = plt.subplots(1, 2)
    axes[0].plot(N, t)
    axes[0].set_xlabel('Nombres de points')
    axes[0].set_ylabel('Temps d\'exécution (s)')
    axes[1].plot(N, t/N)
    axes[1].set_xlabel('Nombre de points n')
    axes[1].set_ylabel(r"Temps d'exécution divisé par $n$")
    fig.suptitle('Complexité empirique de l\'approche aléatoire')
    plt.show()

    return


if __name__ == '__main__':
    main()
