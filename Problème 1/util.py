# Fonctions utilitaires fournies pour le problème `Tournée du jardinier`
import numpy as np
import matplotlib.pyplot as plt


def random_coords(n) -> list[tuple[float, float]]:
    coords = np.random.normal(loc=0, scale=25, size=(n, 2))
    return list(map(tuple, coords))


def lire_fichier_coords(nom_fichier):
    coords = []
    with open(nom_fichier) as f:
        try:
            for ligne in f:
                if not ligne.isspace():
                    # print(ligne)
                    x, y = ligne.split(" ")
                    coords.append((float(x), float(y)))
        except:
            raise ValueError("Fichier de coordonnées mal formé")
    return np.array(coords)


def distance(p1, p2):
    return ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** (1 / 2)


def distance_avec_entree(coords):
    if len(coords) == 0:
        return 0
    dist = distance((0, 0), coords[0]) + distance(coords[-1], (0, 0))
    for i in range(1, len(coords)):
        dist += distance(coords[i], coords[i - 1])
    return dist


def distance_totale_chemin(coords):
    dist = 0
    for i in range(len(coords) - 1):
        dist += distance(coords[i], coords[i + 1])
    return dist


def affiche_tournee(coords, show=True):

    x, y = zip((0, 0), *coords, (0, 0))
    fig, ax = plt.subplots()

    ax.scatter(x, y, s=8)
    ax.scatter(0, 0, color="red")
    ax.plot(x, y)
    ax.set_title(f"Distance totale : {distance_avec_entree(coords):.3f}")

    if show:
        plt.show()


def unknot_path(path):
    path = list(map(tuple, path))
    longest_intersection = 'not none'

    while longest_intersection is not None:
        longest_intersection = None
        longest_intersection_length = 0
        for i, (c1, c2) in enumerate(zip(path, path[1:])):
            for j, (c3, c4) in enumerate(zip(path, path[1:])):
                if c1 == c3 or c1 == c4 or c2 == c3 or c2 == c4:
                    continue

                x1, y1 = c1
                x2, y2 = c2
                x3, y3 = c3
                x4, y4 = c4

                # check if (c3, c4) intersect (c1, c2)
                if y1 != y2:
                    a, b = get_line_param(x1, x2, y1, y2)
                    c3_relative_pos = evaluate_line(*c3, a, b)
                    c4_relative_pos = evaluate_line(*c4, a, b)
                    c3_c4_coef = c3_relative_pos * c4_relative_pos
                else:
                    if y3 < y4:
                        c3_c4_coef = -1 if y3 <= y1 <= y4 else 1
                    else:
                        c3_c4_coef = -1 if y4 <= y1 <= y3 else 1

                # check if (c1, c2) intersect (c3, c4)
                if y3 != y4:
                    a, b = get_line_param(x3, x4, y3, y4)
                    c1_relative_pos = evaluate_line(*c1, a, b)
                    c2_relative_pos = evaluate_line(*c2, a, b)
                    c1_c2_coef = c1_relative_pos * c2_relative_pos
                else:
                    if y1 < y2:
                        c1_c2_coef = -1 if y1 <= y3 <= y2 else 1
                    else:
                        c1_c2_coef = -1 if y2 <= y3 <= y1 else 1

                # if there is no intersection
                if not (c1_c2_coef < 0 and c3_c4_coef < 0):
                    continue

                intersection_length = max(distance(c1, c2), distance(c3, c4))
                if intersection_length > longest_intersection_length:
                    # print('here', intersection_length, c1, c2, c3, c4)
                    longest_intersection = (i, j)
                    longest_intersection_length = intersection_length
            # if breaked:
            #     # affiche_tournee(path)
            #     break

        if longest_intersection is not None:
            i, j = longest_intersection
            # affiche_tournee(path, show=False)
            # print(i, j, flush=True)
            path[i + 1:j + 1] = path[i + 1:j + 1][::-1]
            # (c1, c2), (c3, c4) = path[i:i+2], path[j:j+2]
        #     path[i + 1] = c3
        #     path[j] = c2
        # else:
        #     path[i] = c4
        #     path[j + 1] = c1
            # affiche_tournee(path)
    return path


def get_line_param(x1, x2, y1, y2):
    return (
        (x1 - x2) / (y2 - y1),
        (-y2 * x1 + y1 * x2) / (y2 - y1),
        )


def evaluate_line(x, y, a, b):
    return x + a*y + b


if __name__ == '__main__':
    tournee = [[0.0, 0.0], [8.0, 2.17], [21.67, -6.33], [17.83, -18.0], [2.67, -25.0], [-3.0, -27.5], [-18.33, -23.67], [-19.17, -17.33], [2.83, 15.83], [-9.17, 19.33], [-12.17, 10.83], [-25.83, 27.83], [-13.5, 30.5], [-5.67, 36.33], [0.5, 40.83], [5.33, 49.83], [18.83, 44.67], [28.83, 18.33], [3.5, 33.83], [1.0, 34.0], [0.0, 0.0]]

    affiche_tournee(tournee)
    unknoted_path = unknot_path(tournee)
    affiche_tournee(unknoted_path)
