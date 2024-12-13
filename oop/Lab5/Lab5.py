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
from TableWindow import TableWindow
from tkinter import filedialog

class Lab5(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Shape Drawer")
        self.geometry("800x600")

        self.shapes_data = []

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

        self.table_window = None

        self.object_menu = None
        self.create_menu()

    def create_menu(self):
        menu_bar = Menu(self)
        self.config(menu=menu_bar)

        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Зберегти", command=self.save_shapes)
        file_menu.add_command(label="Відкрити", command=self.load_shapes)
        file_menu.add_command(label="Очистити", command=self.clear)
        file_menu.add_command(label="Вийти", command=self.quit)

        self.object_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Об’єкти", menu=self.object_menu)
        for shape_name in self.button_data:
            self.object_menu.add_command(label=shape_name, command=lambda name=shape_name: self.set_shape(name))

        table_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Таблиця", menu=table_menu)
        table_menu.add_command(label="Показати таблицю", command=self.show_table_window)
        table_menu.add_command(label="Приховати таблицю", command=self.hide_table_window)

        help_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Довідка", menu=help_menu)
        help_menu.add_command(label="Про програму")

    def show_table_window(self):
        if not self.table_window:
            self.create_table_window()
        else:
            self.table_window.deiconify()

    def hide_table_window(self):
        if self.table_window:
            self.shape_editor.not_highlight()
            self.table_window.withdraw()

    def create_table_window(self):
        self.table_window = TableWindow(self, self.shape_editor.highlight_shape, self.shape_editor.not_highlight, self.shape_editor.delete_shape, self.hide_table_window)
        for shape_data in self.shapes_data:
            self.table_window.add_row(*shape_data)

    def set_shape(self, shape_type):
        self.shape_editor.shape_class = self.button_data[shape_type]["shape"]
        self.title(shape_type)
        self.toolbar.update_from_menu(shape_type)

    def on_shape_added(self, shape, x1, y1, x2, y2):
        shape_data = (shape.name, x1, y1, x2, y2)
        self.shapes_data.append(shape_data)
        if self.table_window:
            self.table_window.add_row(shape.name, x1, y1, x2, y2)

    def save_shapes(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            self._write_shapes_to_file(file_path)

    def _write_shapes_to_file(self, file_path):
        with open(file_path, 'w') as file:
            for shape_data in self.shapes_data:
                line = '\t'.join(map(str, shape_data)) + '\n'
                file.write(line)

    def load_shapes(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.clear()
            self._load_shapes_from_file(file_path)

    def _load_shapes_from_file(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                shape_data = line.strip().split('\t')
                shape_data[1:5] = map(int, shape_data[1:5])
                self.shape_editor.on_shape_loaded(*shape_data)

    def clear(self):
        self.shape_editor.clear()
        self.shapes_data.clear()
        if self.table_window:
            self.table_window.clear_table()

if __name__ == "__main__":
    app = Lab5()
    app.mainloop()
