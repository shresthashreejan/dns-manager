import gi
import json
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class InitialWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="DNS Manager")
        self.set_default_size(600, 400)
        self.set_border_width(20)

        vbox_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox_main)

        hbox_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        vbox_main.pack_start(hbox_buttons, False, False, 0)

        info_label = Gtk.Label(label="Currently connected to Quad9")
        hbox_buttons.pack_start(info_label, False, False, 0)

        add_button = Gtk.Button(label="+")
        add_button.connect("clicked", self.add_dns_server)
        hbox_buttons.pack_end(add_button, False, False, 0)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        vbox_main.pack_start(scrolled_window, True, True, 0)

        vbox_cards = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        scrolled_window.add(vbox_cards)

        try:
            with open('dns.json', 'r') as f:
                configurations = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            configurations = []

        for config in configurations:
            card_button = self.create_card(config)
            vbox_cards.pack_start(card_button, False, False, 0)

    def create_card(self, config):
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        card_button = Gtk.Button()

        label = Gtk.Label(label="{}".format(config['Name']))
        label.set_alignment(0, 0.5)

        tick_icon = Gtk.Image.new_from_icon_name("object-select", Gtk.IconSize.BUTTON)
        hbox.pack_start(label, True, True, 0)
        hbox.pack_end(tick_icon, False, False, 0)

        card_button.add(hbox)
        card_button.connect("clicked", self.show_server_details, config['Name'], ', '.join(config['IPv4']), ', '.join(config['IPv6']))

        return card_button

    def show_server_details(self, widget, name, ipv4, ipv6):
        dialog = Gtk.MessageDialog(parent=self, flags=Gtk.DialogFlags.MODAL, type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK, message_format="DNS Details")

        dialog.format_secondary_text("Name: {}\nIPv4: {}\nIPv6: {}".format(name, ipv4, ipv6))
        dialog.run()
        dialog.destroy()

    def add_dns_server(self, widget):
        dialog = AddServerDialog(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            name = dialog.name_entry.get_text()
            ipv4_addresses = [dialog.primary_ipv4_entry.get_text(), dialog.secondary_ipv4_entry.get_text()]
            ipv6_addresses = [dialog.primary_ipv6_entry.get_text(), dialog.secondary_ipv6_entry.get_text()]

            try:
                with open('dns.json', 'r') as f:
                    configurations = json.load(f)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                configurations = []

            configurations.append({'Name': name, 'IPv4': ipv4_addresses, 'IPv6': ipv6_addresses})

            with open('dns.json', 'w') as f:
                json.dump(configurations, f, indent=4)

            print("DNS server added.")

            self.destroy()
            new_win = InitialWindow()
            new_win.connect("destroy", Gtk.main_quit)
            new_win.show_all()
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancelled.")

        dialog.destroy()

class AddServerDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Add DNS Server", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(200, 200)
        self.set_border_width(20)

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        self.get_content_area().add(grid)

        name_label = Gtk.Label(label="Name:")
        self.name_entry = Gtk.Entry()
        primary_ipv4_label = Gtk.Label(label="IPv4:")
        self.primary_ipv4_entry = Gtk.Entry()
        secondary_ipv4_label = Gtk.Label(label="IPv4 2:")
        self.secondary_ipv4_entry = Gtk.Entry()
        primary_ipv6_label = Gtk.Label(label="IPv6:")
        self.primary_ipv6_entry = Gtk.Entry()
        secondary_ipv6_label = Gtk.Label(label="IPv6 2:")
        self.secondary_ipv6_entry = Gtk.Entry()

        grid.attach(name_label, 0, 0, 1, 1)
        grid.attach_next_to(self.name_entry, name_label, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach(primary_ipv4_label, 0, 1, 1, 1)
        grid.attach_next_to(self.primary_ipv4_entry, primary_ipv4_label, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach(secondary_ipv4_label, 0, 2, 1, 1)
        grid.attach_next_to(self.secondary_ipv4_entry, secondary_ipv4_label, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach(primary_ipv6_label, 0, 3, 1, 1)
        grid.attach_next_to(self.primary_ipv6_entry, primary_ipv6_label, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach(secondary_ipv6_label, 0, 4, 1, 1)
        grid.attach_next_to(self.secondary_ipv6_entry, secondary_ipv6_label, Gtk.PositionType.RIGHT, 1, 1)

        self.show_all()

win = InitialWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()