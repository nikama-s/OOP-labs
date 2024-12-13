from LineShape import LineShape
from EllipseShape import EllipseShape


class LineOOShape(LineShape, EllipseShape):
    def __init__(self, x1, y1, x2, y2, trail=False, outline="black", fill="pink", radius=15):
        super().__init__(x1, y1, x2, y2, trail)
        self.fill= "" if trail else fill
        self.outline = outline
        self.radius = radius
        self.name = "LineOO"
        self.dash = (4, 2) if trail else None

    def draw(self, canvas,  x1=None, y1=None, x2=None, y2=None):
        LineShape.draw(self, canvas)

        offset = self.radius

        EllipseShape.draw(self, canvas, self.x1 - offset, self.y1  - offset, self.x1  + offset, self.y1  + offset)
        EllipseShape.draw(self, canvas, self.x2 - offset, self.y2 - offset, self.x2 + offset, self.y2 + offset)

    def get_coordinates(self):
        return self.x1, self.y1, self.x2, self.y2