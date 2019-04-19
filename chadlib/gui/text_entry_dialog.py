from tkinter import Button, Entry, Toplevel


class TextEntryDialog(Toplevel):
    """
    Single entry textbox dialog.

    Accepts a dialog title, callback to invoke upon confirmation, and data 
    to pass along to the callback to allow for capturing state.
    """

    def __init__(self, text_prompt, callback, callback_args):
        super().__init__()

        self.title(text_prompt)
        self.callback = callback
        self.callback_args = callback_args

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
        """
        self.callback(self.text_entry.get(), self.callback_args)
        self._cancel()

    def _cancel(self):
        """
        Close the dialog without taking any action.
        """
        self.destroy()
