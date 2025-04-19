class Map:
    def __init__(self):
        self.level = []

    def load_level(self, filename):
        # читаем уровень, убирая символы перевода строки
        with open(filename, 'r') as mapFile:
            self.level = list(map(lambda line: line.strip(), mapFile))

        # и подсчитываем максимальную длину
        max_width = max(map(len, self.level))

        # дополняем каждую строку пустыми клетками ('.')
        return list(map(lambda x: x.ljust(max_width, ' '), self.level))