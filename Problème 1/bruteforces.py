import util
import functools


def bruteforce(coords):
    solution = None
    sol_distance = float('inf')

    def inner(coords, curr):
        nonlocal solution, sol_distance

        if not coords:
            curr_distance = util.distance_avec_entree(curr)
            if curr_distance < sol_distance:
                solution = curr[:]
                sol_distance = curr_distance
            return

        for coord in frozenset(coords):
            coords.discard(coord)
            curr.append(coord)
            inner(coords, curr)
            curr.pop()
            coords.add(coord)

    coords = list(map(tuple, coords))
    inner(set(coords), [])
    return solution


def bruteforce_backtracking(coords):
    solution = None
    sol_distance = float('inf')

    def inner(coords, curr):
        nonlocal solution, sol_distance

        if util.distance_avec_entree(curr) >= sol_distance:
            return

        if not coords:
            curr_distance = util.distance_avec_entree(curr)
            if curr_distance < sol_distance:
                solution = curr[:]
                sol_distance = curr_distance
            return

        for coord in frozenset(coords):
            coords.discard(coord)
            curr.append(coord)
            inner(coords, curr)
            curr.pop()
            coords.add(coord)

    coords = list(map(tuple, coords))
    inner(set(coords), [])
    return solution


@functools.cache
def bruteforce_backtracking_2(coords):
    """
    Non optimal (parfois la solution est un peu moins bonne)
    Mais tourne plus vite que les autres bruteforce :
    limite acceptable en temps vers n=14
    """
    solution = None
    sol_distance = float('inf')

    def inner(coords, curr):
        nonlocal solution, sol_distance

        # backtracking
        if curr and (util.distance_avec_entree(curr)
            + util.distance_totale_chemin(bruteforce_backtracking_2(frozenset(coords)))
            ) >= sol_distance:
            return

        if not coords:
            curr_distance = util.distance_avec_entree(curr)
            if curr_distance < sol_distance:
                solution = curr[:]
                sol_distance = curr_distance
            return

        for coord in frozenset(coords):
            coords.discard(coord)
            curr.append(coord)
            inner(coords, curr)
            curr.pop()
            coords.add(coord)

    coords = list(map(tuple, coords))
    inner(set(coords), [])
    return solution
