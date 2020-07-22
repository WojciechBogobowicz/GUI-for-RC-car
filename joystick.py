from Geometry import Coordinates, Circle
import tkinter as tk
from motor import MotorsController


class Joysitck(tk.Canvas):
    def __init__(self, motors, master):
        """
        Joystick is graphic obj, which gives you possibility to control motors by mouse or
        build in functions.
        :param motors: Motors obj, which is controlled by joystick.
        :param master: Frame where joystick will be placed.
        """
        super().__init__(master, bg="grey")
        self.configure(width=800, height=600)
        self._motors = motors
        self._start_joystick_position = Coordinates(self.winfo_width() // 2, self.winfo_height() // 2)
        self._actual_joystick_position = self._start_joystick_position
        self.master.bind("<Configure>", self.handle_resize, add="+")
        self.bind("<ButtonRelease-1>", self.close_joystick)
        self.bind('<B1-Motion>', self.callback, '+')
        self._joystick_head_radius = self.winfo_width()
        self._joystick_bottom_radius = self._joystick_head_radius*1.3
        self._joystick_head = self.create_oval(0, 0, 0, 0, fill="#5E5D5D")
        self._joystick_bottom = self.create_oval(0, 0, 0, 0, fill="#443C3C")
        self.tag_raise(self._joystick_head)
        self._relative_joystick_size = 0.5
        self._turn = 0
        self._forward = 0
        self._keys_pressed = 0
        self._speed_limit = 0.5
        self._boost = 0.05

    def callback(self, event):
        """
        This function determinates joystick behavior, when it is dragged.
        :param event: event tkinter.Event obj
        :return: None
        """
        self._set_new_joystick_position(event.x, event.y)
        self._update_joystick_head_position_on_canvas()
        motors_speeds = self._translate_stick_position_to_motor_speed()
        self._motors.move_car(motors_speeds)

    def _set_new_joystick_position(self, x, y):
        """
        This function get new joystick head position.
        :param x: potential new horizontal position of joystick head center
        :param y: potential new vertical position of joystick head center
        :return: updated joystick position
        """
        dst_to_start = Coordinates(x, y).dist_to(self._start_joystick_position)
        current_max_dist = self._joystick_bottom_radius*self.speed_limit
        expected_new_position = Coordinates(x, y)
        if dst_to_start <= current_max_dist:
            self._actual_joystick_position = expected_new_position
        else:
            furthest_point_in_expected_direction = self._start_joystick_position.move(expected_new_position, current_max_dist)
            self._actual_joystick_position = furthest_point_in_expected_direction
        return self._actual_joystick_position

    def _update_joystick_head_position_on_canvas(self):
        """
        This function draws joystick with new position, on canvas.
        :return: None
        """
        draw_obj_in_new_position = self.coords
        joystick_head_circle = Circle(self._actual_joystick_position, self._joystick_head_radius)
        joystick_bottom_circle = Circle(self._start_joystick_position, self._joystick_bottom_radius)

        draw_obj_in_new_position(self._joystick_head, joystick_head_circle.get_spanning_points())
        draw_obj_in_new_position(self._joystick_bottom, joystick_bottom_circle.get_spanning_points())
        
    def _translate_stick_position_to_motor_speed(self):
        """
        This function translates joystick position to motors speeds and updates them.
        :return: None
        """
        centred_stick_position = self._actual_joystick_position-self._start_joystick_position
        relative_joystick_position = self._get_relative_joystick_position(centred_stick_position)
        motors_speeds = Joysitck._get_motors_speeds(relative_joystick_position)
        return motors_speeds

    def _get_relative_joystick_position(self, joystick_position):
        turn, forward = joystick_position
        relative_turn = turn / self._joystick_bottom_radius
        relative_forward = forward / self._joystick_bottom_radius
        return relative_turn, relative_forward

    @staticmethod
    def _get_motors_speeds(joystick_position):
        signed_square = lambda x: x * abs(x)
        signed_sqrt = lambda x: -(-x) ** .5 if x < 0 else x ** .5

        turn, forward = joystick_position
        left_motor_speed = (signed_sqrt(signed_square(-forward) + signed_square(turn)))
        right_motor_speed = (signed_sqrt(signed_square(-forward) - signed_square(turn)))
        return left_motor_speed, right_motor_speed

    def close_joystick(self, event):
        """
        This function resets joystick head position to joystick centre.
        :param event: tkinter.Event obj
        :return: None
        """
        no_speed_on_both_motors = 0, 0
        self._return_joystick_to_center()
        self._motors.move_car(no_speed_on_both_motors)

    def _return_joystick_to_center(self):
        self._actual_joystick_position = self._start_joystick_position
        self._update_joystick_head_position_on_canvas()

    def place(self, relheight=0, relwidth=0, relx=0, rely=0):
        super().place(relheight=relheight, relwidth=relwidth, relx=relx, rely=rely)
        self._relative_joystick_size = self._relative_joystick_size * min(relheight, relwidth)
        self._return_joystick_to_center()

    def update(self):
        """
        This function updates joystick head position on canvas.
        :return: None
        """
        super(Joysitck, self).update()
        self._update_start_position()
        self._update_joystick_size()
        self._update_joystick_head_position_on_canvas()

    def _update_start_position(self):
        self._start_joystick_position = Coordinates(self.winfo_width() // 2, self.winfo_height() // 2)

    def _update_joystick_size(self):
        shorter_screen_edge = min(self.winfo_width(), self.winfo_height())
        self._joystick_head_radius = shorter_screen_edge * self._relative_joystick_size
        joystick_bottom_to_head_ratio = 1.3
        self._joystick_bottom_radius = self._joystick_head_radius * joystick_bottom_to_head_ratio

    def handle_resize(self, event):
        """
        This function corrects size of joystick, when window size changed.
        :param event: is obj type tkinter.Event
        :return: None
        """
        self.update()
        self._return_joystick_to_center()

    def push_left(self):
        """
        This function allows to move joystick left without using mouse.
        :return: None
        """
        excepted_turn_speed = self._turn - self._joystick_bottom_radius*self.boost
        min_turn_speed = -self._joystick_bottom_radius*self._speed_limit
        self._turn = max(excepted_turn_speed, min_turn_speed)
        self._actual_joystick_position += Coordinates(self._turn, self._forward)
        self.callback(self._actual_joystick_position)

    def push_right(self):
        """
        This function allows to move joystick right without using mouse.
        :return: None
        """
        excepted_turn_speed = self._turn + self._joystick_bottom_radius*self.boost
        max_turn_speed = self._joystick_bottom_radius*self._speed_limit
        self._turn = min(excepted_turn_speed, max_turn_speed)
        self._actual_joystick_position += Coordinates(self._turn, self._forward)
        self.callback(self._actual_joystick_position)

    def push_forward(self):
        """
        This function allows to move joystick forward without using mouse.
        :return: None
        """
        excepted_forward_speed = self._forward - self._joystick_bottom_radius*self.boost
        min_forward_speed = -self._joystick_bottom_radius*self._speed_limit
        self._forward = max(excepted_forward_speed, min_forward_speed)
        self._actual_joystick_position += Coordinates(self._turn, self._forward)
        self.callback(self._actual_joystick_position)

    def push_backward(self):
        """
        This function allows to move joystick backward without using mouse.
        :return: None
        """
        excepted_forward_speed = self._forward + self._joystick_bottom_radius * self.boost
        max_forward_speed = self._joystick_bottom_radius*self._speed_limit
        self._forward = min(excepted_forward_speed, max_forward_speed)
        self._actual_joystick_position += Coordinates(self._turn, self._forward)
        self.callback(self._actual_joystick_position)

    def start_moving(self):
        """
        Start and stop moving functions:
        -start_moving function increases number of currently pressed keys used to navigate car.
        -stop_moving function decreases this number, and returns joystick to start position if there is no pressed key.
        :return: None
        """
        self._keys_pressed += 1

    def stop_moving(self):
        """
        Start and stop moving functions:
        -start_moving function increases number of currently pressed keys used to navigate car.
        -stop_moving function decreases this number, and returns joystick to start position if there is no pressed key.
        :return: None
        """
        self._keys_pressed -= 1
        if self._keys_pressed == 0:
            self._turn = 0
            self._forward = 0
            self.callback(self._start_joystick_position)

    @property
    def boost(self):
        return self._boost

    @boost.setter
    def boost(self, value):
        if value < 0:
            self._boost = 0
        elif value > 1:
            self._boost = 1
        else:
            self._boost = value

    @property
    def speed_limit(self):
        return self._speed_limit

    @speed_limit.setter
    def speed_limit(self, value):
        if value < 0:
            self._speed_limit = 0
        elif value > 1:
            self._speed_limit = 1
        else:
            self._speed_limit = value





