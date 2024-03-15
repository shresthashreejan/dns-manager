import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import subprocess
import json
from .add_server_dialog import AddServerDialog

class InitialWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="DNS Manager")
        self.set_default_size(600, 400)
        self.set_border_width(20)

        self.configurations = []
        try:
            with open('dns.json', 'r') as f:
                self.configurations = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            pass

        self.setup_ui()

    def setup_ui(self):
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

        self.vbox_cards = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        scrolled_window.add(self.vbox_cards)

        for config in self.configurations:
            self.add_card(config)

    def add_card(self, config):
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        card_button = Gtk.Button()

        label = Gtk.Label(label="{}".format(config['Name']))
        label.set_alignment(0, 0.5)

        hbox.pack_start(label, True, True, 0)

        card_button.add(hbox)
        card_button.connect("clicked", self.show_server_details, config['Name'], ', '.join(config['IPv4']), ', '.join(config['IPv6']))

        self.vbox_cards.pack_start(card_button, False, False, 0)
        self.show_all()

    def show_server_details(self, widget, name, ipv4, ipv6):
        dialog = Gtk.MessageDialog(parent=self, flags=Gtk.DialogFlags.MODAL, type=Gtk.MessageType.INFO, message_format="DNS Details")

        dialog.format_secondary_text("Name: {}\nIPv4: {}\nIPv6: {}".format(name, ipv4, ipv6))
        dialog.add_button("Remove", Gtk.ResponseType.CANCEL)
        dialog.add_button("Connect", Gtk.ResponseType.OK)
        response = dialog.run()
        dialog.destroy()

        if response == Gtk.ResponseType.OK:
            command = ['bash', 'config_dns.sh', ipv4, ipv6]
            subprocess.run(command)
        elif response == Gtk.ResponseType.CANCEL:
            self.remove_server(widget, name)

    def remove_server(self, widget, name):
        for config in self.configurations:
            if config['Name'] == name:
                self.configurations.remove(config)
                break

        with open('dns.json', 'w') as f:
            json.dump(self.configurations, f, indent=4)

        for child in self.vbox_cards.get_children():
            if child.get_child().get_children()[0].get_label() == name:
                self.vbox_cards.remove(child)
                break

        self.show_all()


    def add_dns_server(self, widget):
        dialog = AddServerDialog(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            name = dialog.name_entry.get_text()
            ipv4_addresses = [dialog.primary_ipv4_entry.get_text(), dialog.secondary_ipv4_entry.get_text()]
            ipv6_addresses = [dialog.primary_ipv6_entry.get_text(), dialog.secondary_ipv6_entry.get_text()]

            self.configurations.append({'Name': name, 'IPv4': ipv4_addresses, 'IPv6': ipv6_addresses})

            with open('dns.json', 'w') as f:
                json.dump(self.configurations, f, indent=4)

            self.add_card({'Name': name, 'IPv4': ipv4_addresses, 'IPv6': ipv6_addresses})

            print("DNS server added.")

        elif response == Gtk.ResponseType.CANCEL:
            print("Cancelled.")

        dialog.destroy()
