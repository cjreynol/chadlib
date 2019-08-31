from datetime           import timedelta
from tkinter            import Entry, Frame
from tkinter.messagebox import showwarning


class TimeEntry(Frame):
    """
    Specialized Entry widget for entering time.
    """

    HOURS_LENGTH = 2
    MINUTES_LENGTH = 2
    SECONDS_LENGTH = 5

    def __init__(self, *args):
        super().__init__(*args)

        self._create_widgets()
        self._arrange_widgets()

    def _create_widgets(self):
        self.hour_entry = Entry(self, width = self.HOURS_LENGTH)
        self.minute_entry = Entry(self, width = self.MINUTES_LENGTH)
        self.second_entry = Entry(self, width = self.SECONDS_LENGTH)

    def _arrange_widgets(self):
        self.hour_entry.grid(row = 0, column = 0)
        self.minute_entry.grid(row = 0, column = 1)
        self.second_entry.grid(row = 0, column = 2)

    def get(self):
        time_obj = None
        try:
            h = self.hour_entry.get()
            m = self.minute_entry.get()
            s = self.second_entry.get()
            time_obj = timedelta(hours = h, minutes = m, seconds = s)
        except TypeError as err:
            showwarning("Error creating time object", str(err), parent = self)

        return time_obj

    def set(self, hours, minutes, seconds):
        self.hour_entry(0, str(hours))
        self.minute_entry(0, str(minutes))
        self.second_entry(0, str(seconds))
