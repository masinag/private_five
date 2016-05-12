# import pygtk
# pygtk.require('2.0')
import gtk, os

LAST_PATH_FILE="./data/.last_path.txt"

class FileOpener:

    def __init__(self, dir = "", file = "", title = ""):

        d = gtk.FileChooserDialog(
            title   = title,
            action  = gtk.FILE_CHOOSER_ACTION_OPEN,
            buttons = (gtk.STOCK_CANCEL,
                       gtk.RESPONSE_CANCEL,
                       gtk.STOCK_OPEN,
                       gtk.RESPONSE_OK))
        if dir:
            d.set_current_folder(dir)
        if file:
            d.set_current_name(file)    # FULL PATH required
        self.dial = d

    def show(self):
        r = self.dial.run()
        if r == gtk.RESPONSE_OK:
            self.filename = self. dial.get_filename()
            set_last_path(os.path.dirname(self.filename))
        else:
            self.filename = ""
        self.dial.destroy()

class FileSaver:

    def __init__(self, dir = "", file = "", title = ""):

        d = gtk.FileChooserDialog(
            title   = title,
            action  = gtk.FILE_CHOOSER_ACTION_SAVE,
            buttons = (gtk.STOCK_CANCEL,
                       gtk.RESPONSE_CANCEL,
                       gtk.STOCK_SAVE,
                       gtk.RESPONSE_OK))
        if dir:
            d.set_current_folder(dir)
        if file:
            d.set_current_name(file)    # FULL PATH required
        self.dial = d

    def show(self):
        r = self.dial.run()
        if r == gtk.RESPONSE_OK:
            self.filename = self. dial.get_filename()
            set_last_path(os.path.dirname(self.filename))
        else:
            self.filename = ""
        self.dial.destroy()

def choose_file_for_open(dir = "", file = "", title = ""):
    if not dir:
        dir=get_last_path()
    d = FileOpener(dir, file, title)
    d.show()
    return d.filename

def choose_file_for_save(dir = "", file = "", title = ""):
    if not dir:
        dir=get_last_path()
    d = FileSaver(dir, file, title)
    d.show()
    return d.filename

def get_last_path():
    try:
        with open (LAST_PATH_FILE) as f:
            path=f.next() # the path is in the first line of the file
    except IOError:
        path='.' # if the file doesn't exist return working directory
    return path


def set_last_path(dir):
    directory=os.path.dirname(LAST_PATH_FILE)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open (LAST_PATH_FILE, 'w') as f:
        f.write(dir)

if __name__ == "__main__":

    # s = choose_file_for_open(dir = "/tmp", title = "Hi Luke")
    s = choose_file_for_save(dir = "/tmp", title = "Hi Luke")
    print "Selection:", s or "<no file selected>"
