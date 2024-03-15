import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from scripts.initial_window import InitialWindow

def main():
    win = InitialWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()