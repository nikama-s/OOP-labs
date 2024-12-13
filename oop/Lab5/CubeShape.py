from LineShape import LineShape
from RectangleShape import RectangleShape


class CubeShape(LineShape, RectangleShape):
    def __init__(self, x1, y1, x2, y2, trail=False, outline="black", fill=""):
        super().__init__(x1, y1, x2, y2, trail)
        self.outline = outline
        self.fill = fill
        self.name = "Cube"
        self.dash = (4, 2) if trail else None

    def draw(self, canvas,  x1=None, y1=None, x2=None, y2=None):

        height = abs(self.y2 - self.y1)
        offset = height / 3

        back_bottom_left = (round(self.x1 + offset), round(self.y1 - offset))
        back_bottom_right = (round(self.x2 + offset), round(self.y1 - offset))
        back_top_left = (round(self.x1 + offset), round(self.y2 - offset))
        back_top_right = (round(self.x2 + offset), round(self.y2 - offset))

        RectangleShape.draw(self, canvas, self.x1, self.y1, self.x2, self.y2, True)

        RectangleShape.draw(self, canvas, back_bottom_left[0], back_bottom_left[1], back_top_right[0], back_top_right[1], True)

        LineShape.draw(self, canvas, self.x1, self.y1, back_bottom_left[0], back_bottom_left[1])
        LineShape.draw(self, canvas, self.x2, self.y1, back_bottom_right[0], back_bottom_right[1])
        LineShape.draw(self, canvas,self.x1, self.y2, back_top_left[0], back_top_left[1])
        LineShape.draw(self, canvas,self.x2, self.y2, back_top_right[0], back_top_right[1])

    def get_coordinates(self):
        return self.x1, self.y1, self.x2, self.y2