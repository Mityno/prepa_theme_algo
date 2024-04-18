import collections


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


def find_longest_seq(words, line_length):

    max_buffer_len = 0

    buffer = collections.deque([])
    curr_len = 0
    for i in range(len(words)):
        if buffer:
            last_i = buffer.popleft()
            curr_len -= len(words[last_i]) + 1

        else:
            buffer.append(i)
            curr_len += len(words[i])

        for j in range(i, len(words)):
            if curr_len + len(words[j]) + 1 > line_length:
                break

            buffer.append(j)
            curr_len += len(words[j]) + 1

            if len(buffer) > max_buffer_len:
                max_buffer_len = len(buffer)

    return max_buffer_len

if __name__ == '__main__':

    line_length = 80

    # text = import_words_from_text('recherche_p1.txt')
    # print(len(text))
    # print(text)

    # print(find_longest_seq(text, line_length))

    # with open('solution_p1.txt', mode='r') as file:
    #     text = file.read()
    # print(get_text_score(text, line_length))
