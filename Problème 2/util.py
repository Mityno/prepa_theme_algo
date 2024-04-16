

def import_words_from_text(filename):

    with open(filename, mode='r') as file:
        datas = file.read()

    datas = datas.strip()
    return list(map(str.strip, datas.split(' ')))


def get_score(spaces_counter):
    return sum(count ** 2 for count in spaces_counter)


def get_line_score(line, line_length):
    spaces_count = line_length - len(line.rstrip())
    return spaces_count ** 2


def get_text_score(text, line_length):
    score = 0
    for line in text.split('\n'):
        score += get_line_score(line, line_length)
    return score


if __name__ == '__main__':

    line_length = 80

    # text = import_words_from_text('recherche_p1.txt')
    # print(len(text))
    # print(text)

    with open('solution_complet.txt', mode='r') as file:
        text = file.read()
    print(get_text_score(text, line_length))
