from abc                import ABC, abstractmethod
from os                 import makedirs
from os.path            import exists, expanduser, join
from platform           import system
from tkinter.filedialog import askopenfilename, asksaveasfilename

from .menu_setup        import MenuSetup
from .root_window       import RootWindow


class ControllerBase(ABC):
    """
    Base template for Controller that implements the interface expected by the 
    RootWindow class.
    """

    APPLICATION_NAME = None
    FILE_EXTENSION = None   # .something
    FILETYPES = None        # (("application files", "*" + FILE_EXTENSION),)

    SUPPORT_DIRS = {"Darwin" : expanduser(join("~", "Library", 
                                            "Application Support")),
                    "Windows" : expanduser(join("~", "AppData", "Local")) }

    def __init__(self, application_state = None, default_view = None, 
                    window_class = RootWindow):
        if self.APPLICATION_NAME is None:
            raise RuntimeError("Must define APPLICATION NAME.")

        self.SUPPORT_DIR = join(self.SUPPORT_DIRS[system()], 
                                self.APPLICATION_NAME)
        self.window = window_class(self, application_state, default_view, 
                                    self.APPLICATION_NAME, 
                                    self.get_menu_data())
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
        if self.FILE_EXTENSION is not None and self.FILETYPES is not None:
            menu_setup.add_submenu_item("File", "Save Drawings", self.save, 
                                        "{}-s")
            menu_setup.add_submenu_item("File", "Load Drawings", self.open, 
                                        "{}-o")

        menu_setup.add_submenu_item("Window", "Close Application", self.stop, 
                                    "{}-w")
        return menu_setup

    def ensure_support_dir_exists(self):
        """
        Check if the support directory exists, if not then create it.
        """
        if not exists(self.SUPPORT_DIR):
            makedirs(self.SUPPORT_DIR)

    def open(self):
        """
        Prompt the user for a filename and open/load that file.
        """
        self.ensure_support_dir_exists()
        filename = askopenfilename(initialdir = self.SUPPORT_DIR, 
                                    filetypes = self.FILETYPES) 
        if filename is not None:
            self._open_logic(filename)

    def save(self):
        """
        Prompt the user for a file and write data to that file.
        """
        self.ensure_support_dir_exists()
        filename = asksaveasfilename(initialdir = self.SUPPORT_DIR, 
                                        defaultextension = 
                                            self.FILE_EXTENSION,
                                        filetypes = self.FILETYPES) 
        if filename is not None:
            self._save_logic(filename)

    # the following two methods only need to be overridden if saving and 
    # loading is implemented
    def _open_logic(self, filename):
        """
        Placeholder to be overridden by subclasses, intended to take load 
        data from the chosen filename.
        """
        pass

    def _save_logic(self, filename):
        """
        Placeholder to be overriden by subclasses, intended to get data from 
        the applicaiton and write it to the given file.
        """
        pass
