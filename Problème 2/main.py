import iterative_algorithm
import recursive_algorithm
import util
import time
import sys

# This code contains a basic comparison of performance between the recursive
# and iterative algorithm
# Implementation and further testing are available in the other python files

words = util.import_words_from_text('recherche_p1.txt')

# words = util.import_words_from_text('recherche_complet.txt')
# tweak the upper bound depending on the wanted time of execution
# words = words[:50_000]

line_length = 80

# necessary for the recursive algorithm to run
sys.setrecursionlimit(len(words) * 2)

for func in (recursive_algorithm.least_squares, iterative_algorithm.iterative_search):

    bef = time.perf_counter()
    result = func(words, line_length)
    aft = time.perf_counter()

    print(f'{func.__module__} : {func.__name__} took {aft - bef:.2e}s')
    print(flush=True)
