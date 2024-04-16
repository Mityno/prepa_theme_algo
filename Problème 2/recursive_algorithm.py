import numpy as np
import util


def aux(end_space, index, word_list, L, mem_dict):
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
        mem_dict[(end_space, index)] = (end_space+1)**2 + aux(L - len(m), index+1, word_list, L, mem_dict)
        return mem_dict[(end_space, index)]
    

    current_line = aux(end_space - len(m), index+1, word_list, L, mem_dict)
    new_line = (end_space+1)**2 + aux(L - len(m), index+1, word_list, L, mem_dict)
    mem_dict[(end_space, index)] = min(current_line, new_line)
    return mem_dict[(end_space, index)]


def least_squares(word_list, L):
    mem_dict = {}
    least_error = aux(L, 0, word_list, L, mem_dict)
    return least_error


if __name__ =='__main__':
    word_list = util.import_text_as_list('./Problème 2/recherche_p1.txt')
    # print(word_list)
    print(least_squares(word_list, 80))

    
