import util


def cut_on_line(text, line_length):

    result = ''
    total_spaces = 0
    text_iterator = iter(text)
    curr_line = next(text_iterator)
    for word in text_iterator:
        if len(word) + len(curr_line) + 1 <= line_length:
            curr_line += ' ' + word
        else:
            spaces_to_add = ' ' * (line_length - len(curr_line))
            total_spaces += len(spaces_to_add) ** 2
            result += curr_line + spaces_to_add + '\n'
            curr_line = word

    spaces_to_add = ' ' * (line_length - len(curr_line))
    total_spaces += len(spaces_to_add) ** 2
    result += curr_line + spaces_to_add
    return result, total_spaces


if __name__ == '__main__':

    text = util.import_text_as_list('recherche_p1.txt')
    # text = util.import_text_as_list('recherche_complet.txt')
    line_length = 80
    formated_text, spaces_count = cut_on_line(text, line_length)
    print(spaces_count)
    # print(formated_text)