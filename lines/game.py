# -*- coding: iso-latin-1 -*-
import common
import board
import walker
import grouper

_NEXT_VALUES_COUNT = 3

class Game:

    def __init__(self, size = (9,9)):
        self.size = size

        self.board = board.Board(self.size)
        self.walker = walker.Walker()
        self.grouper = grouper.Grouper()

        self._score = 0
        self._update_next_values()
        self._add_random_stones()

        self._stone_added    = []
        self._groups_removed = []

    # commands
    def move(self, fc, tc):
        self._check_can_move(fc, tc)
        v = self.board.get_value(fc)
        self.board.set_value(fc, 0)
        if not self._fill_pos(tc, v):
            self._add_random_stones()

    def _add_random_stones(self):
        vv = self._take_next_values()
        cc = self.board.get_all_empty()[:len(vv)]
        # print "free:", cc
        if len(cc) == 0:
            raise common.LinesError, "Non ci sono celle libere!"

        # print "__add_random_stones: zip: %s", zip(cc,vv)
        ss = zip(cc,vv)
        self._stone_added = ss[:]
        self._groups_removed = []
        for c,v in zip(cc,vv):
            self._fill_pos(c,v)

    # comoda nel debugging!
    def debug_add_random_stones(self):
        self._add_random_stones()

    # queries
    def get_size(self):
        return self.size

    def can_move(self, fc, tc):
        try:
            self._check_can_move(fc, tc)
            return True
        except common.LinesError:
            return False

    def get_board(self):
        return self.board

    def get_next_values(self):
        return self._next_values

    def get_score(self):
        return self._score

    def get_paths(self, fc, tc):
        return self.walker.get_paths(self.board, fc, tc)

    def get_raw_data(self):
        return self.board.get_raw_data()

    def load_game(self, data, next_values, score):
        common.check_data(data)
        common.check_next_values(next_values)
        common.check_score(score)
        self.board.load_data(data)
        self._next_values=next_values
        self._score=score

    # private
    def _take_next_values(self):
        vv = self.get_next_values()
        self._update_next_values()
        return vv

    def _check_can_move(self, fc, tc):
        fe = te = pe = ""               # from, to, path errors
        if self.board.is_free(fc):
            fe = "la cella %s non contiene una pedina" % str(fc)
        if not self.board.is_free(tc):
            te = "la cella %s non � libera" % str(tc)
        if len(self.get_paths(fc, tc)) == 0:
            pe = "non esiste un percorso da %s a %s" % (str(fc), str(tc))
        if fe or te or pe:
            ee = ", ".join( (fe, te, pe) ) + '.'
            raise common.LinesError, ee

    def get_some_random_values(self, count):
        "COUNT interi positivi non nulli"
        return common.random_values(count, 0)

    def _fill_pos(self, pos, value):
        """Assegna il valore VALUE alla posizione POS e rimouve gli
        eventuali gruppi formatisi; aggiorna i punti"""
        self.board.set_value(pos, value)
        gg = self.grouper.groups_for_pos_in_board(pos, self.board)
        if not gg: return False

        for g in gg:
            for c in g:
                # print "__fill_pos group:", g
                self.board.set_value(c, 0)

        self._score += self._get_points_for_groups(gg)
        self._groups_removed.extend(gg)

        return True

    def _get_points_for_groups(self, gg):
        return sum(map(len, gg))

    def _update_next_values(self):
        self._next_values = common.random_values(_NEXT_VALUES_COUNT, 0)

#     def add_some_random(self, count = 3):
#         "Aggiunge COUNT pietre con valori random (non nulli)"
#         pp = self.board.get_all_empty()
#         if not pp:
#             raise common.LinesError, "Non ci sono celle libere"
#         pp = pp[:count]
#         print pp
#         vv = self.get_some_random_values(len(pp))
#         cc = zip(pp,vv)
#         for c,v in cc:
#             self._fill_pos(c,v)
#         return cc
