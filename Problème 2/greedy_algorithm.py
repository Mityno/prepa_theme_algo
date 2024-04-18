import util
import time


def cut_on_line(words, line_length):

    result = ''
    score = 0
    words_iterator = iter(words)
    # start the first line with the first word
    curr_line = next(words_iterator)
    spaces_counter = []

    for word in words_iterator:

        # if adding the next word doesn't overflows the line
        if len(word) + len(curr_line) + 1 <= line_length:
            curr_line += ' ' + word

        else:  # if it overflows, fill the line with spaces and make a new line
            spaces_to_add = ' ' * (line_length - len(curr_line))
            spaces_counter.append(len(spaces_to_add))

            # fill the line and make a new one
            result += curr_line + spaces_to_add + '\n'
            curr_line = word

    # add final spaces
    spaces_to_add = ' ' * (line_length - len(curr_line))
    spaces_counter.append(len(spaces_to_add))
    result += curr_line + spaces_to_add
    return result, spaces_counter


def search_best_line_length(text, max_line_length):

    """
    Find the line length that minimises the text score with the greedy
    algorithm
    """

    min_line_length = max(map(len, text))

    best_score = float('inf')
    best_line_length = None

    # test each line length possible up to the maximal line length
    # and keep the one that has the minimal score
    for line_length in range(min_line_length, max_line_length + 1):

        output_text, spaces_counter = cut_on_line(text, line_length)
        text_lines_count = len(output_text.split('\n'))
        line_end_spaces = (max_line_length - line_length) * text_lines_count

        for i in range(len(spaces_counter)):
            spaces_counter[i] += line_end_spaces

        score = util.get_score(spaces_counter)

        if score < best_score:
            best_score = score
            best_line_length = line_length

    return best_line_length, best_score


if __name__ == '__main__':

    # text = util.import_words_from_text('exemple_simple.txt')
    text = util.import_words_from_text('recherche_p1.txt')
    # text = util.import_words_from_text('recherche_complet.txt')

    line_length = 80

    bef = time.perf_counter_ns()
    formated_text, score = cut_on_line(text, line_length)
    aft = time.perf_counter_ns()

    print(f'Greeedy took : {(aft - bef) * 1e-9:3e}s')
    print(util.get_score(score))

    # line_length, score = search_best_line_length(text, line_length)
    # print(line_length, score)
