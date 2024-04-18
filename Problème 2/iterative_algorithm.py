import util
import collections
import time
import numpy as np
import json


def iterative_search(words, line_length):

    n = len(words)
    # use the length of the longest sequence possible for the given line_length
    # to reduce the memory usage of the scores matrix, won't need more space
    # since a line cannot have more words than that value
    max_height = util.find_longest_seq(words, line_length)
    scores = np.full((n, max_height), float('inf'))

    # start at the end, calculate base case
    i = n - 1
    # curr_state is of the form
    # [line first word index, number of word on the line after the first one]
    curr_state = [i, 0]
    curr_len = len(words[i])
    scores[*curr_state] = (line_length - curr_len)**2
    for j in range(i - 1, -1, -1):
        # consider adding word j to the line
        curr_len += 1 + len(words[j])
        if curr_len > line_length:
            # if it cannot be added, stop the current loop
            break

        # replace the first word of the line
        curr_state[0] = j
        curr_state[1] += 1  # added a word to the line
        scores[*curr_state] = (line_length - curr_len)**2

    # start using the recursion relation
    for i in range(n - 2, -1, -1):
        # initialise the position in the text
        curr_state = [i, 0]
        curr_len = len(words[i])
        curr_key = tuple(curr_state)

        curr_state[1] += 1  # consider adding word i + 1 to the line
        scores[*curr_key] = min(
            scores[*curr_state],  # add case
            (line_length - curr_len)**2 + scores[i + 1, 0]  # newline case
        )
        curr_state[1] -= 1  # remove extra word

        # start adding words at the beginning of the line
        for j in range(i - 1, -1, -1):
            # consider adding word j to the beginning of the line
            curr_len += 1 + len(words[j])
            if curr_len > line_length:
                break

            curr_state[0] = j
            curr_state[1] = i - j
            # this keeps track of which combination we are looking
            # the score for
            curr_key = tuple(curr_state)

            curr_state[1] += 1  # consider adding word i + 1 to the line
            # case where adding word i + 1 overflows the line
            if curr_len + len(words[i + 1]) + 1 > line_length:
                # no other choice than making a newline
                scores[*curr_key] = (
                    (line_length - curr_len)**2
                    + scores[i + 1, 0]
                )
            else:  # else compare adding and making a new line
                scores[*curr_key] = min(
                    scores[*curr_state],  # add case
                    (line_length - curr_len)**2 + scores[i + 1, 0]  # newline case
                )
            curr_state[1] -= 1  # remove extra word

    # reconstructing the formated text according to the scores
    i = 0
    curr_state = [i, 0]
    # output_lines : a list of string representing each line
    output_lines = [words[i]]
    while i < n - 1:

        # suppose we add the next word, check the operation won't overflow
        # the current line, in which case make a new line
        if len(output_lines[-1]) + len(words[i + 1]) + 1 > line_length:
            curr_state = [i + 1, 0]  # state for a new line
            output_lines.append(words[i + 1])
            i += 1
            continue

        curr_state[1] += 1  # consider adding word i + 1 to the line
        add_score = scores[*curr_state]
        curr_state[1] -= 1  # remove extra word
        newline_score = (
            util.get_line_score(output_lines[-1], line_length)  # current line score
            + scores[i + 1, 0]  # next line score
        )

        # to minise the score, we choose the operation that has minimal score
        if add_score < newline_score:
            output_lines[-1] += ' ' + words[i + 1]
            curr_state[1] += 1  # word has been added to the line
        else:
            output_lines.append(words[i + 1])
            curr_state = [i + 1, 0]  # state for a new line

        i += 1

    # returns the formated text and the text score
    return '\n'.join(
            f'{line:{line_length}}' for line in output_lines
        ), scores[0, 0]


if __name__ == '__main__':

    # words = util.import_words_from_text('exemple_simple.txt')
    # words = util.import_words_from_text('recherche_p1.txt')
    words = util.import_words_from_text(r'recherche_p1.txt')

    line_length = 80

    bef = time.perf_counter_ns()
    result_text, score = iterative_search(words, line_length)
    aft = time.perf_counter_ns()
    print(f'Iterative search took : {(aft - bef)*1e-9:.2e}s, {line_length = }', flush=True)

    print(score)
    # print(util.get_text_score(result_text, line_length))

    # Pour stocker le résultat dans un fichier texte
    # with open('solution_complet.txt', mode='w') as file:
    #     file.write(result_text)
