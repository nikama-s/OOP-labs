from Shape import Shape

class RectangleShape(Shape):
    def __init__(self, x1=None, y1=None, x2=None, y2=None, trail=False, outline="black", fill="grey"):
        super().__init__(outline, fill, trail)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.name = "Rectangle"
        self.fill = "" if trail else fill
        self.dash = (4, 2) if trail else None


    def draw(self, canvas,  x1=None, y1=None, x2=None, y2=None, corner_to_corner=False):
        x1, y1 = x1 if x1 is not None else self.x1, y1 if y1 is not None else self.y1
        x2, y2 = x2 if x2 is not None else self.x2, y2 if y2 is not None else self.y2

        radius_x, radius_y = abs(x2 - x1), abs(y2 - y1)
        x1, y1, x2, y2 = (
            (x1, y1, x2, y2) if corner_to_corner else (x1 - radius_x, y1 - radius_y, x1 + radius_x, y1 + radius_y)
        )

        canvas.create_rectangle( x1, y1, x2, y2, outline=self.outline, fill=self.fill, width=2, dash=self.dash)

    def get_coordinates(self):
        return self.x1, self.y1, self.x2, self.y2