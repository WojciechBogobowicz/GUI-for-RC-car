import tkinter as tk
from PIL import ImageTk, Image


class ImgButton(tk.Button):
    button_number = 0

    def __init__(self, master, photo_file="", action=None, scale=1):
        """
        ImgButton inherits from tkinter.Button, this kind of button doesn't have text on it,
        only image. This object is scalable.
        :param master: tkinter.frame on which you want to place ImgButton.
        :param photo_file: Path to button icon.
        :param action: Function called when button would be clicked.
        :param scale: Float from 0 to 1, determinate how big image on button would be.
        """
        self._master = master
        self._path_to_image = photo_file
        img = Image.open(self._path_to_image)
        self._img = ImageTk.PhotoImage(img)
        self._img_proportion = self._img.height()/self._img.width()
        self._size = (200, 200*self._img_proportion)
        self._relative_button_height = 1
        self._relative_button_width = 1
        self._scale = scale
        self._clicks = 0
        self._master.bind("<Configure>", self._handle_resize, add="+")
        super().__init__(self._master, image=self._img, bg="grey", command=action)
        ImgButton.button_number += 1

    def change_image(self, new_image):
        """
        This function allows you to change button image.
        :param new_image: Str. Path to image.
        :return: None
        """
        self._path_to_image = new_image
        self._refresh_button_image()

    def _refresh_button_image(self):
        img = Image.open(self._path_to_image).resize(self._size)
        self._img = ImageTk.PhotoImage(img)
        self["image"] = self._img

    def update(self):
        """
        This function is checking if button size or image was changed, and correct those params.
        :return: None
        """
        screen_width = self._master.winfo_width()
        screen_height = self._master.winfo_height()
        super().update()
        self._update_image_size(screen_width, screen_height)
        self._refresh_button_image()

    #ToDo Napisać od nowa? Ta funckja źle działa dla obrazków znacząco wyzszych niż szerszych
    def _update_image_size(self, screen_width, screen_height):
        horizontal_length_that_image_can_have = screen_width * self._relative_button_width * self._scale
        vertical_length_that_image_can_have = screen_height * self._relative_button_height * self._scale
        # take minimum becuse I want keep constant proportions, and be sure that whole
        # image would fit well in button.
        new_image_width = min(
            horizontal_length_that_image_can_have,
            vertical_length_that_image_can_have
        )
        new_image_height = new_image_width * self._img_proportion
        self._size = int(new_image_width), int(new_image_height)

    def _handle_resize(self, event):
        """
        This function is resizing button image to fit button if window is resizing.
        :param event: obj with new window size.
        :return: None
        """
        self._update_image_size(event.width, event.height)
        self._refresh_button_image()

    def click(self):
        self._clicks += 1

    @property
    def counted_clicks(self):
        return self._clicks

    def place(self, relheight=0, relwidth=0, relx=0, rely=0):
        """
        This function places button on master.
        :param relheight: Relative height of button.
        :param relwidth: Relative width of button.
        :param relx: Relative horizontal position of button.
        :param rely: Relative vertical position of button.
        :return: None
        """
        super().place(relheight=relheight, relwidth=relwidth, relx=relx, rely=rely)
        self._relative_button_height = relheight
        self._relative_button_width = relwidth




