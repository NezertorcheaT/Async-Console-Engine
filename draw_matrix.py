from colors import BaceColor
from config import configs


class DrawMatrix:
    def __init__(self):
        self.matrix = []
        d = " "
        for i in range(configs['HEIGHT']):
            self.matrix.append([])
            for j in range(configs['WIDTH']):
                self.matrix[i].append(d)

    def __getitem__(self, tup: tuple):
        return self.matrix[tup[0]][tup[1]]

    def __setitem__(self, key: tuple, value: str):
        self.matrix[key[0]][key[1]] = str(value)[0]

    @property
    def lenx(self):
        return len(self.matrix[0])

    @property
    def leny(self):
        return len(self.matrix)

    def __str__(self):
        s = ''
        for x in range(self.leny):
            for y in range(self.lenx):
                s += self[x, y] + BaceColor("Reset")()
            s += '\n'
        return s

    @property
    def isEmpty(self):
        for x in range(self.leny):
            for y in range(self.lenx):
                if self[x, y] not in ('', ' '):
                    return False
        return True
