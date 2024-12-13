from abc import ABC, abstractmethod
class Editor(ABC):
    def __init__(self, shapes):
        self.shapes = shapes
        self.trail = None
        self.x_start = None
        self.y_start = None

    @abstractmethod
    def touch_start(self, x, y):
        pass

    @abstractmethod
    def touch_move(self, x, y):
        pass

    @abstractmethod
    def touch_up(self, x, y):
        pass
