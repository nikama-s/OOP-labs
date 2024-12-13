from Shape import Shape

class PointShape(Shape):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, canvas):
        canvas.create_oval(self.x - 5, self.y - 5, self.x + 5, self.y + 5, fill="black")