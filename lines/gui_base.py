import gtk

class BaseWindow(gtk.Window):

    def __init__(self):
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        self.connect("delete_event", self.delete_event)
        self.connect("destroy", self.destroy)

    def delete_event(self, widget, event, data=None):
        "Make delete_event call destroy"
        return gtk.FALSE

    def destroy(self, widget, data=None):
        "Clean quit from gtk main loop"
        gtk.main_quit()

    def run(self):
        "Start gtk main loop" 
        self.show_all()
        gtk.main()

class AboutBox(gtk.Window):

    def __init__(self, message):
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)

        self.set_size_request(300, 200)
        v = gtk.VBox(gtk.FALSE, 2)
        self.add(v)

        s = gtk.Label(message)
        v.pack_start(s, gtk.FALSE, gtk.TRUE, 0)

        h = gtk.HBox(gtk.FALSE,2)
        b = gtk.Button("OK", gtk.STOCK_OK)
        h.pack_end(b, gtk.FALSE, gtk.TRUE, 0)
        v.pack_end(h, gtk.FALSE, gtk.TRUE, 0)

        b.connect   ("clicked", self.destroy)
        self.connect("delete_event", self.delete_event)
        self.connect("destroy", self.destroy)
        
    def delete_event(self, widget, event, data=None):
        return gtk.FALSE

    def destroy(self, widget, data=None):
        gtk.quit()
        
def show_about(message):
    AboutBox(message).show_all()
    
class StatusBar(gtk.Statusbar):

    def __init__(self):
        gtk.Statusbar.__init__(self)
        self.id = self.get_context_id("default")

    def show(self, message):
        try:
            self.pop(self.id)
        except:
            pass
        self.push(self.id, message)
        
class MenuBar(gtk.MenuBar):

    def __init__(self):
        gtk.MenuBar.__init__(self)

    def add_menu(self, title):
        m = Menu(title)
        self.append(m.item)
        return m

    def easy_make_menu(self, title, items):
        o = self.add_menu(title)
        for t,c in items:
            if t == "-":
                o.add_separator()
            else:
                o.add_item(t,c)
        return o
    
class Menu(gtk.Menu):
    
    def __init__(self, title):
        gtk.Menu.__init__(self)
        self.item = gtk.MenuItem(title)
        self.item.set_submenu(self)

    def add_item(self, title, on_activate = None):
        i = MenuItem(title)
        self.append(i)
        if on_activate:
            i.connect("activate", on_activate)
        return i

    def add_separator(self):
        i = gtk.SeparatorMenuItem()
        self.append(i)
        return i
        
class MenuItem(gtk.MenuItem):
    def __init__(self, title):
        gtk.MenuItem.__init__(self, title)
        
class FullWindow(BaseWindow):
    
    def __init__(self, title = "Main Window", content = None):
        BaseWindow.__init__(self)

        self.set_title(title)
        self.set_size_request(200,100)

        self.box = gtk.VBox(gtk.FALSE, 3)
        self.add(self.box)

        self.make_menu_bar()

        if not content: content = self.make_fake_content()
        self.set_content(content)
        
        self.make_status_bar()

    def show_message(self, message):
        self.status_bar.show(message)

    def make_fake_content(self):
        b = gtk.Button("Hi Luke")
        return b
    
    def make_menu_bar(self):
        self.menu_bar = MenuBar()
        # def pack_start(child, expand, fill, padding)
        self.box.pack_start(self.menu_bar, gtk.FALSE, gtk.TRUE, 0)
        return self.menu_bar

    def make_status_bar(self):
        self.status_bar = StatusBar()      
        self.box.pack_end(self.status_bar, gtk.FALSE, gtk.TRUE, 0)
        return self.status_bar

    def set_content(self, content):
        try:
            self.box.remove(self.content)
        except:
            pass
        self.content = content
        self.box.pack_start(content, gtk.TRUE, gtk.TRUE, 0)
        
def go():

    FullWindow().run()

if __name__ == "__main__":

    go()
    
