from Editor import Editor
from EllipseShape import EllipseShape

class EllipseEditor(Editor):

    def touch_start(self, x, y):
        self.x_start = x
        self.y_start = y

    def touch_move(self, x, y):
        radius_x = abs(x - self.x_start)
        radius_y = abs(y - self.y_start)
        if self.x_start is not None and self.y_start is not None:
            self.trail = EllipseShape(self.x_start - radius_x, self.y_start - radius_y,  # Top-left corner
                                      self.x_start + radius_x, self.y_start + radius_y,  # Bottom-right corner
                                      outline="black", fill="")

    def touch_up(self, x, y):
        radius_x = abs(x - self.x_start)
        radius_y = abs(y - self.y_start)
        if self.x_start is not None and self.y_start is not None:
            self.shapes.append(EllipseShape(
                self.x_start - radius_x, self.y_start - radius_y,  # Top-left corner
                self.x_start + radius_x, self.y_start + radius_y,  # Bottom-right corner
                outline="black", fill="white"
            ))
        self.trail = None
