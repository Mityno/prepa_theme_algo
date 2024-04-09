import numpy as np


import numpy as np
import matplotlib.pyplot as plt


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
        

def rand_coord(N):
    return np.random.randn(N, 2)


def mat_dist(coords):
    n = len(coords)
    M = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            M[i, j] = distance(coords[i] , coords[j])
    return M

def distance_sortante_max(i, M, liens):
    dists_i = M[i].copy()
    if liens[i] is None:
        first_max = np.max(dists_i)
        dists_i[np.where(dists_i == first_max)[0]] = -float('inf')
        snd_max = np.max(dists_i)
    elif len(liens[i]) == 1:
        first_max = liens[i]
        dists_i[np.where(dists_i == first_max)[0]] = -float('inf')
        snd_max = np.max(dists_i)
    else:
        first_max = snd_max = 0
    return first_max + snd_max

def trouver_j_dist_min(i, M, liens):
    dists_i = M[i].copy()
    for j in range(len(dists_i)):
        if dists_i[j] <= 0:
            dists_i[j] = float('inf')
    return np.where(dists_i == np.min(dists_i))[0][0]

def somme_deg(liens):
    somme = 0
    for e in liens:
        if e is not None:
            somme += len(e)
    return somme

def espèces_en_danger(coords):
    n = len(coords)
    M = mat_dist(coords)
    liens = [None]*n
    while somme_deg(liens) != 2*n:
        dist_sorts = np.zeros(n)
        for i in range(n):
            dist_sorts[i] = distance_sortante_max(i, M, liens)
        imax = np.where(dist_sorts == np.max(dist_sorts))[0][0]
        jmin = trouver_j_dist_min(imax, M, liens)
        if liens[imax] is None:
            liens[imax] = [jmin]
            M[imax, jmin] = -1
            M[jmin, imax] = -1
        elif len(liens[imax]) == 1:
            liens[imax].append(jmin)
            maj = np.array([-1]*n)
            M[imax, :] = maj
            M[:, imax] = maj
    return liens

        
        

coords = rand_coord(6)

liens = espèces_en_danger(coords)

print(liens)






























