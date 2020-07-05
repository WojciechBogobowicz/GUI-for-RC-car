import tkinter as tk
from buttons import ImgButton
from joystick import Joysitck
from motor import Motors
from speed_bar import SpeedBar
from camera import Camera
from keyboard import Keyboard
import cv2


class MainApplication(tk.Frame):
    def __init__(self, master):
        """
        This class creates main application frame, and manages all process and objects used in project.
        :param master: tkinter.Tk obj.
        """
        tk.Frame.__init__(self, master)
        self.master = master
        self.motors = Motors()
        self.bg_color = "grey"
        self.create_right_frame()
        self.create_left_frame()
        self.create_midle_frame()
        self.keyboard = Keyboard()
        self.init_keyboard()

    def create_left_frame(self):
        """
        This function creates left panel which is used to manage speed.
        :return: None
        """
        self.frame_left = tk.Frame(root, bg=self.bg_color)
        self.frame_left.place(relheight=1, relwidth=.2)
        self.add_widgets_to_left_frame()

    def add_widgets_to_left_frame(self):
        """
        Adding widgets connected with speed display and management.
        :return: None
        """
        self.speed_limit_widget = tk.Label(self.frame_left, text=f"Speed Limit:\n{int(self.joystick.speed_limit*100)}%",
                                           relief="groove", borderwidth=5, bg=self.bg_color)
        self.speed_limit_up_button = tk.Button(self.frame_left, bg=self.bg_color, text="+", command=self.speed_limit_up)
        self.speed_limit_down_button = tk.Button(self.frame_left, bg=self.bg_color, text="-", command=self.speed_limit_down)
        self.left_motor_speed_bar = SpeedBar(self.frame_left, "L", self.motors.get_rel_left_speed)
        self.right_motor_speed_bar = SpeedBar(self.frame_left, "R", self.motors.get_rel_right_speed)
        self.motors_speed_frame = tk.LabelFrame(master=self.frame_left, bg=self.bg_color, text="Motors speed")
        self.motors_speed_label = tk.Label(master=self.motors_speed_frame, bg=self.bg_color, anchor="w",
                                           text=" Left motor speed:   {1:7.0f}% \n"
                                                "Right motor speed: {1:7.0f}%".format(
                                                int(100 * self.motors.get_rel_left_speed()),
                                                int(100 * self.motors.get_rel_right_speed())
                                           ))
        self.last_measured_motors_speeds = (-1, -1)

        def upadate_motor_speed_label():
            """
            This function is updating information on speed label. It is necessary to run it if you want your speed
            data to be displayed properly.
            :return: None
            """
            if not self.last_measured_motors_speeds == (self.motors.get_rel_left_speed(), self.motors.get_rel_right_speed()):
                self.last_measured_motors_speeds = (self.motors.get_rel_left_speed(), self.motors.get_rel_right_speed())
                self.motors_speed_label.config(text=" Left motor speed:   {0:7.0f}% \n"
                "Right motor speed: {1:7.0f}%".format(
                    int(100 * self.motors.get_rel_left_speed()),
                    int(100 * self.motors.get_rel_right_speed())))
            self.after(50, upadate_motor_speed_label)

        upadate_motor_speed_label()

        self.motors_speed_label.place(relheight=1, relwidth=1, relx=0, rely=0)
        self.speed_limit_widget.place(relheight=0.16, relwidth=.4, relx=0.3, rely=0)
        self.speed_limit_down_button.place(relheight=0.16, relwidth=.3, relx=0, rely=0)
        self.speed_limit_up_button.place(relheight=0.16, relwidth=.3, relx=0.7, rely=0)
        self.left_motor_speed_bar.place(relheight=0.6, relwidth=.2, relx=0.2, rely=0.25)
        self.right_motor_speed_bar.place(relheight=0.6, relwidth=.2, relx=0.6, rely=0.25)
        self.motors_speed_frame.place(relheight=0.1, relwidth=1, relx=0, rely=0.9)

    def create_right_frame(self):
        """
        This function creates panel which allows you to control pod.
        :return: None
        """
        self.frame_right = tk.Frame(root, bg="white")
        self.frame_right.place(relheight=1, relwidth=.2, relx=0.8)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=1)
        self.add_widgets_to_right_frame()

    def add_widgets_to_right_frame(self):
        """
        This function adds widgets to right frame.
        It sets widgets to control move, taking photos and videos.
        :return: None
        """
        self.video_button = ImgButton(self.frame_right, photo_file="icons/rec.png", action=self.video, scale=.5)
        self.video_button.place(relheight=0.3, relwidth=1, relx=0, rely=0.3)
        self.photo_button = ImgButton(self.frame_right, photo_file="icons/aparat5.png", action=self.photo, scale=.5)
        self.photo_button.bind("<ButtonRelease-1>", lambda event: self.photo_button.change_image("icons/aparat5.png"))
        self.photo_button.bind("<ButtonPress-1>", lambda event: self.photo_button.change_image("icons/aparat4.png"))
        self.photo_button.place(relheight=0.3, relwidth=1, relx=0, rely=0.0)
        self.joystick = Joysitck(self.motors, master=self.frame_right)
        self.joystick.place(relheight=0.4, relwidth=1, relx=0, rely=0.6)
        self.joystick.update()
        self.video_button.update()
        self.photo_button.update()

    def create_midle_frame(self):
        """
        This function creates frame which displays camera view.
        :return: None
        """
        self.frame_middle = tk.Frame(root, bg="blue")
        self.frame_middle.place(relheight=1, relwidth=.6, relx=.2)
        self.camera = Camera(self.frame_middle)
        self.camera.place(relheight=1, relwidth=1)
        self.camera.show_frames()
        self.camera.monitor_video_recording()

    def init_keyboard(self):
        """
        This function binds keyboard keys to functions.
        :return: None
        """
        def start_photo():
            self.photo_button.change_image("icons/aparat4.png")

        def end_photo():
            self.photo()
            self.photo_button.change_image("icons/aparat5.png")

        keys = {
            "up": (self.joystick.start, self.joystick.drive_forward, self.joystick.stop),
            "down": (self.joystick.start, self.joystick.drive_backward, self.joystick.stop),
            "left": (self.joystick.start, self.joystick.turn_left, self.joystick.stop),
            "right": (self.joystick.start, self.joystick.turn_right, self.joystick.stop),
            "e": (start_photo, None, end_photo),
            "r": (self.video, None, None),
            "w": (None, self.speed_limit_up, None),
            "s": (None, self.speed_limit_down, None)
        }
        self.keyboard.add_functions(keys)

        def update_keyboard():
            self.keyboard.update()
            self.after(5, update_keyboard)
        update_keyboard()

    def photo(self):
        """
        This function allows you to take photo.
        :return: None
        """
        print("pstryk")
        self.camera.take_photo()

    def video(self):
        """
        This function allows you to start and stop video.
        :return: None
        """
        self.video_button.click()
        if self.video_button.clicks % 2 == 1:
            self.video_button.change_image("icons/stop.png")
            self.camera.prepare_recording()
            self.camera.isrecording = True
        else:
            self.video_button.change_image("icons/rec.png")
            self.camera.isrecording = False
            self.camera.video_file.release()

    def speed_limit_up(self):
        """
        This function allows you to increase speed limit.
        :return: None
        """
        self.joystick.speed_limit += 0.01
        self.speed_limit_widget.config(text=f"Speed Limit:\n{int(self.joystick.speed_limit * 100)}%")

    def speed_limit_down(self):
        """
        This function allows you to decrease speed limit.
        :return: None
        """

        self.joystick.speed_limit -= 0.01
        self.speed_limit_widget.config(text=f"Speed Limit:\n{int(self.joystick.speed_limit * 100)}%")


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x700")
    app = MainApplication(root)
    app.place(relheight=1, relwidth=1)
    root.mainloop()
    app.camera.release()
    cv2.destroyAllWindows()





