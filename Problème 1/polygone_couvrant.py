import util
import bruteforce_algorithms
from matplotlib import pyplot as plt


def reduction_polygone_couvrant(coords, polygon_summits):
    # on enlève les coordonnées des sommets déjà atteints
    coords = [coord for coord in coords if coord not in polygon_summits]

    while coords:
        min_coord = None
        min_updated_distance = float('inf')
        min_coord_pos = None

        # trouver le point pour lequel casser un segment
        for coord in coords:
            for i in range(1, len(polygon_summits)):
                polygon_summits.insert(i, coord)
                curr_distance = util.distance_totale(polygon_summits)
                polygon_summits.pop(i)

                if curr_distance < min_updated_distance:
                    min_coord = coord
                    min_updated_distance = curr_distance
                    min_coord_pos = i

        # ajouter le point au bon endroit du polygone
        polygon_summits.insert(min_coord_pos, min_coord)
        coords.remove(min_coord)

        util.affiche_tournee(polygon_summits)

    return polygon_summits

# Pour trouver le polygone entourant initial :
# 1. On construit un polygone entourant en itérant sur les points les plus
# loins (et on dénoue quand besoin), on s'arrête quand on a trouvé un polygone
# qui entoure tous les points (vérification de "collision" -> gamedev)

# 2. On fait la même chose, mais sans s'arrêter : on trouve un chemin convexe qui "minimise" la distance

if __name__ == '__main__':
    # coords = util.lire_fichier_coords('exemple_losange_dense.txt')
    coords = util.lire_fichier_coords('exemple_2.txt')[:10]
    coords = list(map(tuple, coords))
    print(coords)
    # plt.scatter(*zip(*coords), s=10)

    # print(coords)
    # util.affiche_tournee(coords)
    # polygon_summits = [(0, 0), (-4, 3), (0, 6), (4, 2)]
    coords.append((0, 0))
    # polygon_summits = [
    #     min(coords, key=lambda coord: coord[0]),
    #     min(coords, key=lambda coord: coord[1]),
    #     max(coords, key=lambda coord: coord[0]),
    #     max(coords, key=lambda coord: coord[1]),
    # ]
    # # on enlève les doublons s'il y en a
    # print(polygon_summits)
    # polygon_summits = sorted(set(polygon_summits))
    # print(polygon_summits)
    polygon_summits = [min(coords), max(coords)]

    polygon_couvrant = reduction_polygone_couvrant(coords, polygon_summits)
    polygon_couvrant.remove((0, 0))
    coords.remove((0, 0))
    print(len(polygon_couvrant))
    util.affiche_tournee(polygon_couvrant, show=False)

    # polygon_couvrant_2 = [(0, 2), (-1, 2), (-1, 3), (-4, 3), (0, 6), (0, 4), (1, 4), (1, 3), (0, 3), (1, 2), (4, 2)]
    # print(len(polygon_couvrant_2))
    # util.affiche_tournee(polygon_couvrant_2)

    print(coords)
    result_backtracking = bruteforce_algorithms.bruteforce_backtracking(coords)
    util.affiche_tournee(result_backtracking, show=False)

    plt.show()
