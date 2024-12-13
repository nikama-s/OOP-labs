import tkinter as tk
from tkinter import Menu
from ShapeObjectsEditor import ShapeObjectsEditor
from Toolbar import Toolbar

class Lab2(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Shape Drawer")
        self.geometry("800x600")

        self.toolbar = Toolbar(self, self.set_shape)
        self.toolbar.pack_toolbar()

        self.shape_editor = ShapeObjectsEditor(self)
        self.shape_editor.pack(fill=tk.BOTH, expand=True)

        self.object_menu = None
        self.create_menu()

    def create_menu(self):
        menu_bar = Menu(self)
        self.config(menu=menu_bar)

        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Очистити", command=self.shape_editor.clear)
        file_menu.add_command(label="Вийти", command=self.quit)

        self.object_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Об’єкти", menu=self.object_menu)
        self.object_menu.add_command(label="Крапка", command=lambda: self.set_shape("Point"))
        self.object_menu.add_command(label="Лінія", command=lambda: self.set_shape("Line"))
        self.object_menu.add_command(label="Прямокутник", command=lambda: self.set_shape("Rectangle"))
        self.object_menu.add_command(label="Еліпс", command=lambda: self.set_shape("Ellipse"))

        help_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Довідка", menu=help_menu)
        help_menu.add_command(label="Про програму")

    def set_shape(self, shape_type):
        self.shape_editor.set_shape_type(shape_type)
        self.title(shape_type)
        self.toolbar.update_from_menu(shape_type)

if __name__ == "__main__":
    app = Lab2()
    app.mainloop()
