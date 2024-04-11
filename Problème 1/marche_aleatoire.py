import numpy as np
import time
import util


def get_path(path_indices, coords):
    return coords[path_indices]
    for i in range(len(path_indices) - 1):
        final_path.append(
            (coords[path_indices[i]], coords[path_indices[i+1]])
        )
    return final_path



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

        desirability = pow((1 / dist_arr), dist_pow) * pow(weights_arr, weight_pow)
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
    weights = np.array([1] * n**2).reshape(n, n)

    dist_mat = np.array([
        [util.distance(c1, c2) if not np.array_equal(c1, c2) else float('inf')
         for c2 in coords
        ] for c1 in coords
    ])

    for era_index in range(1, nb_era + 1):
        paths = []
        weights_reduced = weights / (n * era_index)
        # print(weights[:5, :5])
        # print(weights_reduced[:5, :5])
        # print(weights_reduced.sum(), weights.sum() - n**2)
        # print()
        for _ in range(nb_sim_per_era):
            path = simulate_weighted_walk(weights_reduced, dist_mat, start_index)
            paths.append(path)

        for path in paths:
            for (i, j) in zip(path, path[1:]):
                weights[i, j] += 1

    weights_reduced = weights / (n * era_index)
    final_path_indices = simulate_weighted_walk(weights_reduced, dist_mat, start_index)
    return get_path(final_path_indices, coords)


# coords = util.lire_fichier_coords('exemple_1.txt')
coords = util.lire_fichier_coords('exemple_2.txt')
(start_index, _), _ = np.where(coords == (0, 0))

dist_pow = 8
weight_pow = 8

bef = time.perf_counter()
tournee = desirability_path_search(coords, nb_era=100, nb_sim_per_era=20, start_index=start_index)
aft = time.perf_counter()
print(f'Path search took : {aft - bef:.2f}s', flush=True)
util.affiche_tournee(tournee)

# path_indices = simulate_weighted_walk(weights, dist_mat, start=start_index)
# tournee = get_path(path_indices, coords)
# util.affiche_tournee(tournee)
