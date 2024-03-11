import gi
import json
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class InitialWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="DNS Manager")
        self.set_border_width(10)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        label = Gtk.Label()
        label.set_text("No DNS configurations yet.")
        vbox.pack_start(label, True, True, 0)

        add_button = Gtk.Button(label="+ Add DNS Server")
        add_button.connect("clicked", self.add_dns_server)
        vbox.pack_start(add_button, False, False, 0)

    def add_dns_server(self, widget):
        dialog = AddServerDialog(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            name = dialog.name_entry.get_text()
            ipv4_address = dialog.ipv4_entry.get_text()
            ipv6_address = dialog.ipv6_entry.get_text()

            try:
                with open('dns_config.json', 'r') as f:
                    configurations = json.load(f)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                configurations = []

            configurations.append({'Name': name, 'IPv4': ipv4_address, 'IPv6': ipv6_address})

            with open('dns_config.json', 'w') as f:
                json.dump(configurations, f, indent=4)

            print("DNS server added.")
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancelled.")

        dialog.destroy()

class AddServerDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Add DNS Server", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(200, 200)

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        self.get_content_area().add(grid)

        name_label = Gtk.Label(label="Name:")
        self.name_entry = Gtk.Entry()
        ipv4_label = Gtk.Label(label="IPv4:")
        self.ipv4_entry = Gtk.Entry()
        ipv6_label = Gtk.Label(label="IPv6:")
        self.ipv6_entry = Gtk.Entry()

        grid.attach(name_label, 0, 0, 1, 1)
        grid.attach_next_to(self.name_entry, name_label, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach(ipv4_label, 0, 1, 1, 1)
        grid.attach_next_to(self.ipv4_entry, ipv4_label, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach(ipv6_label, 0, 2, 1, 1)
        grid.attach_next_to(self.ipv6_entry, ipv6_label, Gtk.PositionType.RIGHT, 1, 1)

        self.show_all()

win = InitialWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()