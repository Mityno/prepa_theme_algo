import numpy as np
import util


def get_n_th_elem_deco(n):
    def inner(seq):
        return seq[n]
    return inner


get_first = get_n_th_elem_deco(0)


def lst_find(lst, value, func=None):
    if func is None:
        func = lambda x: x

    for i, elem in enumerate(lst):
        if func(elem) == value:
            return i

    return None


def exist_loop(start, end, paths):

    while start != end:
        next_vertice = lst_find(paths, start, func=get_first)

        if next_vertice is None:
            return False

        start = paths[next_vertice][1]
    return True


def algo_glouton(coords):
    # make a copy and convert to the right format for coords
    coords = list(map(tuple, coords))

    dist_mat = np.array([
        [util.distance(c1, c2) if c1 != c2 else float('+inf')
        for c1 in coords
        ] for c2 in coords
        ])

    vertices_usage_counter = [0] * len(coords)
    solution = []
    point_first_usage_history = []

    while (dist_mat < float('inf')).any():

        min_pos = dist_mat.argmin()
        x_min, y_min = divmod(min_pos, len(coords))
        x_min, y_min = sorted(
            (x_min, y_min),
            key=lambda point: point_first_usage_history.index(point) if point in point_first_usage_history else float('inf'),
        )

        dist_mat[x_min, y_min] = float('+inf')
        dist_mat[y_min, x_min] = float('+inf')

        if exist_loop(x_min, y_min, solution):
            continue

        solution.append((x_min, y_min))

        if x_min not in point_first_usage_history:
            point_first_usage_history.append(x_min)
        if y_min not in point_first_usage_history:
            point_first_usage_history.append(y_min)

        vertices_usage_counter[x_min] += 1
        vertices_usage_counter[y_min] += 1

        if vertices_usage_counter[x_min] >= 2:
            dist_mat[x_min, :] = float('+inf')
            dist_mat[:, x_min] = float('+inf')

        if vertices_usage_counter[y_min] >= 2:
            dist_mat[y_min, :] = float('+inf')
            dist_mat[:, y_min] = float('+inf')

    #     print(dist_mat)

    # print(len(solution))
    # print(len(coords))
    # exit()
    path = make_path(coords, solution)

    return path


def make_path(coords, path_indices):
    solution = []
    path_indices = path_indices.copy()
    start = path_indices[0][0]
    end = start
    next_index = None
    print(path_indices)

    while path_indices:
        next_index = lst_find(path_indices, True, func=lambda x: end in x)
        print(next_index, end)
        print(path_indices)
        (new_start, new_end) = path_indices.pop(next_index)
        end = new_start if new_start != end else new_end
        solution.append(coords[end])

    return solution


if __name__ == '__main__':

    # coords = util.lire_fichier_coords('exemple_nathael_ninon.txt')
    coords = util.lire_fichier_coords('exemple_2.txt')[:20]
    coords = list(map(tuple, coords))
    coords.append((0, 0))
    # print(coords)

    tournee_glouton = algo_glouton(coords)
    print(tournee_glouton, flush=True)
    zero_pos = tournee_glouton.index((0, 0))
    tournee_glouton = util.rotate_list(tournee_glouton, zero_pos + 1)
    tournee_glouton.pop()
    print(tournee_glouton, flush=True)
    util.affiche_tournee(tournee_glouton)

    # seq_no_loop = [(0, 1), (2, 0), (5, 4)]
    # seq_loop = [(0, 1), (2, 0), (5, 4), (1, 2)]
    # seq_loop = [(1, 3), (3, 2)]

    # print(exist_loop(1, 2, seq_loop))
    # print(exist_loop(1, 0, seq_loop))
