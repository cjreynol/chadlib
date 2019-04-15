from abc        import ABC, abstractmethod
from tkinter    import Frame


class View(Frame, ABC):
    """
    Generic widget for creation of views to popuate the applications main 
    window.  

    Subclasses are expected to override the create and arrange widget methods.
    """
    
    def __init__(self, controller, root, *args, **kwargs):
        """
        Creates the frame for the view, stores the controller, and then steps 
        through the expected actions for the view.

        Not expected to be overridden, only extended in special cases.
        """
        super().__init__(root, *args, **kwargs)
        self.controller = controller

        self._create_widgets()
        self._arrange_widgets()
        self._bind_actions()

    @abstractmethod
    def _create_widgets(self):
        """
        Expected to define and initialize all of the widget attributes for 
        the class and their visual attributes.
        """
        pass
        
    @abstractmethod
    def _arrange_widgets(self):
        """
        Expected to place all of the attributes for the class inside the frame.
        """
        pass

    def _bind_actions(self):
        """
        Used to attach actions to buttons and other widgets.  

        Not abstract for the case of informational widgets that have no 
        actions or widgets that are instantiated programatically and need the 
        actions created at the same time.
        """
        pass
