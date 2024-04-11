import numpy as np
import time
import util
from matplotlib import pyplot as plt


def simulate_weighted_walk(weights, dist_mat, start=None):
    dist_mat = dist_mat.copy()

    coords_indices = list(range(len(dist_mat)))
    if start is None:
        start = np.random.choice(coords_indices)

    path = [start]
    # make the probability of going onto that point equals to 0
    dist_arr = dist_mat[start]
    weights_arr = weights[start]
    dist_mat[:, start] = float('inf')

    while (dist_mat < float('inf')).any():
        desirability = np.power((1 / dist_arr), dist_pow) * np.power(weights_arr, weight_pow)
        # normalize desirability so that it sums up to 1
        norm = desirability.sum()
        desirability = desirability / norm

        next_index = np.random.choice(
            coords_indices,
            p=desirability
            )

        path.append(next_index)
        dist_arr = dist_mat[next_index]
        weights_arr = weights[next_index]
        dist_mat[:, next_index] = float('inf')

    path.append(start)
    return path


def desirability_path_search(coords, nb_era=50, nb_sim_per_era=10, start_index=None):
    n = len(coords)
    coords = np.array(coords)
    weights = np.array([1.] * n**2).reshape(n, n)

    dist_mat = np.array([
        [util.distance(c1, c2) if not np.array_equal(c1, c2) else float('inf')
         for c2 in coords
         ] for c1 in coords
    ])

    for era_index in range(1, nb_era + 1):
        paths = []
        for _ in range(nb_sim_per_era):
            path = simulate_weighted_walk(weights, dist_mat)
            paths.append(path)

        for path in paths:
            for (i, j) in zip(path, path[1:]):
                weights[i, j] += 10

        # delete a part of previous weights so that the algorithm keep
        # exploring without having overflowing values
        weights *= 0.8
        xs, ys = np.where(weights < 1)
        for x, y in zip(xs, ys):
            weights[x, y] = 1

    final_path_indices = simulate_weighted_walk(weights, dist_mat, start_index)
    # last and first element are [0, 0] and shouldn't be returned
    final_path = coords[final_path_indices]
    final_path_unknoted = util.unknot_path(final_path)
    return final_path_unknoted[1:-1]


# Parameters
dist_pow = 11
weight_pow = 2
nb_era = 65
nb_sim_per_era = 20


if __name__ == '__main__':
    # A few examples of coordinates to test the program on
    # coords = util.lire_fichier_coords('exemple_losange_dense.txt')
    # coords = util.random_coords(200)
    coords = util.lire_fichier_coords('exemple_2.txt')

    coords = list(map(tuple, coords))
    if (0, 0) not in coords:
        coords.append((0, 0))
    coords = np.array(coords)
    (start_index, ), = np.where((coords == (0, 0)).sum(axis=1) == 2)

    # Make a few tries to try to get a good distance
    for _ in range(10):
        bef = time.perf_counter_ns()
        tournee = desirability_path_search(
            coords,
            nb_era=nb_era, nb_sim_per_era=nb_sim_per_era,
            start_index=start_index
        )
        aft = time.perf_counter_ns()
        print(f'Path search took : {(aft - bef)*1e-9:.2e}s', flush=True)

        print(f'Unknoting took : {(aft - bef)*1e-9:.2e}s', flush=True)
        path_distance = util.distance_avec_entree(tournee)
        print(f'Path total distance : {path_distance}', flush=True)
        # needs tuning depending on the threshold that we want shown values
        # to fulfill, here 680 is a quite good distance for this algorithm
        # on the exemple_2.txt data set
        if path_distance < 680:
            util.affiche_tournee(tournee)
            print('printed', flush=True)
    plt.show()