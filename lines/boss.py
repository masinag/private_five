# -*- coding: iso-latin-1 -*-
import game, common

class Boss:

    """Boss fornisce una interfaccia unica, di alto livello, verso le GUI.

    Alcune delle funzionalit� sono implementate da altre classi (es:
    Game, Board) e vengono delegate, altre sono implementate
    direttamente da Boss."""

    def __init__(self):
        self.new_empty_game()

    # command
    def new_empty_game(self, size = (9,9)):
        self._game  = game.Game(size)
        self._board = self._game.get_board()

    def move(self, fc, tc):
        self._game.move(fc, tc)

    def load_from_file(self, file):
        with open (file) as f:
            s=f.next()
        data, next_values, score=common.make_datas(s) # read the first line
        self._game.load_game(data, next_values, score)

    def save_to_file(self, file):
        data = self._game.get_raw_data()
        next_values= self._game.get_next_values()
        score=self._game.get_score()
        string=repr([data, next_values, score])
        with open(file, 'w') as f:
            f.write(string)

    # query
    def get_size(self):
        return self._game.get_size()

    def can_move(self, fc, tc):
        return self._game.can_move(fc, tc)

    def is_free(self, pos):
        return self._board.is_free(pos)

    def get_next_values(self):
        return self._game.get_next_values()

    def get_score(self):
        return self._game.get_score()

    def get_data(self):
        for rcv in self._board:
            yield rcv

    def get_raw_data(self):
        return self._board.get_raw_data()
