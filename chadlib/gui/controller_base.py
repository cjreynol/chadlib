from abc                import ABC, abstractmethod

from .menu_setup        import MenuSetup
from .root_window       import RootWindow


class ControllerBase(ABC):
    """
    Base template for Controller that implements the interface expected by the 
    RootWindow class.
    """

    def __init__(self, application_name, application_state = None, default_view = None, 
                    window_class = RootWindow):

        self.window = window_class(self, application_state, default_view, 
                                    application_name, self.get_menu_data())
        self.application_state = application_state

    @property
    def current_view(self):
        return self.window.current_view

    def start(self):
        self.window.start()

    def stop(self):
        self.window.destroy()

    def update(self):
        self.window.update()

    def get_menu_data(self):
        """
        Create the initial menu setup with default actions.

        Expected to be extended by subclasses, not overridden.
        """
        menu_setup = MenuSetup()
        menu_setup.add_submenu_item("Window", "Close Application", self.stop, 
                                    "{}-w")
        return menu_setup
