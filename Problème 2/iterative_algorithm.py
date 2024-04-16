import util
import collections
import time


def iterative_search(words, line_length):

    scores = {}
    n = len(words)

    i = n - 1
    # curr_state is of the form [line_first_word_index, line_last_word_index]
    curr_state = [i] * 2
    curr_len = len(words[i])
    scores[tuple(curr_state)] = (line_length - curr_len)**2
    for j in range(i - 1, -1, -1):
        # consider adding word j to the line
        curr_len += 1 + len(words[j])
        if curr_len > line_length:
            break

        curr_state[0] = j
        scores[tuple(curr_state)] = (line_length - curr_len)**2

    for i in range(n - 2, -1, -1):
        curr_state = [i] * 2
        curr_len = len(words[i])
        curr_key = tuple(curr_state)

        temp_end = curr_state[1]
        curr_state[1] = i + 1  # consider adding word i + 1 to the line
        scores[curr_key] = min(
            scores[tuple(curr_state)],  # add case
            (line_length - curr_len)**2 + scores[(i + 1,) * 2]  # newline case
        )
        curr_state[1] = temp_end  # remove extra word

        for j in range(i - 1, -1, -1):
            # consider adding word j to the line
            curr_len += 1 + len(words[j])
            if curr_len > line_length:
                break

            curr_state[0] = j
            # this keeps track of which combination we are looking
            # the score for
            curr_key = tuple(curr_state)

            # consider adding word i + 1 to the line
            temp_end = curr_state[1]
            curr_state[1] = i + 1  # consider adding word i + 1 to the line
            # case where adding word i + 1 overflows the line
            if curr_len + len(words[i + 1]) + 1 > line_length:
                scores[curr_key] = (line_length - curr_len)**2 + scores[(i + 1,) * 2]
            else:  # else compare adding and making a new line
                scores[curr_key] = min(
                    scores[tuple(curr_state)],  # add case
                    (line_length - curr_len)**2 + scores[(i + 1,) * 2]  # newline case
                )
            curr_state[1] = temp_end  # remove extra word

    i = 0
    curr_state = [i] * 2
    output_lines = [words[i]]
    while i < n - 1:

        # suppose we add the previous word, check the operation won't overflow the
        # current line, in which case make a new line
        if len(output_lines[-1]) + len(words[i + 1]) + 1 > line_length:
            curr_state = [i + 1] * 2
            output_lines.append(words[i + 1])
            i += 1
            continue

        temp_end = curr_state[1]
        curr_state[1] = i + 1  # consider adding word i + 1 to the line
        add_score = scores[tuple(curr_state)]
        curr_state[1] = temp_end  # remove extra word
        newline_score = (
            util.get_line_score(output_lines[-1], line_length)  # current line score
            + scores[(i + 1,) * 2]  # next line score
        )

        # to minise the score, we apply the operation that has minimal score
        if add_score < newline_score:
            output_lines[-1] += ' ' + words[i + 1]
            curr_state[1] = i + 1
        else:
            output_lines.append(words[i + 1])
            curr_state = [i + 1] * 2

        i += 1

    return '\n'.join(
            f'{line:{line_length}}' for line in output_lines
        ), scores[(0,) * 2]


if __name__ == '__main__':
    line_length = 80

    # words = util.import_words_from_text('exemple_simple.txt')
    # words = util.import_words_from_text('recherche_p1.txt')
    words = util.import_words_from_text('recherche_complet.txt')

    bef = time.perf_counter()
    result_text, score = iterative_search(words, line_length)
    aft = time.perf_counter()
    print(f'Iterative search took : {aft - bef:.2e}s')

    print(score)
    print(util.get_text_score(result_text, line_length))

    # with open('solution_complet.txt', mode='w') as file:
    #     file.write(result_text)
