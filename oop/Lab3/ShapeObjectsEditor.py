import tkinter as tk
from PointEditor import PointEditor
from LineEditor import LineEditor
from RectangleEditor import RectangleEditor
from EllipseEditor import EllipseEditor

class ShapeObjectsEditor(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.shapes = []
        self.current_editor = None

        self.editors = {
            "Point": PointEditor(self.shapes),
            "Line": LineEditor(self.shapes),
            "Rectangle": RectangleEditor(self.shapes),
            "Ellipse": EllipseEditor(self.shapes)
        }

        self.bind("<Button-1>", self.on_mouse_down)
        self.bind("<B1-Motion>", self.on_mouse_move)
        self.bind("<ButtonRelease-1>", self.on_mouse_up)

    def set_shape_type(self, shape_type):
        self.current_editor = self.editors.get(shape_type)

    def on_mouse_down(self, event):
        if self.current_editor:
            self.current_editor.touch_start(event.x, event.y)
        self.redraw()

    def on_mouse_move(self, event):
        if self.current_editor:
            self.current_editor.touch_move(event.x, event.y)
        self.redraw()

    def on_mouse_up(self, event):
        if self.current_editor:
            self.current_editor.touch_up(event.x, event.y)
        self.redraw()

    def redraw(self):
        self.delete("all")
        for shape in self.shapes:
            shape.draw(self)

        if self.current_editor and self.current_editor.trail:
            self.current_editor.trail.draw(self)

    def clear(self):
        self.shapes.clear()
        self.redraw()
