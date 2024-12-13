from Editor import Editor
from RectangleShape import RectangleShape

class RectangleEditor(Editor):

    def touch_start(self, x, y):
        self.x_start = x
        self.y_start = y

    def touch_move(self, x, y):
        if self.x_start is not None and self.y_start is not None:
            self.trail = RectangleShape(self.x_start, self.y_start, x, y, outline="black", fill="")

    def touch_up(self, x, y):
        if self.x_start is not None and self.y_start is not None:
            self.shapes.append(RectangleShape(self.x_start, self.y_start, x, y, outline="black", fill="lightblue"))
        self.trail = None

