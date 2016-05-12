# -*- coding: iso-latin-1 -*-
import random
import common

def make_data(size):
    "Una lista di liste di None con dimensioni SIZE (coppia di interi)"
    return [[None for c in range(size[1])] for r in range(size[0])]

def iterate_raw_data(data):
    "Itera una lista di liste fornendo la tripla (riga, colonna, valore)"
    for r, row in enumerate(data):
        for c, v in enumerate(row):
            yield r,c,v

# def load_integers_into_data(data, size = None):
#     rows = load_integers(size)
#     for r,c,v in iterate_raw_data(rows):
#         data.set_value((r,c),v)

def get_data_size(data):
    "Le dimensioni (righe, colonne) di una lista di liste"
    return len(data), len(data[0])

class Board:

    def __init__(self, size):
        self.data = make_data(size)
        for r,c,v in self:
            self.set_value((r,c), 0)

    def __iter__(self):
        for r, row in enumerate(self.data):
            for c, v in enumerate(row):
                yield r,c,v

    def get_value(self, pos):
        "Il valore alla posizione POS"
        self.check_pos(pos)
        r,c = pos
        return self.data[r][c]

    def set_value(self, pos, v):
        "Assegna il valore V alla posizione POS"
        self.check_pos(pos)
        r,c = pos
        self.data[r][c] = v

    def get_size(self):
        "La dimensione (righe, colonne) dei dati"
        return get_data_size(self.data)

    def get_raw_data(self):
        "I dati come lista di liste di interi"
        return self.data

    def load_data(self, values):
        for r,c,v in iterate_raw_data(values):
            self.set_value((r,c),v)

    def is_free(self, pos):
        "True se il valore in POS � zero"
        self.check_pos(pos)
        return self.get_value(pos) == 0

    def check_pos(self, pos):
        "Solleva una eccesione se POS � fuori dai limiti di board.get_size()"
        common.check_pos_in_size(pos, self.get_size())

    def get_all_empty(self):
        "Tutte le posizioni libere"
        pp = [(r,c) for r,c,v in self if self.is_free( (r,c) )]
        random.shuffle(pp)
        return pp


if __name__ == "__main__":

    pass
