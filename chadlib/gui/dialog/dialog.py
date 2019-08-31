from abc                import ABC, abstractmethod
from tkinter            import Button, Entry, Toplevel

from chadlib.utility    import event_wrapper


class Dialog(Toplevel, ABC):
    """
    Generic widget to capture dialogs which follow the pattern of allowing 
    the user to provide some input and then passing that input to some 
    callback.
    """

    def __init__(self, title_text, callback, callback_args, validation_check):
        super().__init__()

        self.title(title_text)
        self._callback = callback
        self._callback_args = callback_args
        self._validation_check = validation_check

        self._create_widgets()
        self._arrange_widgets()
        self._bind_actions()

    @abstractmethod
    def _create_widgets(self):
        """
        Create the widgets for the dialog.
        """
        self.confirm_button = Button(self, text = "Confirm")
        self.cancel_button = Button(self, text = "Cancel")

    @abstractmethod
    def _arrange_widgets(self):
        """
        Place the widgets on the dialog window.
        """
        pass

    def _bind_actions(self):
        """
        Bind methods to the buttons and keybindings.
        """
        self.confirm_button["command"] = self._confirm
        self.bind("<Return>", event_wrapper(self._confirm))

        self.cancel_button["command"] = self._cancel
        self.bind("<Escape>", event_wrapper(self._cancel))

    @abstractmethod
    def _get_data(self):
        """
        Get the data from the dialog to pass to the callback.
        """
        pass

    def _confirm(self):
        """
        Call the given callback method with the given data and data from the 
        dialog, then close itself.

        If a validation check was given, ensure it passed before passing the 
        data back.
        TODO CJR:  Feedback if the validation check fails.
        """
        data = self._get_data()
        if (data is not None 
            and (self._validation_check is None 
                or self._validation_check(data))):
            if self._callback_args is not None:
                self._callback(data, self._callback_args)
            else:
                self._callback(data)
            self._cancel()

    def _cancel(self):
        """
        Close the whole dialog.
        """
        self.destroy()
