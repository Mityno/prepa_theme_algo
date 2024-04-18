import iterative_algorithm
import recursive_algorithm
import util
import time
import sys

words = util.import_words_from_text('recherche_p1.txt')
line_length = 80

sys.setrecursionlimit(len(words) * 2)

for func in (recursive_algorithm.least_squares, iterative_algorithm.iterative_search):
    bef = time.perf_counter()
    result = func(words, line_length)
    aft = time.perf_counter()
    print(f'{func.__name__} took {aft - bef:.2e}s')

    if isinstance(result, int):
        print(result)
    elif isinstance(result, tuple):
        print(result[1])
    print(flush=True)
