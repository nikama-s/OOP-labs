class Shape:
    def __init__(self, outline="black", fill="white"):
        self.outline = outline
        self.fill = fill

    def draw(self, canvas):
        raise NotImplementedError
