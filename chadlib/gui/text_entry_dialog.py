from tkinter    import Entry

from .dialog    import Dialog


class TextEntryDialog(Dialog):
    """
    Single entry textbox dialog.
    """

    def __init__(self, text_prompt, callback, callback_args = None, 
                    validation_check = None):
        super().__init__(text_prompt, callback, callback_args, 
                            validation_check)

    def _create_widgets(self):
        super()._create_widgets()
        self.text_entry = Entry(self)

    def _arrange_widgets(self):
        self.text_entry.grid(row = 0, column = 0, columnspan = 2)
        self.text_entry.focus()
        self.confirm_button.grid(row = 1, column = 1)
        self.cancel_button.grid(row = 1, column = 0)

    def _get_data(self):
        return self.text_entry.get()
