import random
import time
import numpy as np
from matplotlib import pyplot as plt
import json


def time_func(func):

    def inner(*args, **kwargs):
        bef = time.perf_counter()
        result = func(*args, **kwargs)
        aft = time.perf_counter()
        print(f'{func.__name__} took {aft - bef:.1e}s')
        return result

    return inner


# def get_nth_item_deco(n):
#     def inner(seq):
#         return seq[n]
#     return inner
# get_first = get_nth_item_deco(0)


#@time_func
def bruteforce(lst, start_point=None):
    curr = []
    last_end_point = float('-inf')
    lst = sorted(lst)

    def inner(last_end_point, curr):
        sub_solutions = []
        for (start, end) in lst:
            if start >= last_end_point:
                curr.append((start, end))
                sub_solutions.extend(inner(end, curr))
                curr.pop()

        solutions = sub_solutions[:]
        solutions.append(curr[:])
        return solutions

    return max(inner(last_end_point, curr), key=len)


#@time_func
def solve_efficient(lst):
    n = len(lst)
    lst = lst[:]
    lst.sort(key=lambda x: x[::-1])

    solution = []
    last_end = float('-inf')
    for start, end in lst:
        if start >= last_end:
            solution.append((start, end))
            last_end = end
    return solution



# lst = [(2, 5), (3, 9), (7, 10), (8, 9), (10, 11), (9, 10), (12, 13)]
# lst = [(2, 5), (3, 9), (7, 10)]

# nb_tries = 100
# for _ in range(nb_tries):
#     n = 8
#     lower_bound, higher_bound = 0, 10
#     lst = []
#     for _ in range(n):
#         start = random.randrange(lower_bound, higher_bound - 1)
#         end = random.randrange(start + 1, higher_bound)
#         lst.append((start, end))

#     print(_)
#     try:
#         assert (len(solve_more_efficient(lst)) == len(solve_efficient(lst)))
#     except AssertionError:
#         print(lst)
#         exit()
#     # result = solve_more_efficient(lst)
#     # print('-' * 50)
#     # print(result)
#     # print(solve_efficient(lst))
#     # print('-' * 50)

lower_bound, higher_bound = 0, 60
times = []
ns = list(map(int, np.linspace(20, 100_000, 10_000, dtype=int)))
# ns = list(map(int, np.linspace(20, 100, 10, dtype=int)))

lst = []
for _ in range(max(ns)):
    start = random.randrange(lower_bound, higher_bound - 1)
    end = random.randrange(start + 1, higher_bound)
    lst.append((start, end))
print('Started', flush=True)

lst_times = 0
for n in ns:
    bef = time.perf_counter()
    temp_lst = lst[:n]
    aft = time.perf_counter()
    lst_times += aft - bef

    bef = time.perf_counter_ns()
    solve_efficient(temp_lst)
    aft = time.perf_counter_ns()

    times.append((aft - bef) * 1e-9)

with open('results.json', mode='w', encoding='utf-8') as file:
    json.dump([ns, times], file)

print('solve time :', sum(times))
print('list manipulation time :', lst_times, flush=True)

plt.plot(ns, np.array(times) / ns)
# plt.plot(ns, ns * 5e-7)
plt.show()
