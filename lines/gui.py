# -*- coding: iso-latin-1 -*-

import os
import random

import gtk

import common
import gui_base
import board
import utils

image_dir = "./images"
images = [ "empty.png", "blue.png", "light-blue.png", "purple.png",
           "yellow.png", "green.png", "orange.png", "red.png"]

def get_image(image):
    path = os.path.join(image_dir, image)
    return path

pixbufs= [gtk.gdk.pixbuf_new_from_file(get_image(img)) for img in images]
class StoneCell(gtk.Button):

    "Il widget che mostra le pedine in attesa di inserimento"

    def __init__(self):
        gtk.Button.__init__(self, None) #"%d:%d" % (row, col))

        self.set_size_request(40,40)
        self.image = gtk.Image()
        self.add(self.image)

    def set_value(self, value):
        pixbuf=pixbufs[value]
        pixbuf = pixbuf.scale_simple(30, 30, gtk.gdk.INTERP_BILINEAR)
        self.image.set_from_pixbuf(pixbuf)

class ButtonCell(gtk.Button):

    "Il widget per le pedine sulla scacchiera"

    def __init__(self, pos, back):
        gtk.Button.__init__(self, None)

        self.image = gtk.Image()
        self.add(self.image)

        self.pos = pos
        self.set_value(0)

        # self.connect("clicked", back, None)
        self.connect("pressed", back, None)

    def get_pos(self):
        return self.pos

    def set_value(self, value):
        self.value = value
    def update(self, size):
        pixbuf = pixbufs[self.value]
        pixbuf = pixbuf.scale_simple(size[0], size[1], gtk.gdk.INTERP_BILINEAR)
        self.image.set_from_pixbuf(pixbuf)

    def __str__(self):
        return str(self.pos)

Cell = ButtonCell

class Grid(gtk.Table):
    "La griglia che fa da GUI per la scacchiera"

    def __init__(self, size, back):
        "Griglia di dimensione SIZE, BACK � il gestore dei click delle celle"
        self.size = size
        r,c = size
        gtk.Table.__init__(self, r, c, gtk.TRUE)
        self.set_homogeneous(gtk.TRUE)
        self.set_size_request(400,400)
        self.cells = mat = board.Board( size )
        for r,c,v in mat:
            o = Cell( (r,c), back)
            mat.set_value( (r,c), o)
            self.attach(o, r, r+1, c, c+1)
        self.alloc=self.get_allocation()

    def size(self):
        "Le dimensioni della scacchiera"
        return self.cells.size()

    def update_from_boss(self, boss):
        "Aggiorna la scacchiera con i dati della BOARD"
        cell = self.cells.get_value
        for r,c,v in boss.get_data():
            pos = r,c
            # print "Setting %s to %d" % (str(pos), v)
            cell(pos).set_value(v)
        self.update_cells()

    def update_cells(self):
        a=self.get_allocation()
        self.alloc=a
        if a.width<=1 or a.height<=1:
            return
        size=(a.height/(self.size[0]+1),a.height/(self.size[1]+1))
        for r,c,v in self.cells:
            self.cells.get_value((r,c)).update(size)

class Window(gui_base.FullWindow):

    def __init__(self, boss):
        gui_base.FullWindow.__init__(self, "App")

        # self.boss e self.size sono usati nella costruzione della
        # grid, quindi serve settarla quanto prima
        self.boss = boss
        self.size = boss.get_size()

        # costruzione di parti dinamiche che dipendono da game
        self._make_menus()
        c = self._make_content()
        self.set_content(c)



        self.set_geometry_hints(min_width=400, min_height=400,
                                width_inc=50, height_inc=50,
                                base_width = 400,
                                base_height=400, min_aspect=1.0, max_aspect=1.0)


        # altri setting della finestra
        #self.set_size_request(600,600)
        self.set_resizable(gtk.TRUE)
        self.selected_pos = None
        self.alloc=self.get_allocation()
        # evento per il ridimensionamento della finestra
        self.connect_after('check-resize', self.on_check_resize)
        self.connect("window-state-event", self.on_window_state_event)
        # mostra la situazione iniziale del gioco
        self.update_from_boss()

    def _make_next_stones(self):
        h  = gtk.HBox(gtk.FALSE, 3)
        bb = []
        for c in range(3):
            b = StoneCell()
            bb.append(b)
            h.pack_end(b, gtk.FALSE, gtk.FALSE, 0)
        self._next_stones = bb
        self._score_label = gtk.Label()
        h.pack_start(self._score_label, gtk.FALSE, gtk.FALSE, 0)
        return h

    def _make_content(self):
        self.grid = Grid(self.size, self.on_cell_clicked)
        b = self._make_next_stones()
        v = gtk.VBox(gtk.FALSE, 2)
        v.pack_start(b,         gtk.FALSE, gtk.FALSE, 0)
        v.pack_end  (self.grid, gtk.TRUE,  gtk.TRUE,  0)
        return v

    def on_check_resize(self, window):
        if self.get_allocation() != self.alloc:
            self.grid.update_cells()
            self.alloc=self.get_allocation()

    def on_window_state_event(self, widget, event, data=None):
        #self.update_grid(widget)
        pass

    def step_cell(self, fc, tc):
        raise "NotImplemented"
        mess = "stepping %s -> %s" % (fc, tc)
        self.show_message(mess)
        tc.set_value(fc.value)
        fc.set_value(0)
        x = 400
        tc.queue_draw_area(0, 0, x, x)
        fc.queue_draw_area(0, 0, x, x)

    def on_cell_clicked(self, widget, data = None):
        old = self.selected_pos
        new = widget.get_pos()
        is_free = self.boss.is_free
        if not old:
            if is_free(new):
                self.show_message("Select a NON free cell!")
            else:
                self.show_message("Cell at %s selected" % str(new))
                self.selected_pos = new
        else:
            if new == old:
                self.show_message("Cell at %s DE-selected" % str(new))
                self.selected_pos = None
            else:
                if is_free(new):
                   if self.boss.can_move(old, new):
                       self.show_message("Moving %s to %s" %
                                         (str(old), str(new)))
                       self.do_move(old, new)
                       self.selected_pos = None
                   else:
                       self.show_message("NO path from %s to %s" %
                                         (str(old), str(new)))
                else:
                    self.show_message("Cell at %s selected" % str(new))
                    self.selected_pos = new

    def _make_menus(self):

        make = self.menu_bar.easy_make_menu

        make("_Game", (
            ("_New",  self.on_new_game),
            ("_Open", self.on_load_game),
            ("_Save", self.on_save_game),
            ("-", None),
            ("_Quit", self.destroy),
            ))

        make("_Help", (
            ("_Content", self.on_help),
            ("_About", self.on_about),
            ))

    def _update_next_stones(self):
        vv = self.boss.get_next_values()
        ss = self._next_stones
        for c,v in enumerate(vv):
            ss[c].set_value(v)

    def _update_score(self):
        s = self.boss.get_score()
        self._score_label.set_text("Punteggio: %3d" % s)

    def update_from_boss(self):
        self.grid.update_from_boss(self.boss)
        self._update_next_stones()
        self._update_score()

    # gestori degli eventi
    def on_help(self, widget):
        self.show_message("Read the source, Luke!")

    def on_about(self, widget):
        gui_base.show_about(common.about_message)

    def on_new_game(self, widget):
        self.boss.new_empty_game(self.size)
        self.update_from_boss()

    def on_load_game(self, widget):
        s = utils.choose_file_for_open()
        if s:
            self.show_message("Loading from: %s" % s)
            try:
                self.boss.load_from_file(s)
            except common.LinesError:
                self.show_message("Loading failed. %s is not a valid game save"%s)
            self.update_from_boss()
            self.show_message("Loading completed")

    def on_save_game(self, widget):
        s = utils.choose_file_for_save()
        if s:
            self.show_message("Saving to: %s" % s)
            self.boss.save_to_file(s)
            self.show_message("Game saved")

    # chiamate verso il "boss"
    def do_move(self, fc, tc):
        try:
            self.boss.move(fc, tc)
        except common.LinesError as e:
            self.show_message(str(e))
        self.update_from_boss()

def get_gui_for_boss(boss):
    return Window(boss)
