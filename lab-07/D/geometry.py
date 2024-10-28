import math

class Point:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Point(%r, %r)" % (self.x, self.y)

    def delta_x(self, dx) -> 'Point':
        return Point(self.x + dx, self.y)
    
    def delta_y(self, dy) -> 'Point':
        return Point(self.x, self.y + dy)
    
    def translate(self, dx, dy) -> 'Point':
        return Point(self.x + dx, self.y + dy)
class Circle:

    def __init__(self, center=Point(), radius=0):
        self.center = center
        self.radius = radius

    def __repr__(self):
        return "Circle(%r, %r)" % (self.center, self.radius)

    def translate(self, dx, dy) -> 'Circle':
        return Circle(self.center.translate(dx, dy), self.radius)
    
    def perimeter(self) -> float:
        return 2 * math.pi * self.radius

    def area(self) -> float:
        return math.pi * self.radius ** 2
    

class Rectangle:
    
        def __init__(self, upper_left=Point(), lower_right=Point()):
            self.upper_left = upper_left
            self.lower_right = lower_right

        def __repr__(self) -> str:
            return "Rectangle(%r, %r)" % (self.upper_left, self.lower_right)
        
        def area(self) -> float:
            return abs((self.lower_right.x - self.upper_left.x) * abs(self.upper_left.y - self.lower_right.y))
        
        def perimeter(self) -> float:
            return 2 * (abs(self.lower_right.x - self.upper_left.x) + abs(self.upper_left.y - self.lower_right.y))
        
        def translate(self, dx, dy) -> 'Rectangle':
            return Rectangle(self.upper_left.translate(dx, dy), self.lower_right.translate(dx, dy))
                             