import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class InitialWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="DNS Manager")
        self.set_border_width(10)

        label = Gtk.Label()
        label.set_text("Hello, World!")
        self.add(label)

win = InitialWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()