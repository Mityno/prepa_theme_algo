import numpy as np
import util
import sys
import time
import json


def least_squares(word_list: list[str], L: int) -> tuple[int, str]:
    mem_dict: dict[tuple[int, int], int] = {}
    line_break_dict: dict[tuple[int, int], bool] = {}

    # Définition de la fonction auxiliaire récursive, pour qui les paramètres de la fonction principale sont des variables globales
    def aux(end_space: int, index: int) -> int:
        # Mémoisation :
        if (end_space, index) in mem_dict:
            return mem_dict[(end_space, index)]

        # Cas de base :
        if index == len(word_list):
            mem_dict[(end_space, index)] = (end_space+1)**2
            return mem_dict[(end_space, index)]
        
        # Cas général :
        # NB : les "+1" dans le calcul des scores de fin de ligne servent à compenser l'ajout des espaces en fin de mot 
        # (le dernier espace de la ligne étant dans un mot, il est soustrait à end_space mais doit être compté)
        m = word_list[index] + ' '
        
        # Force un retour à la ligne si l'espace en fin de ligne n'est pas suffisant
        if len(m) - 1 > end_space:
            mem_dict[(end_space, index)] = (end_space+1)**2 + aux(L - len(m), index+1)
            line_break_dict[(end_space, index)] = True
            return mem_dict[(end_space, index)]
        
        # Si end_space le permet, compare le score obtenu en effectuant un retour à la ligne et celui
        # obtenu sans retour, et conserve le meilleur cas des deux, en notant si un retour à la ligne
        # a été effectué ou non
        current_line = aux(end_space - len(m), index+1)
        new_line = (end_space+1)**2 + aux(L - len(m), index+1)
        if current_line <= new_line:
            mem_dict[(end_space, index)] = current_line
            line_break_dict[(end_space, index)] = False
        else:
            mem_dict[(end_space, index)] = new_line
            line_break_dict[(end_space, index)] = True
        return mem_dict[(end_space, index)]
    

    least_error: int = aux(L, 0)

    # Reconstitution de la mise en page offrant un score optimal
    line_list: list[list[str]] = [[]]
    end_space: int = L
    for index, word in enumerate(word_list):
        # Change de ligne en cas de retour, et met à jour la valeur de endspace pour s'assurer de 
        # parcourir les bonnes branches de l'arbre de récursivité
        if line_break_dict[(end_space, index)]:
            line_list.append([])
            end_space = L - len(word) - 1
        else:
            end_space -= len(word) + 1
        line_list[-1].append(word)

    # Converti la liste de ligne d'une liste de listes en une liste de chaînes de caractères,
    # complète les lignes avec des espaces, puis transforme cette liste en une seule chaîne
    # paginée, le texte mis en page final
    line_list: list[str] = [' '.join(line) for line in line_list]
    line_list = [f'{line:{L}}' for line in line_list]
    result_text: str = '\n'.join(line_list)
    return least_error, result_text


if __name__ =='__main__':
    # word_list = util.import_words_from_text('recherche_complet.txt')
    # # print(len(word_list))
    # deb = time.perf_counter_ns()
    # least_error, result_text = least_squares(word_list, 80)
    # fin = time.perf_counter_ns()
    # print(least_error)
    # print(f'{least_squares.__name__} took {(fin - deb)*1e-9:.3e}s to run')

    # with open('./Problème 2/solution_complet.txt', mode='w') as file:
    #     file.write(result_text)
    
    n = 50_000

    words = util.import_words_from_text(r'recherche_complet.txt')
    words = words[:n]
    sys.setrecursionlimit(len(words) * 10)

    min_line_length = max(map(len, words))
    print(min_line_length, max(words, key=len))
    line_lengths = np.linspace(min_line_length, 250, 80, dtype=int)
    times = []

    for line_length in line_lengths:

        bef = time.perf_counter_ns()
        result_text, score = least_squares(words, line_length)
        aft = time.perf_counter_ns()
        times.append((aft - bef) * 1e-9)
        print(f'Iterative search took : {(aft - bef)*1e-9:.2e}s, {line_length = }', flush=True)

    line_lengths = list(map(int, line_lengths))

    with open('time_testing.txt', mode='a') as file:
        json.dump([line_lengths, times], file)
        file.write('\n')
