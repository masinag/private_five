#!/usr/bin/env python
# -*- coding: iso-latin-1 -*-
# Copyright: Luca Manini (2005)

import os
import cmd
import common

def ints_to_row(ii):
    return ' '.join([i <> 0 and str(i) or "_" for i in ii])

class BaseCli(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '> '

    def do_quit(self, arg):
        print "\nbye bye"
        return 1

    def do_EOF(self, arg):
        self.do_quit(None)
        return 1

    def emptyline(self):
        pass

    def run(self):
        self.cmdloop()

class Cli(BaseCli):

    def __init__(self, boss):
        BaseCli.__init__(self)
        self.boss = boss
        self.size = self.boss.get_size()
        self.print_after_move = True
        self.do_print(None)

    def show_message(self, message):
        print message

    def _ascii(self):
        data = self.boss.get_raw_data()
        cc = len(data[1])
        cc = map(str, range(cc))
        head = "   " + ' '.join(cc)
        rr = ["%d  %s" % (c, ints_to_row(r)) for c,r in enumerate(data)]
        rr.insert(0,head)
        rr.insert(1,"")
        return '\n'.join(rr)

    def _line_to_ints(self, line, count = None):
        # In questo modo si può anche scrivere:
        # move 01 34 oppure move 0134 oppure ...
        cc = [c for c in line if c in "0123456789"]
        if count <> None and len(cc) <> count:
            self.show_message("Fornire %d interi" % count)
            return []
        try:
            cc = map(int, cc)
        except:
            self.show_message("Fornire %d INTERI" % count)
            return []
        return cc
        
    # gestori degli eventi
    def do_print(self, line):
        s = self._ascii()
        print s

    def do_move(self, line):
        cc = self._line_to_ints(line, 4)
        if not cc: return

        fc, tc = cc[0:2], cc[2:4]

        if not self.boss.can_move(fc, tc):
            self.show_message("Spostamento impossibile")
            return
        self.boss.move(fc, tc)
        if self.print_after_move: self.do_print(None)

    def do_about(self, line):
        self.show_message(common.about_message)

def get_gui_for_boss(boss):
    return Cli(boss)
