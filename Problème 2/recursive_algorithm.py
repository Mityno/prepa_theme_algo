import numpy as np
import util
import sys
import time


def least_squares(word_list, L):
    mem_dict = {}
    line_break_dict = {}

    def aux(end_space, index):
        # Mémoisation :
        if (end_space, index) in mem_dict:
            return mem_dict[(end_space, index)]

        # Cas de base :
        if index == len(word_list):
            mem_dict[(end_space, index)] = (end_space+1)**2
            return mem_dict[(end_space, index)]
        
        # Cas général :
        m = word_list[index] + ' '

        if len(m) - 1 > end_space:
            mem_dict[(end_space, index)] = (end_space+1)**2 + aux(L - len(m), index+1)
            line_break_dict[(end_space, index)] = True
            return mem_dict[(end_space, index)]
        

        current_line = aux(end_space - len(m), index+1)
        new_line = (end_space+1)**2 + aux(L - len(m), index+1)
        if current_line <= new_line:
            mem_dict[(end_space, index)] = current_line
            line_break_dict[(end_space, index)] = False
        else:
            mem_dict[(end_space, index)] = new_line
            line_break_dict[(end_space, index)] = True
        return mem_dict[(end_space, index)]
    

    least_error = aux(L, 0)
    line_list = [[]]
    end_space = L
    for index, word in enumerate(word_list):
        if line_break_dict[(end_space, index)]:
            line_list.append([])
            end_space = L - len(word) - 1
        else:
            end_space -= len(word) + 1
        line_list[-1].append(word)

    line_list = [' '.join(line) for line in line_list]
    result_text = '\n'.join(line_list)
    return least_error, result_text


if __name__ =='__main__':
    word_list = util.import_text_as_list('./Problème 2/recherche_complet.txt')
    # print(len(word_list))
    sys.setrecursionlimit(len(word_list)*10)
    deb = time.perf_counter()
    least_error, result_text = least_squares(word_list, 80)
    print(least_error)
    fin = time.perf_counter()
    print(f'{least_squares.__name__} took {fin - deb:.3f}s to run')

    # with open('./Problème 2/solution_complet.txt', mode='w') as file:
    #     file.write(result_text)
    


    
