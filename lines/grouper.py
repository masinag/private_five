# -*- coding: iso-latin-1 -*-

""" """


import common
class Grouper:

    """_MIN_LEN è la lunghezza minima di un gruppo. È la tipica costante
    che dipende dalle regole del gioco; quindi fissa per il gioco,
    variabile per l'algoritmo. Per il momento non ha senso poterla
    configurare fuori dai sorgenti; dovesse servire ... è qui."""
    _MIN_LEN = 5

    """Grouper sa trovare i gruppi di una pietra, ossia le liste di
    pietre 'vicine' con lo stesso valore.  La classe ha un unico
    metodo pubblico (groups_for_pos_in_board). La board viene passata
    ogni volta per minimizzare lo stato mantenuto da Grouper; d'altra
    parte non viene fornita una funzione globale perché creare una
    istanza di Grouper è banale e una applicazione la usa molte
    volte."""

    def groups_for_pos_in_board(self, pos, board):
        "I gruppi di BOARD 'centrati' in POS"
        # nessun riferimento a board fuori da questo metodo
        self.size = board.get_size()
        self.value_at  = board.get_value
        v = board.get_value(pos)        #  this checks for valid pos

        return self._groups_at_pos_with_value(pos, v)   

    def _groups_at_pos_with_value(self, pos, value):
        """Lista dei gruppi 'centrati' in POS con valore VALUE"""
        ii  = [(1,0),(0,1),(1,1),(-1,1)]
        fun = self._line_from_pos_by_inc_with_value
        gg  = [fun(pos, i, value) for i in ii]
        gg  = [g for g in gg if len(g) >= self._MIN_LEN]
        return gg

    def _step_pos_by_inc(self, pos, inc):
        "La posizione che differisce di INC da POS"
        new = (pos[0]+inc[0], pos[1]+inc[1])
        if common.is_pos_in_size(new, self.size):
            return new
        else:
            return None

    def _line_from_pos_by_inc_with_value(self, pos, inc, value):
        "Le posizioni in contatto con POS nella direzione INC e con valore VALUE"
        pp = []
        p  = tuple(pos)
        while p and self.value_at(p) == value:
            if not p in pp: pp.append(p)
            p = self._step_pos_by_inc(p, inc)
        inc = (-inc[0], -inc[1])
        p  = tuple(pos)
        while p and self.value_at(p) == value:
            if not p in pp: pp.append(p)
            p = self._step_pos_by_inc(p, inc)
        return pp

