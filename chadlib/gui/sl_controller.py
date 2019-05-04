from abc                import abstractmethod
from os                 import makedirs
from os.path            import exists, expanduser, join
from platform           import system
from tkinter.filedialog import askopenfilename, asksaveasfilename

from .controller_base   import ControllerBase


class SLController(ControllerBase):

    SUPPORT_DIR_BASES = {"Darwin" : expanduser(join("~", "Library", 
                                            "Application Support")),
                        "Windows" : expanduser(join("~", "AppData", "Local")) }

    def __init__(self, file_extension, filetypes, application_name, *args):
        """
        file_extension should be a string in the format .extension
        filetypes in the format (("application files", "*" + file_extension),)
        """
        super().__init__(application_name, *args)
        self.file_extension = file_extension
        self.filetypes = filetypes
        self.support_dir = join(self.SUPPORT_DIR_BASES[system()], 
                                application_name)

    def ensure_dir_exists(self, dir_path):
        """
        Check if the directory exists, if not then create it.
        """
        if not exists(dir_path):
            makedirs(dir_path)

    def open(self):
        """
        Prompt the user for a filename and open/load that file.
        """
        self.ensure_dir_exists(self.support_dir)
        filename = askopenfilename(initialdir = self.support_dir, 
                                    filetypes = self.filetypes) 
        if filename is not None:
            self._open_logic(filename)

    def save(self):
        """
        Prompt the user for a file and write data to that file.
        """
        self.ensure_dir_exists(self.support_dir)
        filename = asksaveasfilename(initialdir = self.support_dir, 
                                        defaultextension = 
                                            self.file_extension,
                                        filetypes = self.filetypes) 
        if filename is not None:
            self._save_logic(filename)

    @abstractmethod
    def _open_logic(self, filename):
        """
        Placeholder to be overridden by subclasses, intended to take load 
        data from the chosen filename.
        """
        pass

    @abstractmethod
    def _save_logic(self, filename):
        """
        Placeholder to be overriden by subclasses, intended to get data from 
        the applicaiton and write it to the given file.
        """
        pass

    def get_menu_data(self):
        """
        Adds saving and loading options to the base menu.
        """
        menu_setup = super().get_menu_data()
        menu_setup.add_submenu_item("File", "Save Drawings", self.save, 
                                    "{}-s")
        menu_setup.add_submenu_item("File", "Load Drawings", self.open, 
                                    "{}-o")
        return menu_setup