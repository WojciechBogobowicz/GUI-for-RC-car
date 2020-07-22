from time import sleep
from tkinter import ttk
import tkinter


class SpeedBar(ttk.Progressbar):
    def __init__(self, master, style_name, monitored_function, ms_to_update=10):
        """
        This widget displays last value returned by monitored function. In case of this project it is motor speed.
        :param master: Canvas or frame on with you want set speed bar.
        :param style_name: Any string. If you want two bars to have the same color put the same value here
        :param monitored_function: Function used to calculate progress on bar (have to return float form -1 to 1)
        :param ms_to_update: Int
        """
        self.master = master
        self.relative_height_abs = 0
        self._style = ttk.Style()
        self._style.theme_use('classic')
        self._style_name = style_name + ".Horizontal.TProgressbar"
        self._style.configure(self._style_name, foreground='black', background='grey')
        ttk.Progressbar.__init__(self, master, style=self._style_name,
                                 orient="vertical", length=500, mode="determinate",
                                 maximum=255, value=0)
        self._speed_is_negative = False
        self._color = "grey"
        self._max_value_for_color = 255
        self._monitored_function = monitored_function
        self._ms_to_update = ms_to_update
        self.update()

    @property
    def ms_to_update(self):
        return self._ms_to_update

    @ms_to_update.setter
    def ms_to_update(self, value):
        if value <= 0:
            raise ValueError(f"time have to be positive value in ms. {value} was given")
        self._ms_to_update = value

    def update(self):
        """
        This function actualises bar height. It is enough to call it once, because it calls itself recursively.
        :return:  None
        """
        self._set_value(self._monitored_function())
        self.master.after(self._ms_to_update, self.update)

    def _set_value(self, relative_height):
        """
        This function determinate how much of SpeedBar will be filled with color.
        :param relative_height: Determinate current color and height of speed bar. It should be float from range -1, 1.
        :return: None
        """

        if not -1 <= relative_height <= 1:
            raise ValueError(f"Function used to calculate speed bar height should return values"
                             f" from -1 to 1. {relative_height} given")
        self._set_speed_sign(relative_height)
        self.relative_height_abs = abs(relative_height)
        self['value'] = int(self.relative_height_abs * self["maximum"])
        self._set_colour()
        self._style.configure(self._style_name, foreground=self._color, background=self._color)
        self['style'] = self._style_name
        self.update_idletasks()

    def _set_speed_sign(self, relative_height):
        if relative_height >= 0:
            self._speed_is_negative = False
        else:
            self._speed_is_negative = True

    def _set_colour(self):
        """
        This function sets new color of bar, which depends on bar height.
        :param p: Determinate current color and height of speed bar. It should be float from range -1, 1.
        :return: None
        """
        if not self._speed_is_negative:
            self._set_colour_for_positive_value()
        else:
            self._set_colour_for_negative_value()

    def _set_colour_for_positive_value(self):
        max_value = self._max_value_for_color
        decreasing_value = int(max_value - 2 * (self.relative_height_abs - 0.5) * max_value)
        increasing_value = int(2 * self.relative_height_abs * max_value)
        blue = 0
        green = min(self._max_value_for_color, decreasing_value)
        red = min(increasing_value, self._max_value_for_color)
        RGB = red, green, blue
        self._color = self._translate_RGB_tuple_to_string(RGB)

    def _translate_RGB_tuple_to_string(self, RGB):
        RGB_in_hex_strings = [SpeedBar._get_hex_value(color) for color in RGB]
        formated_RGB = list(map(lambda x: '0' + x if len(x) == 1 else x, RGB_in_hex_strings))
        return "#" + "".join(formated_RGB)
   
    @staticmethod
    def _get_hex_value(dec_value):
        return hex(dec_value)[2:]

    def _set_colour_for_negative_value(self):
        red = int(self.relative_height_abs * .8 * self._max_value_for_color)
        green = 0
        blue = int(max(1 - self.relative_height_abs, 0.3) * self._max_value_for_color)
        RGB = red, green, blue
        self._color = self._translate_RGB_tuple_to_string(RGB)


if __name__ == "__main__":
    p = -1
    root = tkinter.Tk()
    def f():
        return 1
    bar = SpeedBar(root, "a", f)
    bar.pack()
    while True:
        if p > 1:
            p = -1
        bar._set_value(p)
        p += 0.01
        root.update()
        sleep(0.03)

    #root.mainloop()