

def import_text_as_list(filename):

    with open(filename, mode='r') as file:
        datas = file.read()

    datas = datas.strip()
    return list(map(str.strip, datas.split(' ')))


if __name__ == '__main__':

    text = import_text_as_list('recherche_p1.txt')
    print(len(text))
    print(text)
