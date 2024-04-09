import util
import bruteforces
from matplotlib import pyplot as plt
from convex_hull import graham_scan


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

        # trouver le point pour lequel casser un segment
        for coord in coords:
            for i in range(1, len(polygon_summits)):
                polygon_summits.insert(i, coord)
                curr_distance = util.distance_totale_chemin(polygon_summits)
                polygon_summits.pop(i)

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

if __name__ == '__main__':
    # coords = util.lire_fichier_coords('exemple_losange_dense.txt')
    coords = util.lire_fichier_coords(r'Problème 1\exemple_2.txt')
    coords = list(map(tuple, coords))
    print(coords)

    coords.append((0, 0))
    plt.scatter(*zip(*coords), s=10)
    polygon_summits = graham_scan(coords)
    polygon_summits = sorted(set(polygon_summits), key=lambda coord: polygon_summits.index(coord))

    xs, ys = zip(*coords)
    plt.scatter(xs, ys)
    xp, yp = zip(*(polygon_summits+polygon_summits[0]))
    plt.plot(xp, yp)
    plt.scatter(xp, yp)
    plt.show()

    polygon_couvrant = reduction_polygone_couvrant(coords.copy(), polygon_summits)

    start_pos = polygon_couvrant.index((0, 0))
    polygon_couvrant = rotate_list(polygon_couvrant, start_pos)
    polygon_couvrant.remove((0, 0))

    coords.remove((0, 0))
    print(len(polygon_couvrant), flush=True)
    util.affiche_tournee(polygon_couvrant, show=False)

    # result_backtracking = bruteforces.bruteforce_backtracking(coords)
    # util.affiche_tournee(result_backtracking, show=False)

    plt.show()
