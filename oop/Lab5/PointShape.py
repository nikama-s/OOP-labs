from Shape import Shape

class PointShape(Shape):
    def __init__(self, x1, y1, x2=None, y2=None, outline="black", fill = "black", trail=False):
        super().__init__(outline, fill, trail)
        self.x = x1
        self.y = y1
        self.name = "Point"
    def draw(self, canvas):
        canvas.create_oval(self.x - 5, self.y - 5, self.x + 5, self.y + 5, fill=self.outline)

    def get_coordinates(self):
        return self.x, self.y, self.x, self.y