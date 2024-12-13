import tkinter as tk
from tkinter import Menu
from ShapeObjectsEditor import ShapeObjectsEditor

class Lab2(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Shape Drawer")
        self.geometry("800x600")

        self.shape_editor = ShapeObjectsEditor(self)
        self.shape_editor.pack(fill=tk.BOTH, expand=True)

        self.shape_vars = {
            "point": tk.BooleanVar(value=False),
            "line": tk.BooleanVar(value=False),
            "rectangle": tk.BooleanVar(value=False),
            "ellipse": tk.BooleanVar(value=False),
        }
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
        self.object_menu.add_checkbutton(label="Крапка", variable=self.shape_vars["point"], command=lambda: self.set_shape("point"))
        self.object_menu.add_checkbutton(label="Лінія", variable=self.shape_vars["line"],command=lambda: self.set_shape("line"))
        self.object_menu.add_checkbutton(label="Прямокутник", variable=self.shape_vars["rectangle"],command=lambda: self.set_shape("rectangle"))
        self.object_menu.add_checkbutton(label="Еліпс", variable=self.shape_vars["ellipse"],command=lambda: self.set_shape("ellipse"))

        help_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Довідка", menu=help_menu)
        help_menu.add_command(label="Про програму")

    def set_shape(self, shape_type):
        for key in self.shape_vars:
            self.shape_vars[key].set(False)

        self.shape_vars[shape_type].set(True)

        self.shape_editor.set_shape_type(shape_type)

if __name__ == "__main__":
    app = Lab2()
    app.mainloop()
