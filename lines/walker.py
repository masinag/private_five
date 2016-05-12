# -*- coding: iso-latin-1 -*-

# __get_cross è abbastanza generica da essere una funzione e non un
# metodo, ma sta qui perché non è usato in nessun altro posto.

def get_cross(pos, size):
    "Le quattro posizioni (o None) sinistra, destra, sopra, sotto a POS"
    r, c = size
    tr = r - 1                      # top row
    tc = c - 1                      # top col
    r,c = pos
    return [ c >  0 and (r,   c-1) or None, # sinistra
             c < tc and (r,   c+1) or None, # destra
             r >  0 and (r-1, c  ) or None, # sopra
             r < tr and (r+1, c  ) or None] # sotto

class Walker:
    """Trova i cammmini liberi tra due posizioni di una Board
    Walker sa trovare i percorsi liberi da una posizione a un'altra.
    Walker ha un unico metodo pubblico (get_paths).
    Un client di solito avrà un walker e una board e ad ogni richiesta
    di percorso libero chiamerà:
       walker.get_paths(board, from_pos, to_pos). """

    # naming:
    # p are path(s)
    # c are cell(s), i.e. pos, i.e. pair(s) of integers

    def get_paths(self, board, fc, tc):
        "Cammmini liberi tra le posizioni FC e TC di BOARD"
        if fc == tc:
            return []

        # nessun riferimento a board fuori di qui
        self.is_free = board.is_free
        self.size    = board.get_size()
        
        self.visited = [fc]
        self.paths = [[tuple(fc)]]
        while self._step():
            for p in self.paths:
                if p[-1] == tuple(tc):
                    return [p]
        return []
    
    def _step(self):
        "Estende tutti i path con le celle 'friends'"
        found = False
        pp = []
        for p in self.paths:
            cc = self._get_friends(p[-1])
            
            self.visited.extend(cc)
            if cc: found = True
            # if not cc: self.paths.remove(p)
            for c in cc:
                n = p[:]
                n.append(c)
                pp.append(n)
                #print map(str,n)
        self.paths = pp
        return found
    
    def _get_friends(self, fc):
        "Celle vicine a fc, libere e non ancora visitate"
        cc = get_cross(fc, self.size)
        return [c for c in cc
                if c and self.is_free(c) \
                and (c not in self.visited)]
