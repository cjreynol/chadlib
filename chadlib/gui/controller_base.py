from abc            import ABC, abstractmethod

from .root_window   import RootWindow


class ControllerBase(ABC):
    """
    Base template for Controller that implements the interface expected by the 
    RootWindow class.
    """

    def __init__(self, title, application_state = None, default_view = None, 
                    window_class = RootWindow):
        self.window = window_class(self, application_state, default_view, 
                                    title, self._get_menu_data())
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

    def _get_menu_data(self):
        pass
