from tkinter    import Tk, Menu


class RootWindow:
    """
    A wrapper around the Tk class, RootWindow is intended to be the base 
    of an application.  It provides functionality for creating the root 
    window of the application and easily swapping out views.
    """

    WINDOW_CLOSE_EVENT = "WM_DELETE_WINDOW"

    def __init__(self, controller, application_state, initial_view_class,
                    window_title, menu_setup):
        self.controller = controller
        self.root = self._create_root(window_title)
        self.application_state = application_state

        menubar = menu_setup.create_menubar(self.root)
        self.root.config(menu = menubar)
        
        self.current_view = initial_view_class
        if self.current_view is not None:
            self._display_view(self.current_view)


    def _create_root(self, window_title):
        """
        Create the root window with the given title, and register the 
        window close event with the controller so the application can 
        properly shut down.
        """
        root = Tk()
        root.title(window_title)
        root.protocol(self.WINDOW_CLOSE_EVENT, self.controller.stop)

        return root

    def _display_view(self, view):
        """
        Instantiate the new view with the correct arguments, then display it.
        """
        self.current_view = view(self.controller, self.root, 
                                    self.application_state)
        self.current_view.pack()

    def set_new_view(self, new_view):
        """
        Destroy the last view and display the given view.
        """
        if self.current_view is not None:
            self.current_view.destroy()
        self._display_view(new_view)

    def start(self):
        """
        Begin the root window's event handling loop.
        """
        self.root.mainloop()

    def destroy(self):
        """
        Destroy the window and its resources.
        """
        self.current_view.destroy()
        self.root.destroy()

    def update(self):
        """
        Force a visual update.
        """
        self.root.update()
