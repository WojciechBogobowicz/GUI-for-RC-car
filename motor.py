from Coordinates import Coordinates


class Motors:
    def __init__(self):
        """
        This function allows you to communicate with physical motors.
        """
        self._left_speed = 0
        self._right_speed = 0
        self.max_speed = 480
        self._joistick_pos = Coordinates(0, 0)

    @property
    def left_speed(self):
        return self._left_speed

    @left_speed.setter
    def left_speed(self, value):
        if value < -self.max_speed:
            self._left_speed = -self.max_speed
        elif value > self.max_speed:
            self._left_speed = self.max_speed
        else:
            self._left_speed = value

    @property
    def right_speed(self):
        return self._right_speed

    @right_speed.setter
    def right_speed(self, value):
        if value < -self.max_speed:
            self._right_speed = -self.max_speed
        elif value > self.max_speed:
            self._right_speed = self.max_speed
        else:
            self._right_speed = value

    def get_rel_left_speed(self):
        """
        Calculates relative speed from range -1, 1. Where 1 is max motor speed and -1 is max speed in opposite direction.
        :return: relative left motor speed (percent of speed - float from -1 to 1).
        """
        return self.left_speed / self.max_speed

    def get_rel_right_speed(self):
        """
        Calculates relative speed from range -1, 1. Where 1 is max motor speed and -1 is max speed in opposite direction.
        :return: relative right motor speed (percent of speed - float from -1 to 1).
        """
        return self.right_speed / self.max_speed

    def move(self):
        """
        This function controls physical motor. You have to call it always when you want to change motors speed.
        :return: None
        """
        if not (-self.max_speed <= self.left_speed <= self.max_speed or
                -self.max_speed <= self.right_speed <= self.max_speed):
            raise ValueError(f"Speed limit exceeded: "
                             f"\n left motors {self.left_speed} "
                             f"\n right motors {self.right_speed}"
                             f"\n avaliable max speed {self.max_speed}")
        print("I'm driving")
        print("left wheel speed:", self.left_speed)
        print("rigth wheel speed:", self.right_speed)
        print("####################################")

    def update_motors(self, stick_position, start_point, joystick_range):
        """
        This function reads information from joystick about its position and updates motors speeds basing on
        read data.
        :param stick_position: Coordinates obj with current stick position.
        :param start_point: Coordinates obj with starting stick position.
        :param joystick_range: Maximum distance between stick position and start point.
        :return: None
        """
        self._joistick_pos = stick_position - start_point
        self._joistick_pos.x = self._joistick_pos.x / joystick_range
        self._joistick_pos.y = self._joistick_pos.y / joystick_range
        self._calculate_speed()

    def _calculate_speed(self):
        """
        This function translates joystick position to motors speeds and updates them.
        :return: None
        """
        turn, forward = self._joistick_pos.tuple
        signed_square = lambda x: x * abs(x)
        signed_sqrt = lambda x: -(-x) ** .5 if x < 0 else x ** .5
        self.left_speed = (signed_sqrt(signed_square(-forward) + signed_square(turn)))*self.max_speed
        self.right_speed = (signed_sqrt(signed_square(-forward) - signed_square(turn)))*self.max_speed

    def drive_car(self, stick_position, start_point, joystick_range):
        """
        This function allows you to drive car using information about joystick.
        :param stick_position: Coordinates obj with current stick position.
        :param start_point: Coordinates obj with starting stick position.
        :param joystick_range: Maximum distance between stick position and start point.
        :return: None
        """
        self.update_motors(stick_position, start_point, joystick_range)
        self.move()