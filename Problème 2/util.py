import collections


def import_words_from_text(filename):

    with open(filename, mode='r') as file:
        datas = file.read()

    datas = datas.strip()
    # returns a list of all words from the text (in apparition order)
    return list(map(str.strip, datas.split(' ')))


def get_score(spaces_counter):
    # returns the score for a list of spaces at the end of each line
    return sum(count ** 2 for count in spaces_counter)


def get_line_score(line, line_length):
    # return the score for a line (string) depending on the giben line_length
    spaces_count = line_length - len(line.rstrip())
    return spaces_count ** 2


def get_text_score(text, line_length):
    # returns the score of a whole text
    score = 0
    for line in text.split('\n'):
        score += get_line_score(line, line_length)
    return score


def find_longest_seq(words, line_length):

    """
    Search the longest possible sequence of following words within the given
    line length
    This serves as a upper bound for the time complexity of both algorithms
    """

    max_buffer_len = 0

    buffer = collections.deque([])
    curr_len = 0
    for i in range(len(words)):
        if buffer:  # delete the previous tried first word
            last_i = buffer.popleft()
            curr_len -= len(words[last_i]) + 1

        else:  # if buffer was empty, add a first word
            buffer.append(i)
            curr_len += len(words[i])

        # add as many words as possible at the end of the buffer while not
        # overflowing the line length
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

    # text = import_words_from_text('recherche_complet.txt')
    # print(len(text))

    # print(find_longest_seq(text, line_length))
