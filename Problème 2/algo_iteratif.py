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
        curr_len += 1 + len(words[j])
        if curr_len > line_length:
            break
        curr_state.appendleft(j)
        scores[tuple(curr_state)] = (line_length - curr_len)**2

    for i in range(n - 2, -1, -1):
        curr_state = collections.deque([i])
        curr_len = len(words[i])
        curr_key = tuple(curr_state)
        curr_state.append(i + 1)
        scores[curr_key] = min(
            scores[tuple(curr_state)], (line_length - curr_len)**2 + scores[(i + 1,)]
        )
        curr_state.pop()

        for j in range(i - 1, -1, -1):
            curr_len += 1 + len(words[j])
            if curr_len > line_length:
                break
            curr_state.appendleft(j)
            curr_key = tuple(curr_state)
            curr_state.append(i + 1)
            if curr_len + len(words[i + 1]) + 1 > line_length:
                scores[curr_key] = (line_length - curr_len)**2 + scores[(i + 1,)]
            else:
                scores[curr_key] = min(
                    scores[tuple(curr_state)], (line_length - curr_len)**2 + scores[(i + 1,)]
                )
            curr_state.pop()

    return scores[(0,)]

if __name__ == '__main__':

    # words = util.import_text_as_list('recherche_p1.txt')
    words = util.import_text_as_list('recherche_complet.txt')
    line_length = 80
    print(iterative_search(words, line_length))
