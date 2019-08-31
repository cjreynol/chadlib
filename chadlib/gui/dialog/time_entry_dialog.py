from .time_entry    import TimeEntry
from .dialog        import Dialog


class TimeEntryDialog(Dialog):
    """
    Dialog for entering an amount of time.
    """

    def __init__(self, callback, callback_args = None, 
                    validation_check = None):
        super().__init__("Enter a time", callback, callback_args, 
                            validation_check)
    
    def _create_widgets(self):
        super()._create_widgets()
        self.time_entry = TimeEntry()

    def _arrange_widgets(self):
        self.time_entry.grid(row = 0, column = 0, columnspan = 3)
        self.confirm_button.grid(row = 1, column = 0)
        self.cancel_button.grid(row = 1, column = 2)

    def _get_data(self):
        return self.time_entry.get()
