from collections    import OrderedDict
from platform       import system
from tkinter        import Menu


class MenuSetup:
    """
    Container to hold menu data and create the menu widget from it.
    """

    SHORTCUT_MODIFIERS = { "Darwin" : "Command",
                            "Windows": "Control" }

    def __init__(self):
        self.data = OrderedDict()

    def add_submenu_item(self, submenu_name, item_name, callback, 
                            shortcut = None):
        """
        Add the item to the list, or start the list if it does not exist.

        Instead of Ctrl/Cmd, shortcut expects a format blank in the shortcut 
        string that it will replace with the appropriate modifier for the 
        current platform.
        """
        if shortcut is not None:
            shortcut = shortcut.format(self.SHORTCUT_MODIFIERS[system()])
        try:
            self.data[submenu_name].append((item_name, callback, shortcut))
        except KeyError:
            self.data[submenu_name] = [(item_name, callback, shortcut)]

    def add_submenu_items(self, submenu_name, items):
        """
        Add multiple items from an iterator.

        items is expected to be a triple in the format of:
        (name, callback, shortcut key)
        """
        for item_name, callback, shortcut in items:
            self.add_submenu_item(submenu_name, item_name, callback, shortcut)

    def create_menubar(self, root):
        """
        Create the entire menu widget from the current menu data.
        """
        menubar = Menu(root)
        for menu_name, items in self.data.items():
            new_menu = Menu(menubar)
            menubar.add_cascade(label = menu_name, menu = new_menu)
            for item_name, callback, shortcut in items:
                if shortcut is None:
                    new_menu.add_command(label = item_name, command = callback)
                else:
                    # "Key-" replace because accelerators will not display 
                    # properly in the menu otherwise
                    new_menu.add_command(label = item_name, command = callback, 
                                    accelerator = shortcut.replace("Key-", ""))
                    root.bind("<{}>".format(shortcut), 
                                self._make_event_lambda(callback))
        return menubar

    def _make_event_lambda(self, function):
        """
        Wrap a function to capture and throw away the event argument.
        """
        return lambda event: function()
