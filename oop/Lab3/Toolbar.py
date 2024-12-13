import tkinter as tk
from Tooltip import ToolTip


class Toolbar(tk.Frame):
    def __init__(self, parent, set_shape_callback):
        super().__init__(parent, bd=1, relief=tk.RAISED)
        self.set_shape_callback = set_shape_callback
        self.active_button = None
        self.buttons = {}

        self.point_image = tk.PhotoImage(file="images/point.png").subsample(3, 3)
        self.line_image = tk.PhotoImage(file="images/line.png").subsample(3, 4)
        self.rectangle_image = tk.PhotoImage(file="images/rectangle.png").subsample(3, 4)
        self.ellipse_image = tk.PhotoImage(file="images/ellipse.png").subsample(3, 4)

        self.create_toolbar()

    def create_toolbar(self):
        # Button for Point
        btn_point = tk.Button(self, image=self.point_image, command=lambda: self.on_button_click("Point", btn_point), width=50, height=30, borderwidth=2)
        btn_point.pack(side=tk.LEFT, padx=2, pady=2)
        ToolTip(btn_point, "Намалювати крапку")
        self.buttons["Point"] = btn_point

        # Button for Line
        btn_line = tk.Button(self, image=self.line_image, command=lambda: self.on_button_click("Line", btn_line), width=50, height=30, borderwidth=2)
        btn_line.pack(side=tk.LEFT, padx=2, pady=2)
        ToolTip(btn_line, "Намалювати лінію")
        self.buttons["Line"] = btn_line

        # Button for Rectangle
        btn_rectangle = tk.Button(self,  image=self.rectangle_image, command=lambda: self.on_button_click("Rectangle", btn_rectangle), width=50, height=30, borderwidth=2)
        btn_rectangle.pack(side=tk.LEFT, padx=2, pady=2)
        ToolTip(btn_rectangle, "Намалювати прямокутник")
        self.buttons["Rectangle"] = btn_rectangle

        # Button for Ellipse
        btn_ellipse = tk.Button(self, image=self.ellipse_image, command=lambda: self.on_button_click("Ellipse", btn_ellipse), width=50, height=30, borderwidth=2)
        btn_ellipse.pack(side=tk.LEFT, padx=2, pady=2)
        ToolTip(btn_ellipse, "Намалювати еліпс")
        self.buttons["Ellipse"] = btn_ellipse

    def on_button_click(self, shape_type, button):
        if self.active_button == button:
            return
        self.set_shape_callback(shape_type)
        self.update_button_state(button)

    def update_button_state(self, button):
        if self.active_button:
            self.active_button.config(bg="#f0f0f0", relief=tk.RAISED)
        self.active_button = button
        self.active_button.config(bg="#d8d8d8", relief=tk.SUNKEN)

    def update_from_menu(self, shape_type):
        button = self.buttons.get(shape_type)
        self.update_button_state(button)

    def pack_toolbar(self):
        self.pack(side=tk.TOP, fill=tk.X)