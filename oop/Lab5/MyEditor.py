import tkinter as tk

class MyEditor(tk.Canvas):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, parent):
        if hasattr(self, '_initialized') and self._initialized:
            return
        super().__init__(parent, bg="white")
        self.parent = parent
        self.shapes = []
        self.highlighted_shape = None
        self.current_shape = None
        self.shape_class = None
        self.x_start = None
        self.y_start = None

        self.bind("<Button-1>", self.on_mouse_down)
        self.bind("<B1-Motion>", self.on_mouse_move)
        self.bind("<ButtonRelease-1>", self.on_mouse_up)
        parent.bind("<Control-z>", self.undo)

        self._initialized = True

    def on_mouse_down(self, event):
        if not self.shape_class:
            return
        self.x_start, self.y_start = event.x, event.y
        self.current_shape = self.shape_class(event.x, event.y, event.x, event.y, trail=True)
        if self.current_shape.name == "Point":
            self.end_draw(self.current_shape, event.x, event.y)
        self.redraw()

    def on_mouse_move(self, event):
        if not self.current_shape:
            return
        self.current_shape.x2, self.current_shape.y2 = event.x, event.y
        self.redraw()

    def on_mouse_up(self, event):
        if not self.current_shape:
            return
        finalized_shape = self.shape_class(self.x_start, self.y_start, event.x, event.y, trail=False)
        self.end_draw(finalized_shape, event.x, event.y)
        self.redraw()

    def end_draw(self, shape, x, y):
        self.shapes.append(shape)
        self.parent.on_shape_added(shape, self.x_start, self.y_start, x, y)
        self.x_start, self.y_start = None, None
        self.current_shape = None

    def redraw(self):
        self.delete("all")
        for shape in self.shapes:
            shape.draw(self)
        if self.current_shape:
            self.current_shape.draw(self)

    def clear(self):
        self.shapes = []
        self.redraw()

    def undo(self, event=None):
        if not self.shapes:
            return
        self.shapes.pop()
        self.redraw()
        self.parent.shapes_data.pop()
        if self.parent.table_window:
            self.parent.table_window.remove_last_row()

    def highlight_shape(self, shape_info):
        shape_name, x1, y1, x2, y2 = shape_info
        self.not_highlight()
        shape = next((s for s in self.shapes if s.get_coordinates() == (int(x1), int(y1), int(x2), int(y2))), None)
        if shape:
            self.highlighted_shape = shape
            shape.outline = "red"
            shape.draw(self)
    
    def not_highlight(self):
        if self.highlighted_shape:
            self.highlighted_shape.outline = "black"
            self.highlighted_shape.draw(self)
            self.highlighted_shape = None
        
    def delete_shape(self, shape_info):
        shape_name, x1, y1, x2, y2 = shape_info
        shape_to_delete = next((shape for shape in self.shapes if shape.get_coordinates() == (int(x1), int(y1), int(x2), int(y2))), None)
        if shape_to_delete:
            self.shapes.remove(shape_to_delete)
            self.delete_shapes_data((int(x1), int(y1), int(x2), int(y2)))
            self.highlighted_shape = None
            self.redraw()

    def delete_shapes_data(self, coordinates):
        shape_data_to_delete = next( (data for data in self.parent.shapes_data if data[1:] == coordinates), None )
        if shape_data_to_delete:
            self.parent.shapes_data.remove(shape_data_to_delete)

    def on_shape_loaded(self, name, x1, y1, x2, y2):
        shape_class = self.parent.button_data[name]["shape"]
        shape = shape_class(x1, y1, x2, y2, trail=False)
        self.shapes.append(shape)
        self.redraw()
        self.parent.on_shape_added(shape, x1, y1, x2, y2)