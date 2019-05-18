from datetime           import timedelta
from tkinter            import Entry
from tkinter.messagebox import showwarning

from .dialog            import Dialog


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

        self.hour_entry = Entry(self)
        self.minute_entry = Entry(self)
        self.second_entry = Entry(self)

    def _arrange_widgets(self):
        self.hour_entry.grid(row = 0, column = 0)
        self.minute_entry.grid(row = 0, column = 1)
        self.second_entry.grid(row = 0, column = 2)

        self.confirm_button.grid(row = 1, column = 0)
        self.cancel_button.grid(row = 1, column = 2)

    def _get_data(self):
        time_obj = None
        try:
            h = self.hour_entry.get()
            m = self.minute_entry.get()
            s = self.second_entry.get()

            if h == "": h = 0
            if m == "": m = 0
            if s == "": s = 0

            time_obj = timedelta(hours = h, minutes = m, seconds = s)
        except TypeError as err:
            showwarning("Error creating time object", str(err), parent = self)

        return time_obj
