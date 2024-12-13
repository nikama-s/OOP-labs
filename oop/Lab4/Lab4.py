import tkinter as tk
from tkinter import Menu
from MyEditor import MyEditor
from Toolbar import Toolbar
from PointShape import PointShape
from LineShape import LineShape
from RectangleShape import RectangleShape
from EllipseShape import EllipseShape
from LineOOShape import LineOOShape
from CubeShape import CubeShape

class Lab4(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Shape Drawer")
        self.geometry("800x600")

        self.button_data = {
            "Point": {"shape": PointShape, "image": tk.PhotoImage(file = "images/point.png").subsample(3, 3), "tooltip": "Намалювати крапку"},
            "Line": {"shape": LineShape, "image": tk.PhotoImage(file = "images/line.png").subsample(3, 4), "tooltip": "Намалювати лінію"},
            "Rectangle": {"shape": RectangleShape, "image": tk.PhotoImage(file ="images/rectangle.png").subsample(3, 4), "tooltip": "Намалювати прямокутник"},
            "Ellipse": {"shape": EllipseShape, "image": tk.PhotoImage(file ="images/ellipse.png").subsample(3, 4), "tooltip": "Намалювати еліпс"},
            "LineOO": {"shape": LineOOShape, "image": tk.PhotoImage(file ="images/lineOO.png").subsample(4, 4), "tooltip": "Намалювати лінію з кружечками"},
            "Cube": {"shape": CubeShape, "image": tk.PhotoImage(file ="images/cube.png").subsample(3, 3), "tooltip": "Намалювати куб"},
        }

        self.toolbar = Toolbar(self, self.set_shape, self.button_data)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.shape_editor = MyEditor(self)
        self.shape_editor.pack(fill=tk.BOTH, expand=True)

        self.object_menu = None
        self.create_menu()


    def create_menu(self):
        menu_bar = Menu(self)
        self.config(menu=menu_bar)

        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Очистити", command=self.clear_editor)
        file_menu.add_command(label="Вийти", command=self.quit)

        self.object_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Об’єкти", menu=self.object_menu)
        for shape_name in self.button_data:
            self.object_menu.add_command(label=shape_name, command=lambda name=shape_name: self.set_shape(name))

        help_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Довідка", menu=help_menu)
        help_menu.add_command(label="Про програму")

    def set_shape(self, shape_type):
        self.shape_editor.shape_class = self.button_data[shape_type]["shape"]
        self.title(shape_type)
        self.toolbar.update_from_menu(shape_type)

    def clear_editor(self):
        self.shape_editor.destroy()
        self.shape_editor = MyEditor(self)
        self.shape_editor.pack(fill=tk.BOTH, expand=True)

        self.title("Shape Drawer")
        self.toolbar.reset_buttons()

if __name__ == "__main__":
    app = Lab4()
    app.mainloop()
