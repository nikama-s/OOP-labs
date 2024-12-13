from abc import ABC, abstractmethod
class Shape(ABC):
    def __init__(self, outline, fill, trail):
        self.outline = outline
        self.fill = fill
        self.trail = trail

    @abstractmethod
    def draw(self, canvas):
        raise NotImplementedError