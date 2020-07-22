class MotorsController:
    def __init__(self):
        """
        This function allows you to communicate with physical motors.
        """
        self.left_motor = Motor()
        self.right_motor = Motor()

    def move_car(self, motors_speeds):
        """
        This function allows you to drive car using information about joystick.
        :return: None
        """
        self._update_motors_speeds(motors_speeds)
        self._move()

    def _update_motors_speeds(self, motors_speeds):
        relative_left_motor_speed, relative_right_motor_speed = motors_speeds
        self.left_motor.relative_speed = relative_left_motor_speed
        self.right_motor.relative_speed = relative_right_motor_speed

    def _move(self):
        """
        This function controls physical motor. You have to call it always when you want to change motors speed.
        :return: None
        """
        print("I'm driving")
        print("left wheel speed:", self.left_motor.speed)
        print("rigth wheel speed:", self.right_motor.speed)
        print("####################################")

    def set_motors_max_speed(self, new_max_speed):
        if not MotorsController.value_is_positive(new_max_speed):
            raise ValueError("Motor  max speed have to be positive")
        self.left_motor._max_speed = new_max_speed
        self.right_motor._max_speed = new_max_speed

    @staticmethod
    def value_is_positive(value):
        return value > 0

    def get_relative_left_motor_speed(self):
        return self.left_motor.relative_speed

    def get_relative_right_motor_speed(self):
        return self.right_motor.relative_speed
    
    
class Motor:
    def __init__(self, max_speed=480):
        self._speed = 0
        self._max_speed = max_speed
        
    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        if value < -self._max_speed:
            self._speed = -self._max_speed
        elif value > self._max_speed:
            self._speed = self._max_speed
        else:
            self._speed = value

    @property
    def relative_speed(self):
        return self.speed / self._max_speed

    @relative_speed.setter
    def relative_speed(self, relative_speed):
        self._speed = round(relative_speed * self._max_speed, 6)
        self._check_speed_value()

    def _check_speed_value(self):
        if not self._speed_have_property_type():
            raise TypeError("Motor speed must be int or float type")
        if self._speed_is_bigger_than_max_speed():
            raise ValueError(f"Motor speed have to be in range from {-self._max_speed} to {self._max_speed}"
                             f"\n {self._speed} given instead")

    def _speed_have_property_type(self):
        return isinstance(self._speed, (int, float))

    def _speed_is_bigger_than_max_speed(self):
        speed_is_in_range = -self._max_speed <= self._speed <= self._max_speed
        return not speed_is_in_range
