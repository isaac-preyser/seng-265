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