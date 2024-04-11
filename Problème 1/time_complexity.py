import numpy as np
import matplotlib.pyplot as plt
import util
import convex_path
import time

def random_coords(n):
    coords = np.random.normal(loc=0, scale=25, size=(n, 2))
    return list(map(tuple, coords))



def main() -> None:
    N = np.linspace(50, 600, num=70, dtype=int)
    t = np.zeros(70)
    for i, n in np.ndenumerate(N):
        coords = random_coords(n)
        start_time = time.perf_counter()
        convex_path.path(coords)
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
    fig.suptitle('Complexité empirique de la méthode de l\'enveloppe convexe')
    plt.show()

    return




if __name__ == '__main__':
    main()

