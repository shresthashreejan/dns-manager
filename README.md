# Linux DNS Manager

Linux DNS Manager is a simple Python GTK application for managing DNS server configurations. It allows users to add, view, remove and setup DNS server configurations through a graphical user interface.

## Requirements

Before running the application, make sure you have the following dependencies installed:

-   Python 3
-   Python GObject Introspection bindings for GTK (`python3-gi`)
-   Python GObject Introspection bindings for Cairo (`python3-gi-cairo`)
-   GTK 3 Python bindings (`gir1.2-gtk-3.0`)

You can install these dependencies on Ubuntu or Debian-based systems using the following command:

```
sudo apt install python3 python3-gi python3-gi-cairo gir1.2-gtk-3.0
```

## Running the Application

To run the application, follow these steps:

1. Clone the repository or download the project files to your local machine.

2. Navigate to the project directory:

```
cd dns-manager
```

3. Run the main.py file using Python 3:

```
python3 main.py
```

4. The application window should appear, displaying the list of configured DNS servers. You can add new servers by clicking the "+" button, view server details, and remove servers by clicking the "Remove" button in the server details dialog.

## Contributing

Contributions to Linux DNS Manager are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
