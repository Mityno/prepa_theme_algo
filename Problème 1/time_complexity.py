import numpy as np
import matplotlib.pyplot as plt
import util
import convex_path
import time
from jardinier_especes_en_danger import espèces_en_danger


def main() -> None:
    N = np.linspace(50, 600, num=70, dtype=int)
    t = np.zeros(70)
    for i, n in np.ndenumerate(N):
        coords = util.random_coords(n)
        coords.insert(0, (0., 0.))
        start_time = time.perf_counter()
        espèces_en_danger(coords)
        end_time = time.perf_counter()
        t[i] = end_time - start_time
        print(f'Itération {i[0]} ; Taille {n} ; Temps {t[i]}')

    fig, axes = plt.subplots(1, 2)
    axes[0].plot(N, t)
    axes[0].set_xlabel('Nombres de points')
    axes[0].set_ylabel('Temps d\'exécution (s)')
    axes[1].plot(N, t/(N**3))
    axes[1].set_xlabel('Nombre de points n')
    axes[1].set_ylabel(r"Temps d'exécution divisé par $n^3$")
    fig.suptitle('Complexité empirique de la méthode des espèces en danger')
    plt.show()

    return




if __name__ == '__main__':
    main()

