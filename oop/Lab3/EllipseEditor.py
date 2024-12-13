from Editor import Editor
from EllipseShape import EllipseShape

class EllipseEditor(Editor):

    def touch_start(self, x, y):
        self.x_start = x
        self.y_start = y

    def touch_move(self, x, y):
        if self.x_start is not None and self.y_start is not None:
            self.trail = EllipseShape(self.x_start, self.y_start, x, y, outline="red", fill="")

    def touch_up(self, x, y):
        if self.x_start is not None and self.y_start is not None:
            self.shapes.append(EllipseShape( self.x_start, self.y_start, x, y, outline="black", fill=""))
        self.trail = None
