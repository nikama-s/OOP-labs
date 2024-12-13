from Shape import Shape

class LineShape(Shape):
    def __init__(self, x1, y1, x2, y2, outline="black"):
        super().__init__(outline)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def draw(self, canvas):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.outline, width=2)