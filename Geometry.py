from math import atan, pi, sin, cos, asin, tan, acos


class Coordinates:
    def __init__(self, x, y):
        """
        This class represents position of the point on the screen.
        (0; 0) point is in top left corner of the screen.
        :param x: Horizontal position.
        :param y: Vertical position.
        """
        self.x = x
        self.y = y
        #if False in map(lambda cor: isinstance(cor, int) or isinstance(cor, float), (x, y)):
        if not self._coordinates_have_property_types():
            raise ValueError("Coordinates need to be int or float type.")

    def _coordinates_have_property_types(self):
        x_have_property_type = isinstance(self.x, (int, float))
        y_have_property_type = isinstance(self.y, (int, float))
        return x_have_property_type and y_have_property_type

    def __str__(self):
        """
        This function gives string representation of point in format (x; y).
        :return: String representation of point.
        """
        return f"({self.x}; {self.y})"

    def __add__(self, other):
        """
        This function implements addition of two Coordinates objects without changing self and other.
        :param other: Coordinates obj that you want to add.
        :return: Coordinate obj, whith is sum of two Coordinates objects.
        """
        return Coordinates(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """
        This function implements substraction of two Coordinates objects without changing self and other.
        :param other: Coordinates obj that you want to substract.
        :return: Coordinate obj, which is difference of two other Coordinates objects.
        """
        return Coordinates(self.x - other.x, self.y - other.y)

    def __abs__(self):
        """
        This function calculates module.
        :return: Float, module.
        """
        return (self.x ** 2 + self.y ** 2) ** (1 / 2)

    def __neg__(self):
        """
        This function returns point with opposite coordinates.
        :return: Coordinates obj.
        """
        return Coordinates(-self.x, -self.y)

    def __eq__(self, other):
        """
        This function checks if two objects have the same coordinates.
        :param other: Coordinate obj that you want to compare,
        :return: Bool - true if both objects have the same coordinates.
        """
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def __iter__(self):
        #return (self.__dict__[item] for item in 'xy')
        return (i for i in (self.x, self.y))

    def dist_to(self, other):
        """
        This function calculates distance to other Coordinate obj.
        :param other: Coordinate obj.
        :return: Float - dist between two obj.
        """
        return abs(self-other)

    def in_ball(self, r, other):
        """
        This function checks if dist to other Coordinate obj is smaller than r (self is in ball of radius r and center in other).
        :param r: Float - ball radius, checking distance.
        :param other: Coordinates obj. - center of ball.
        :return: Bool - True if dist to other is smaller than r.
        """
        return other.dist_to(self) < r

    def get_alpha(self):
        """
        This function calculates angle between vector from (0,0) to (self.x, self.y) and OX.
        :return: Float. Angle in radians.
        """
        if self.x == 0 and self.y == 0:
            raise ValueError("Point (0,0) doesn't have any angle")
        if self.x == 0:
            return self._calculate_angle_for_vertical_vector()
        alpha = atan(self.y/self.x)
        if self.x <= 0:
            alpha += pi
        return alpha

    def _calculate_angle_for_vertical_vector(self):
        if self.y > 0:
            return pi / 2
        elif self.y < 0:
            return (3 / 2) * pi

    def move(self, direction_point, dst):
        """
        This function allows you to move point by dst in other point direction.
        :param direction_point: Coordinates obj - point which is used to determinate move
         direction.
        :param dst: Float - distance by which you want to move self.
        :return: New Coordinates obj with new coordinates.
        """
        if self == direction_point:
            return self
        alpha = (direction_point-self).get_alpha()
        x = self.x + cos(alpha) * dst
        y = self.y + sin(alpha) * dst
        return Coordinates(x, y)

    def _get_tuple(self):
        return self.x, self.y

    def _set_tuple(self, pos):
        self.x, self.y = pos

    tuple = property(_get_tuple, _set_tuple)


class Circle:
    def __init__(self, center, radius):
        """
        Algebraic representation of circle.
        :param center: Coordinates obj
        :param radius: Float
        """
        if radius < 0:
            raise ValueError("Radius can")
        self.center = center
        self.radius = radius

    def get_spanning_points(self):
        left_bottom_point_x = self.center.x - self.radius
        left_bottom_point_y = self.center.y - self.radius
        right_top_point_x = self.center.x + self.radius
        right_top_point_y = self.center.y + self.radius
        return left_bottom_point_x, left_bottom_point_y, right_top_point_x, right_top_point_y



if __name__ == "__main__":
    p1 = Coordinates(3, 1)
    p2 = Coordinates(4, 5)
    print(p1.move(Coordinates(2, 0), 2**.5))
    print(*p1)
