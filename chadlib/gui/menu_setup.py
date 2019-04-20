from collections    import OrderedDict
from tkinter        import Menu


class MenuSetup:
    """
    Container to hold menu data and create the menu widget from it.
    """
    
    def __init__(self):
        self.data = OrderedDict()

    def add_submenu_item(self, submenu_name, item_name, callback):
        """
        Add the item to the list, or start the list if it does not exist.
        """
        try:
            self.data[submenu_name].append((item_name, callback))
        except KeyError:
            self.data[submenu_name] = [(item_name, callback)]

    def add_submenu_items(self, submenu_name, pairs):
        """
        Add multiple items from an iterator.
        """
        for item_name, callback in pairs:
            self.add_submenu_item(submenu_name, item_name, callback)

    def create_menubar(self, root):
        """
        Create the entire menu widget from the current menu data.
        """
        menubar = Menu(root)
        for menu_name, items in self.data.items():
            new_menu = Menu(menubar)
            menubar.add_cascade(label = menu_name, menu = new_menu)
            for item_name, callback in items:
                new_menu.add_command(label = item_name, command = callback)
        return menubar
