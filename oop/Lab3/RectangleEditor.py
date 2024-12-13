from Editor import Editor
from RectangleShape import RectangleShape

class RectangleEditor(Editor):

    def touch_start(self, x, y):
        self.x_start = x
        self.y_start = y

    def touch_move(self, x, y):
        radius_x = abs(x - self.x_start)
        radius_y = abs(y - self.y_start)
        if self.x_start is not None and self.y_start is not None:
            self.trail = RectangleShape(self.x_start - radius_x, self.y_start - radius_y, self.x_start + radius_x, self.y_start + radius_y, outline="red", fill="")

    def touch_up(self, x, y):
        radius_x = abs(x - self.x_start)
        radius_y = abs(y - self.y_start)
        if self.x_start is not None and self.y_start is not None:
            self.shapes.append(RectangleShape(self.x_start - radius_x, self.y_start - radius_y, self.x_start + radius_x, self.y_start + radius_y, outline="black", fill="grey"))
        self.trail = None

