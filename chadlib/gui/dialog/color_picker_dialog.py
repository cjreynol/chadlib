from tkinter    import Label, Scale, HORIZONTAL

from .dialog    import Dialog


class ColorPickerDialog(Dialog):
    """
    """

    SCALE_MIN = 0
    SCALE_MAX = 255
    
    def __init__(self, callback, callback_args = None, 
                    validation_check = None):
        super().__init__("Pick a color", callback, callback_args, 
                            validation_check)

    def _create_widgets(self):
        super()._create_widgets()
        self.swatch_label = Label(self, text = (" " * 10) + ("\n" * 7))
        self.r_scale = Scale(self, orient = HORIZONTAL, 
                                from_ = self.SCALE_MIN,
                                to = self.SCALE_MAX)
        self.g_scale = Scale(self, orient = HORIZONTAL, 
                                from_ = self.SCALE_MIN,
                                to = self.SCALE_MAX)
        self.b_scale = Scale(self, orient = HORIZONTAL, 
                                from_ = self.SCALE_MIN,
                                to = self.SCALE_MAX)
        self._update_swatch()

    def _arrange_widgets(self):
        self.swatch_label.grid(row = 0, column = 0, rowspan = 3)
        self.r_scale.grid(row = 0, column = 1)
        self.g_scale.grid(row = 1, column = 1)
        self.b_scale.grid(row = 2, column = 1)

        self.cancel_button.grid(row = 3, column = 0)
        self.confirm_button.grid(row = 3, column = 1)

    def _bind_actions(self):
        super()._bind_actions()
        self.r_scale["command"] = self._update_swatch
        self.g_scale["command"] = self._update_swatch
        self.b_scale["command"] = self._update_swatch

    def _get_data(self):
        """
        Return the hex format string built from the three scales.
        """
        rgb = map(lambda x: hex(x)[2:], 
                (self.r_scale.get(), self.g_scale.get(), self.b_scale.get()))
        return "#{:0>2}{:0>2}{:0>2}".format(*rgb)

    def _update_swatch(self, *args):
        """
        Update the color of the swatch label to the current selection.
        """
        self.swatch_label["background"] = self._get_data()
