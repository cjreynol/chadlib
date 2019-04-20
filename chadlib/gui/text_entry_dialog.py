from tkinter import Button, Entry, Toplevel


class TextEntryDialog(Toplevel):
    """
    Single entry textbox dialog.

    Accepts a dialog title, callback to invoke upon confirmation, data to 
    pass along to the callback to allow for capturing state, and an optional 
    validation method to ensure the data from the dialog meets some conditions.
    """

    def __init__(self, text_prompt, callback, callback_args, 
                    validation_check = None):
        super().__init__()

        self.title(text_prompt)
        self.callback = callback
        self.callback_args = callback_args
        self.validation_check = validation_check

        self.text_entry = Entry(self)
        self.confirm_button = Button(self, text = "Confirm", 
                                        command = self._confirm)
        self.cancel_button = Button(self, text = "Cancel", 
                                    command = self._cancel)

        self.text_entry.grid(row = 0, column = 0, columnspan = 2)
        self.text_entry.focus()
        self.confirm_button.grid(row = 1, column = 1)
        self.cancel_button.grid(row = 1, column = 0)

        self.bind("<Return>", lambda event: self._confirm())
        self.bind("<Escape>", lambda event: self._cancel())

    def _confirm(self):
        """
        Call the given callback, pass in the entered text and the given data, 
        then close the dialog.

        If a validation check was given, ensure it passed before passing the 
        data back.
        TODO CJR:  Feedback if the validation check fails.
        """
        text = self.text_entry.get()
        if self.validation_check is None or self.validation_check(text):
            if self.callback_args is not None:
                self.callback(text, self.callback_args)
            else:
                self.callback(text)
            self._cancel()

    def _cancel(self):
        """
        Close the dialog without taking any action.
        """
        self.destroy()
