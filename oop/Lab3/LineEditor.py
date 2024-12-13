from Editor import Editor
from LineShape import LineShape

class LineEditor(Editor):

    def touch_start(self, x, y):
        self.x_start = x
        self.y_start = y

    def touch_move(self, x, y):
        if self.x_start is not None and self.y_start is not None:
            self.trail = LineShape(self.x_start, self.y_start, x, y, outline="red")

    def touch_up(self, x, y):
        if self.x_start is not None and self.y_start is not None:
            self.shapes.append(LineShape(self.x_start, self.y_start, x, y))
        self.trail = None
