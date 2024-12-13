from Editor import Editor
from PointShape import PointShape

class PointEditor(Editor):
    def touch_start(self, x, y):
        self.shapes.append(PointShape(x, y))

    def touch_move(self, x, y):
        pass
    def touch_up(self, x, y):
        pass