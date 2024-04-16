import numpy as np
import time
import util
from matplotlib import pyplot as plt
import contextlib
import convex_path


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

    shortest_path = None
    minimum_dist_bef_unknot = float('inf')
    minimum_dist_aft_unknot = float('inf')

    for era_index in range(1, nb_era + 1):
        paths = []
        for _ in range(nb_sim_per_era):
            path = simulate_weighted_walk(weights, dist_mat)
            paths.append(path)

        for path in paths:
            for (i, j) in zip(path, path[1:]):
                weights[i, j] += 10

            real_path = coords[path]
            curr_dist = util.distance_totale_chemin(real_path)
            if curr_dist < minimum_dist_bef_unknot ** 1.006:
                real_path = util.unknot_path(real_path)
                real_path_dist = util.distance_totale_chemin(real_path)
                if real_path_dist < minimum_dist_aft_unknot:
                    # print(real_path_dist, flush=True)
                    minimum_dist_bef_unknot = curr_dist
                    minimum_dist_aft_unknot = real_path_dist
                    shortest_path = real_path

        # delete a part of previous weights so that the algorithm keep
        # exploring without having overflowing values
        weights *= 0.8
        weights[np.where(weights < 1)] = 1

    shortest_path = list(map(tuple, shortest_path))
    shortest_path.pop()  # remove last point (it shouldn't be returned)
    zero_index = shortest_path.index((0, 0))
    shortest_path = util.rotate_list(shortest_path, zero_index)
    return shortest_path[1:]


# Parameters
dist_pow = 13  # 11
weight_pow = 1.2  # 2
nb_era = 10  # 65
nb_sim_per_era = 15  # 20
threshold = 660  # 630 - 1300 - 880
# best : 632.13


if __name__ == '__main__':
    # A few examples of coordinates to test the program on
    # coords = util.lire_fichier_coords('exemple_losange_dense.txt')
    # coords = util.random_coords(50)
    coords = util.lire_fichier_coords('exemple_2.txt')
    # coords = util.lire_fichier_coords('exemple_3.txt')

    coords = list(map(tuple, coords))
    convex_sol, convex_sol_dist = convex_path.path(list(map(tuple, coords)))
    util.affiche_tournee(convex_sol)

    if (0, 0) not in coords:
        coords.append((0, 0))
    coords = np.array(coords)
    (start_index, ), = np.where((coords == (0, 0)).sum(axis=1) == 2)

    # threshold = convex_sol_dist
    threshold = 645

    # Make a few tries to try to get a good distance
    with open('ignore/log_random.txt', mode='a') as file:
        # with contextlib.redirect_stdout(file):
            for _ in range(10):
                bef = time.perf_counter_ns()
                tournee = desirability_path_search(
                    coords,
                    nb_era=nb_era, nb_sim_per_era=nb_sim_per_era,
                    start_index=start_index
                )
                aft = time.perf_counter_ns()
                print(f'Path search took : {(aft - bef)*1e-9:.2e}s', flush=True)

                path_distance = util.distance_avec_entree(tournee)
                print(f'Path total distance : {path_distance:.2f} {threshold - path_distance:.2f}', flush=True)
                # needs tuning depending on the threshold that we want shown values
                # to fulfill, here 680 is a quite good distance for this algorithm
                # on the exemple_2.txt data set
                if path_distance < threshold:
                    print('printed', flush=True)
                    util.affiche_tournee(tournee, show=False)

                if path_distance < threshold + 8:
                    print(tournee, flush=True)
            # print(tournee)
            plt.show()
