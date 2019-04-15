from abc            import ABC, abstractmethod

from .root_window   import RootWindow


class ControllerBase(ABC):
    """
    Base template for Controller that implements the interface expected by the 
    RootWindow class.
    """

    WINDOW_TITLE = None
    DEFAULT_VIEW = None
    
    def __init__(self):
        if self.WINDOW_TITLE is None:
            raise RuntimeError("Window title must be defined by subclasses.")

        self.window = RootWindow(self, self.WINDOW_TITLE, self.DEFAULT_VIEW)

    def start(self):
        self.window.start()

    def stop(self):
        self.window.destroy()

    def update(self):
        self.window.update()
