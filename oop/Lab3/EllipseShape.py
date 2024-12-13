from Shape import Shape

class EllipseShape(Shape):
    def __init__(self, x1, y1, x2, y2, outline="black", fill=""):
        super().__init__(outline, fill)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def draw(self, canvas):
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2, outline=self.outline, fill=self.fill, width=2)
