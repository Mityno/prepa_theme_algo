import util
import bruteforces
from matplotlib import pyplot as plt
from convex_hull import graham_scan
import time


def rotate_list(lst, n):
    return lst[n:] + lst[:n]


def reduction_polygone_couvrant(coords, polygon_summits, show=False):
    # on enlève les coordonnées des sommets déjà atteints
    for summit in polygon_summits:
        coords.remove(summit)

    polygon_summits.append(polygon_summits[0])

    while coords:
        min_coord = None
        min_updated_distance = float('inf')
        min_coord_pos = None

        last_polygon_distance = util.distance_totale_chemin(polygon_summits)

        # trouver le point pour lequel casser un segment
        for coord in coords:
            for i in range(1, len(polygon_summits)):
                curr_distance = last_polygon_distance
                curr_distance -= util.distance(polygon_summits[i-1], polygon_summits[i])
                curr_distance += util.distance(polygon_summits[i-1], coord) + util.distance(coord, polygon_summits[i])

                if curr_distance < min_updated_distance:
                    min_coord = coord
                    min_updated_distance = curr_distance
                    min_coord_pos = i

        # ajouter le point au bon endroit du polygone
        polygon_summits.insert(min_coord_pos, min_coord)
        coords.remove(min_coord)

        if show:
            if coords:
                xs, ys = zip(*coords)
                plt.scatter(xs, ys)
            xp, yp = zip(*polygon_summits)
            plt.plot(xp, yp)
            plt.scatter(xp, yp)
            plt.show()


    polygon_summits.pop()
    return polygon_summits

# Pour trouver le polygone entourant initial :
# 1. On construit un polygone entourant en itérant sur les points les plus
# loins (et on dénoue quand besoin), on s'arrête quand on a trouvé un polygone
# qui entoure tous les points (vérification de "collision" -> gamedev)

# 2. On fait la même chose, mais sans s'arrêter : on trouve un chemin convexe qui "minimise" la distance


def path_finder(coords: list[tuple[float, float]], quiet: bool = True) -> list[tuple[float, float]]:
    if not (0,0) in coords:
        coords.append((0,0))

    polygon_summits = graham_scan(coords)
    polygon_summits = sorted(set(polygon_summits), key=lambda coord: polygon_summits.index(coord))

    if not quiet:
        # Affichage des points et de leur enveloppe convexe
        xs, ys = zip(*coords)
        plt.scatter(xs, ys)
        xp, yp = zip(*(polygon_summits+[polygon_summits[0]]))
        plt.plot(xp, yp)
        plt.scatter(xp, yp)
        plt.show()

    # Transformation de l'enveloppe en chemin valide
    polygon_path = reduction_polygone_couvrant(coords.copy(), polygon_summits)

    # Réorganisation du chemin pour qu'il démarre en (0,0)
    start_pos = polygon_path.index((0, 0))
    polygon_path = rotate_list(polygon_path, start_pos)

    polygon_path.remove((0, 0))
    coords.remove((0, 0))
    return polygon_path



if __name__ == '__main__':
    # coords = util.lire_fichier_coords(r'Problème 1\exemple_nathael_ninon.txt')
    coords = util.lire_fichier_coords(r'Problème 1\exemple_2.txt')
    # coords = util.lire_fichier_coords(r'Problème 1\exemple_losange_dense.txt')

    coords = list(map(tuple, coords))
    # coords = util.random_coords(80)
    
    start_time = time.perf_counter()
    polygon_path = path_finder(coords, quiet=True)
    end_time = time.perf_counter()
    print(f'{path_finder.__name__} took {end_time - start_time:.2f}s to run')

    util.affiche_tournee(polygon_path, show=False)

    # Si coords compte suffisamment peu (<12), on peut comparer avec la solution optimale obtenue en bruteforce
    # result_backtracking = bruteforces.bruteforce_backtracking(coords)
    # util.affiche_tournee(result_backtracking, show=False)

    plt.show()
