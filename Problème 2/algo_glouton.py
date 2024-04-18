import util


def cut_on_line(text, line_length):

    result = ''
    spaces_counter = []
    text_iterator = iter(text)
    curr_line = next(text_iterator)
    for word in text_iterator:
        if len(word) + len(curr_line) + 1 <= line_length:
            curr_line += ' ' + word
        else:
            spaces_to_add = ' ' * (line_length - len(curr_line))
            spaces_counter.append(len(spaces_to_add))
            result += curr_line + spaces_to_add + '\n'
            curr_line = word

    spaces_to_add = ' ' * (line_length - len(curr_line))
    spaces_counter.append(len(spaces_to_add))
    result += curr_line + spaces_to_add
    return result, spaces_counter


def search_best_line_length(text, max_line_length):
    min_line_length = max(map(len, text))
    best_score = float('inf')
    best_line_length = None
    for line_length in range(min_line_length, max_line_length + 1):
        print(line_length, 'in test', flush=True)
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
    # text = util.import_words_from_text('recherche_p1.txt')  # max=80 => best=80 -> score=2515
    text = util.import_words_from_text('recherche_complet.txt')  # max=80 => best=80 -> score=1652570
    line_length = 80
    formated_text, spaces_counter = cut_on_line(text, line_length)
    print(util.get_score(spaces_counter))
    # print('\n'.join(formated_text.split('\n')[2:5]))
    # line_length, score = search_best_line_length(text, line_length)

    # for line_length in (79, 80):
    # for line_length in (20,):
    #     print(line_length)
    #     output_text, spaces_counter = cut_on_line(text, line_length)
    #     print(util.get_score(spaces_counter))
    #     # print(len(output_text.split('\n')))
    #     print(output_text)
        # print()
    # print(line_length)
    # print(score)
    # print(util.get_score(spaces_counter))
    # print(formated_text)
