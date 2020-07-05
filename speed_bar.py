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
        self._style = ttk.Style()
        self._style.theme_use('classic')
        self._style_name = style_name + ".Horizontal.TProgressbar"
        self._style.configure(self._style_name, foreground='black', background='grey')
        ttk.Progressbar.__init__(self, master, style=self._style_name,
                                 orient="vertical", length=500, mode="determinate", maximum=255, value=0)
        self._speed_is_negative = False
        self._color = "grey"
        self._scale = 255
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

    def _set_value(self, p):
        """
        This function determinates how much of SpeedBar will be filled with color.
        :param p: Determinate current color and height of speed bar. It should be float from range -1, 1.
        :return: None
        """
        if not -1 <= p <= 1:
            raise ValueError(f"Function used to calculate speed bar height should return values"
                             f" from -1 to 1. {p} given")
        if p >= 0:
            self._speed_is_negative = False
        else:
            self._speed_is_negative = True
        p = abs(p)
        self['value'] = int(p * self["maximum"])
        self._get_colour(p)
        self._style.configure(self._style_name, foreground=self._color, background=self._color)
        self['style'] = self._style_name
        self.update_idletasks()

    def _get_colour(self, p):
        """
        This function sets new color of bar, which depends on bar height.
        :param p: Determinate current color and height of speed bar. It should be float from range -1, 1.
        :return: None
        """
        if not self._speed_is_negative:
            blue = hex(0)[2:]
            if p <= 0.5:
                green = hex(self._scale)[2:]
                red = hex(int(2 * p * self._scale))[2:]
            else:
                green = hex(int(self._scale - 2 * (p - 0.5) * self._scale))[2:]
                red = hex(self._scale)[2:]
        else:
            red = hex(int(p * .8 * self._scale))[2:]
            green = hex(0)[2:]
            blue = hex(int(max(1 - p, 0.3) * self._scale))[2:]
        RGB = [red, green, blue]
        RGB = list(map(lambda x: '0' + x if len(x) == 1 else x, RGB))
        self._color = "#" + "".join(RGB)


if __name__ == "__main__":
    p=-1
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