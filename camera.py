import PIL
from PIL import Image, ImageTk
import pytesseract
import cv2
from tkinter import *
from datetime import datetime
import os


class Camera(cv2.VideoCapture):
    def __init__(self, master, turn_upside_down=False, get_mirror_view=False):
        """
        Camera allows you to display image from webcam, take photos, and record videos.
        :param master: tkinter.frame on which you want to display image from camera.
        :param turn_upside_down: Flag which you can set if you want to display image from camera
        upside down.
        :param get_mirror_view: Flag which you can set if you want to display image from camera
        in mirror view.
        """
        self.master = master
        index_of_used_camera = 0
        super().__init__(index_of_used_camera)
        self._video_type_str = "avi"
        self._video_type = Camera.VIDEO_TYPE[self._video_type_str]
        self._video_dim = Camera.STD_DIMENSIONS["480p"]
        self._window = Label(master)
        self._window_dims = self._window.winfo_height(), self._window.winfo_width()
        self._frame_dim = Camera.STD_DIMENSIONS["480p"]
        Camera.change_res(self, *self._frame_dim)
        self._window.config(bg="#a1a1a1")
        self.turn_upside_down = turn_upside_down
        self.get_mirror_view = get_mirror_view
        self._isrecording = False

    def show_frames(self):
        """
        This function displays camera image on screen.
        :return: None
        """
        self.rep, self.frame = self.read()
        self._flip_frame_if_wanted()
        self._resize_frame_if_wanted()
        self._display_frame_on_screen()
        ms_to_next_call = 10
        self._window.after(ms_to_next_call, self.show_frames)

    def _flip_frame_if_wanted(self):
        """
        Get mirror view or flip upside down frame if user set flags - turn_upside_down or get_mirror_view when create
        camera obj.
        :return: None
        """
        if self.get_mirror_view:
            self.frame = cv2.flip(self.frame, 1)
        if self.turn_upside_down:
            self.frame = cv2.flip(self.frame, 0)

    def _resize_frame_if_wanted(self):
        """
        Resize frame to window size.
        :return: None
        """
        self._frame_dim = self._window.winfo_width(), self._window.winfo_height()
        self.frame = cv2.resize(self.frame, self._frame_dim)

    def _display_frame_on_screen(self):
        """
        Display frame on the screen.
        :return: None
        """
        self.imgtk = Camera.prepare_frame(self.frame)
        self._window.imgtk = self.imgtk
        self._window.configure(image=self.imgtk)

    def take_photo(self):
        """
        This function takes a photo and write it in photos folder with current date.
        :return: None
        """
        photo_name = "photos/photo " + str(datetime.now()) + ".png"
        cv2.imwrite(photo_name, self.frame)

    def prepare_recording(self):
        """
        This function is recording a video and is saving it in videos folder with current date.
        :return: None
        """
        self.video_name = "videos/video" + str(datetime.now()) + "." + self._video_type_str
        self.video_file = cv2.VideoWriter(self.video_name, self._video_type, 25, self._video_dim)

    def monitor_video_recording(self):
        """
        This function checks if camera should to record video, and deals with it if yes.
        :return: None
        """
        ms_to_next_call = 30
        if self._isrecording:
            self.video_frame = cv2.resize(self.frame, self._video_dim)
            self.video_file.write(self.video_frame)
        self._window.after(ms_to_next_call, self.monitor_video_recording)

    def place(self, relheight=0, relwidth=0, relx=0, rely=0):
        """
        This function places camera frame on master.
        :param relheight: Relative height of button.
        :param relwidth: Relative width of button.
        :param relx: Relative horizontal position of button.
        :param rely: Relative vertical position of button.
        :return: None
        """
        self._window.place(relheight=relheight, relwidth=relwidth, relx=relx, rely=rely)

    STD_DIMENSIONS = {
        "480p": (640, 480),
        "720p": (1280, 720),
        "1080p": (1920, 1080),
        "4k": (3840, 2160),
    }

    VIDEO_TYPE = {
        'avi': cv2.VideoWriter_fourcc(*'XVID'),
        'mp4': cv2.VideoWriter_fourcc(*'XVID'),
    }

    @staticmethod
    def prepare_frame(frame):
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = PIL.Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        return imgtk

    @staticmethod
    def get_video_type(filename):
        filename, ext = os.path.splitext(filename)
        if ext in Camera.VIDEO_TYPE:
            return Camera.VIDEO_TYPE[ext]
        return Camera.VIDEO_TYPE['avi']

    @staticmethod
    def change_res(cap, width, height):
        cap.set(3, width)
        cap.set(4, height)

    @staticmethod
    def get_dims(cap, res='1080p'):
        width, height = Camera.STD_DIMENSIONS["480p"]
        if res in Camera.STD_DIMENSIONS:
            width, height = Camera.STD_DIMENSIONS[res]
        Camera.change_res(cap, width, height)
        return width, height

