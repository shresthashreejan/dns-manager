import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ServerDialog(Gtk.Dialog):

    LABELS = {
        "Name:": "name_entry",
        "Primary IPv4:": "primary_ipv4_entry",
        "Secondary IPv4:": "secondary_ipv4_entry",
        "Primary IPv6:": "primary_ipv6_entry",
        "Secondary IPv6:": "secondary_ipv6_entry"
    }

    def __init__(self, parent):
        super().__init__("Add DNS Server", parent, 0, (Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(200, 200)
        self.set_border_width(20)

        grid = Gtk.Grid(column_spacing=10, row_spacing=10)
        self.get_content_area().add(grid)

        self.entries = {}

        for row_index, (label_text, entry_attr) in enumerate(self.LABELS.items()):
            label = Gtk.Label(label=label_text)
            grid.attach(label, 0, row_index, 1, 1)
            entry_widget = Gtk.Entry()
            grid.attach_next_to(entry_widget, label, Gtk.PositionType.RIGHT, 1, 1)
            setattr(self, entry_attr, entry_widget)
            self.entries[entry_attr] = entry_widget

            if label_text == "Secondary IPv6:":
                grid.attach(Gtk.Label(), 0, row_index + 1, 1, 1)

        self.show_all()

    def validate_entries(self):
        for entry_widget in self.entries.values():
            if entry_widget.get_text().strip() == "":
                return False
        return True

    def show_toast_message(self, message):
        toast = Gtk.MessageDialog(parent=self, flags=Gtk.DialogFlags.MODAL, type=Gtk.MessageType.WARNING, message_format=message)
        toast.set_border_width(20)
        toast.run()
        toast.destroy()