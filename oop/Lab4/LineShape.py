from Shape import Shape

class LineShape(Shape):
    def __init__(self, x1=None, y1=None, x2=None, y2=None, trail=False, outline="black", fill="black"):
        super().__init__(outline, fill, trail)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.dash = (4, 2) if trail else None

    def draw(self, canvas,  x1=None, y1=None, x2=None, y2=None):
        x1, y1 = x1 if x1 is not None else self.x1, y1 if y1 is not None else self.y1
        x2, y2 = x2 if x2 is not None else self.x2, y2 if y2 is not None else self.y2

        canvas.create_line(x1, y1, x2, y2, fill=self.outline, width=2, dash=self.dash)
