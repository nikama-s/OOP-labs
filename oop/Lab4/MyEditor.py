import tkinter as tk

class MyEditor(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.shapes = []
        self.current_shape = None
        self.shape_class = None
        self.x_start = None
        self.y_start = None

        self.bind("<Button-1>", self.on_mouse_down)
        self.bind("<B1-Motion>", self.on_mouse_move)
        self.bind("<ButtonRelease-1>", self.on_mouse_up)
        parent.bind("<Control-z>", self.undo)

    def set_shape_type(self, shape_class):
        self.shape_class = shape_class

    def on_mouse_down(self, event):
        if self.shape_class is None: return

        self.x_start, self.y_start = event.x, event.y
        self.current_shape = self.shape_class(event.x, event.y, event.x, event.y, trail=True)

        self.redraw()

    def on_mouse_move(self, event):
        if  self.current_shape:
            self.current_shape.x2, self.current_shape.y2 = event.x, event.y
            self.redraw()

    def on_mouse_up(self, event):
        if self.current_shape:
            finalized_shape = self.shape_class(self.x_start, self.y_start, event.x, event.y, trail=False)
            self.shapes.append(finalized_shape)
            self.current_shape = None
        self.x_start, self.y_start = None, None
        self.redraw()

    def redraw(self):
        self.delete("all")
        for shape in self.shapes:
            shape.draw(self)
        if self.current_shape:
            self.current_shape.draw(self)

    def undo(self, event=None):
        if self.shapes:
            self.shapes.pop()
            self.redraw()