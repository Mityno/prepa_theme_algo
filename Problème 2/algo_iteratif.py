import util
import collections


def iterative_search(words, line_length):

    scores = {}
    n = len(words)

    i = n - 1
    curr_state = collections.deque([i])
    curr_len = len(words[i])
    scores[tuple(curr_state)] = (line_length - curr_len)**2
    for j in range(i - 1, -1, -1):
        # consider adding word j to the line
        curr_len += 1 + len(words[j])
        if curr_len > line_length:
            break

        curr_state.appendleft(j)
        scores[tuple(curr_state)] = (line_length - curr_len)**2

    for i in range(n - 2, -1, -1):
        curr_state = collections.deque([i])
        curr_len = len(words[i])
        curr_key = tuple(curr_state)

        curr_state.append(i + 1)  # consider adding word i + 1 to the line
        scores[curr_key] = min(
            scores[tuple(curr_state)],  # add case
            (line_length - curr_len)**2 + scores[(i + 1,)]  # newline case
        )
        curr_state.pop()  # remove extra word

        for j in range(i - 1, -1, -1):
            # consider adding word j to the line
            curr_len += 1 + len(words[j])
            if curr_len > line_length:
                break

            curr_state.appendleft(j)
            # this keeps track of which combination we are looking
            # the score for
            curr_key = tuple(curr_state)

            # consider adding word i + 1 to the line
            curr_state.append(i + 1)
            # case where adding word i + 1 overflows the line
            if curr_len + len(words[i + 1]) + 1 > line_length:
                scores[curr_key] = (line_length - curr_len)**2 + scores[(i + 1,)]
            else:  # else compare adding and making a new line
                scores[curr_key] = min(
                    scores[tuple(curr_state)],  # add case
                    (line_length - curr_len)**2 + scores[(i + 1,)]  # newline case
                )
            curr_state.pop()  # remove extra word

    i = 0
    curr_state = collections.deque([i])
    output_lines = [words[i]]
    while i < n - 1:

        # suppose we add the next word, check the operation won't overflow the
        # current line, in which case make a new line
        if len(output_lines[-1]) + len(words[i + 1]) + 1 > line_length:
            curr_state = collections.deque([i + 1])
            output_lines.append(words[i + 1])
            i += 1
            continue

        curr_state.append(i + 1)  # consider adding word i + 1 to the line
        add_score = scores[tuple(curr_state)]
        curr_state.pop()  # remove extra word
        newline_score = scores[(i + 1,)] + scores[tuple(curr_state)]

        # to minise the score, we apply the operation that has minimal score
        if add_score < newline_score:
            output_lines[-1] += ' ' + words[i + 1]
            curr_state.append(i + 1)
        else:
            output_lines.append(words[i + 1])
            curr_state = collections.deque([i + 1])

        i += 1

    return '\n'.join(
            f'{line:{line_length}}' for line in output_lines
        ), scores[(0,)]


if __name__ == '__main__':

    # words = util.import_text_as_list('exemple_simple.txt')
    words = util.import_text_as_list('recherche_p1.txt')
    # words = util.import_text_as_list('recherche_complet.txt')
    line_length = 80
    result_text, score = iterative_search(words, line_length)
    print(score)
    # with open('solution_complet.txt', mode='w') as file:
    #     file.write(result_text)
