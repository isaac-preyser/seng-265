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
