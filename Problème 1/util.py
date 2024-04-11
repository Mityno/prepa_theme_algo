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
