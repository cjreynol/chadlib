from abc                import ABC, abstractmethod


class SLController(ABC):
    """
    Companion class to the save/load component, specifies the interface 
    required for that component to function.
    """

    @abstractmethod
    def load_logic(self, filename):
        """
        Placeholder to be overridden by subclasses, intended to take load 
        data from the chosen filename.
        """
        pass

    @abstractmethod
    def save_logic(self, filename):
        """
        Placeholder to be overridden by subclasses, intended to get data from 
        the applicaiton and write it to the given file.
        """
        pass
