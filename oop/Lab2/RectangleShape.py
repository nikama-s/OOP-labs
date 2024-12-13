from Shape import Shape

class RectangleShape(Shape):
    def __init__(self, x1, y1, x2, y2, outline="black", fill="lightblue"):
        super().__init__(outline, fill)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def draw(self, canvas):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline="black", fill=self.fill, width=2)
