import numpy as np
import util


def mat_dist(coords):
    n = len(coords)
    M = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            M[i, j] = util.distance(coords[i], coords[j])
    return M


def distance_sortante_max(i, M, liens):
    dists_i = M[i].copy()
    if len(liens[i]) == 0:
        first_max = np.max(dists_i)
        dists_i[np.where(dists_i == first_max)[0]] = -float("inf")
        snd_max = np.max(dists_i)
    elif len(liens[i]) == 1:
        first_max = liens[i]
        dists_i[np.where(dists_i == first_max)[0]] = -float("inf")
        snd_max = np.max(dists_i)
    else:
        first_max = snd_max = 0
    return first_max + snd_max


def trouver_j_dist_min(i, M, liens):
    dists_i = M[i].copy()
    for j in range(len(dists_i)):
        if dists_i[j] <= 0:
            dists_i[j] = float("inf")
    return np.where(dists_i == np.min(dists_i))[0][0]


def somme_deg(liens):
    somme = 0
    for e in liens:
        somme += len(e)
    return somme


def dfs(graph, start, end, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    if start == end:
        return True
    for neighbor in graph[start]:
        if neighbor not in visited:
            if dfs(graph, neighbor, end, visited):
                return True
    return False


def trouver_chemin(liens, i, j):
    if i < 0 or i >= len(liens) or j < 0 or j >= len(liens):
        return False
    visited = set()
    return dfs(liens, i, j, visited)


def maj_M_imax(coords, M, imax, liens):
    for j in range(len(coords)):
        if trouver_chemin(liens, imax, j):
            M[imax, j] = -1
            M[j, imax] = -1


def maj_M_jmin_imax(liens, imax, jmin, M, maj):
    if len(liens[imax]) == 1:
        M[imax, jmin] = -1
        M[jmin, imax] = -1
    elif len(liens[imax]) == 2:
        M[imax, :] = maj
        M[:, imax] = maj
    if len(liens[jmin]) == 1:
        M[imax, jmin] = -1
        M[jmin, imax] = -1
    elif len(liens[jmin]) == 2:
        M[jmin, :] = maj
        M[:, jmin] = maj


def forme_affichage(chemin, coords):
    chemincoords = []
    point_act = chemin[0][0]
    point_prec = 0
    rep = [point_act]
    while len(rep) != len(chemin) - 1:
        for j in chemin[point_act]:
            if j != point_prec:
                point_prec = point_act
                point_act = j
                rep.append(point_act)
                break
    for i in rep:
        chemincoords.append(coords[i])
    return np.array(chemincoords)


def exploit(chemin):
    coords_exploit = list(map(tuple, chemin))
    coords_exploit = [(0, 0)] + coords_exploit + [(0, 0)]
    coords_exploit = util.unknot_path(coords_exploit)
    coords_exploit.pop()
    coords_exploit.pop(0)
    return coords_exploit


def espèces_en_danger(coords):
    n = len(coords)  # initialisation
    M = mat_dist(coords)  # matrice de distance des points
    liens = [[] for i in range(n)]  # liste d'adjacence du graphe associé aux points
    maj = np.array([-1] * n)  # initialisation

    while somme_deg(liens) != 2 * n - 2:  # construit le chemin entre n-2 points

        dist_sorts = np.zeros(
            n
        )  # trouve le sommet le plus en danger(ie éloigné des autres)
        for i in range(n):
            dist_sorts[i] = distance_sortante_max(i, M, liens)
        imax = np.where(dist_sorts == np.max(dist_sorts))[0][0]

        maj_M_imax(coords, M, imax, liens)  # met à jour la matrice de distance M
        # car on va utiliser imax pour créer la prochaine arête

        jmin = trouver_j_dist_min(
            imax, M, liens
        )  # trouve le point le plus proche de imax

        liens[imax].append(jmin)  # crée une arête entre jmin et imax
        liens[jmin].append(imax)

        maj_M_jmin_imax(liens, imax, jmin, M, maj)  # maj M car création d'une arête

    deux_derniers_pts = []  # fait le lien entre les deux derniers points
    for i in range(n):
        if len(liens[i]) == 1:
            deux_derniers_pts.append(i)
    p1 = deux_derniers_pts[0]
    p2 = deux_derniers_pts[1]
    liens[p1].append(p2)
    liens[p2].append(p1)

    chemin = forme_affichage(liens, coords)  # transforme la matrice d'adjacence
    # solution en chemin exploitable par
    return exploit(chemin)  # affiche_tournee


if __name__ == "__main__":
    coords = util.lire_fichier_coords("exemple_2.txt")
    # coords = util.lire_fichier_coords("exemple_nathael_ninon.txt")
    # coords = util.random_coords(200)

    chemin = espèces_en_danger(coords)
    util.affiche_tournee(chemin)
