import util


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


if __name__ == '__main__':
    pass