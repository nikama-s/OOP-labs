import tkinter as tk
import pyperclip
import socket
import sys
import threading
import ast

class GraphPlotter:
    def __init__(self, x_offset = 100, y_offset = 100, points=None):
        self.points = sorted(points or [], key=lambda p: p[0])
        self.canvas_width = 550
        self.canvas_height = 450
        self.margin = 60
        self.root = None
        self.canvas = None
        self.normalized_points = []
        self.min_range = 1
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.hover_label = None

    def _normalize_point(self, x, y, min_x, max_x, min_y, max_y):
        norm_x = self.margin + (x - min_x) / (max_x - min_x) * (self.canvas_width - 2 * self.margin)
        norm_y = self.canvas_height - self.margin - (y - min_y) / (max_y - min_y) * (self.canvas_height - 2 * self.margin)
        return norm_x, norm_y

    def _on_mouse_move(self, event):
        if not self.normalized_points:
            return
        for i, (x, y) in enumerate(self.normalized_points):
            if abs(event.x - x) < 5 and abs(event.y - y) < 5:
                self.place_label(x, y, i)
                return
        if self.hover_label:
            self.canvas.delete(self.hover_label)
            self.hover_label = None

    def place_label(self, x, y, i):
        if not self.hover_label:
            self.hover_label = self.canvas.create_text(
                x + 10, y - 10,
                text=f"{self.points[i]}",
                font=("Arial", 10),
                fill="darkgreen",
                anchor="w"
            )
        else:
            self.canvas.coords(self.hover_label, x + 10, y - 10)
            self.canvas.itemconfig(self.hover_label, text=f"{self.points[i]}")

    def draw_graph(self):
        if not self.points:
            return

        min_x, max_x = (f(p[0] for p in self.points) for f in (min, max))
        min_y, max_y = (f(p[1] for p in self.points) for f in (min, max))

        for coord_min, coord_max in ((min_x, max_x), (min_y, max_y)):
            if coord_max - coord_min < self.min_range:
                mid = (coord_min + coord_max) / 2
                coord_min, coord_max = mid - self.min_range / 2, mid + self.min_range / 2

        min_x, max_x = min(min_x, 0), max(max_x, 0)
        min_y, max_y = min(min_y, 0), max(max_y, 0)

        x_axis_y = self.canvas_height - self.margin - (0 - min_y) / (max_y - min_y) * (self.canvas_height - 2 * self.margin)
        y_axis_x = self.margin + (0 - min_x) / (max_x - min_x) * (self.canvas_width - 2 * self.margin)

        self.canvas.delete("all")

        self.draw_axis(x_axis_y, y_axis_x)

        self.draw_marks(min_x, max_x, min_y, max_y, x_axis_y, y_axis_x)

        self.normalized_points = [self._normalize_point(x, y, min_x, max_x, min_y, max_y) for x, y in self.points]
        for i in range(len(self.normalized_points)):
            x, y = self.normalized_points[i]
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")
            if i > 0:
                prev_x, prev_y = self.normalized_points[i - 1]
                self.canvas.create_line(prev_x, prev_y, x, y, fill="black", width=2)

    def draw_axis(self, x_axis_y, y_axis_x):
        self.canvas.create_line(self.margin, x_axis_y, self.canvas_width - self.margin, x_axis_y, arrow=tk.LAST,width=2)
        self.canvas.create_line(y_axis_x, self.canvas_height - self.margin, y_axis_x, self.margin, arrow=tk.LAST,width=2)
        self.canvas.create_text(self.canvas_width - self.margin + 15, x_axis_y + 10, text="X", font=("Arial", 12),fill="black")
        self.canvas.create_text(y_axis_x - 10, self.margin - 15, text="Y", font=("Arial", 12), fill="black")
        self.canvas.create_text(y_axis_x - 10, x_axis_y + 15, text="O", font=("Arial", 12), fill="black")

    def draw_marks(self, min_x, max_x, min_y, max_y, x_axis_y, y_axis_x):
        x_step = (max_x - min_x) / 10
        for i in range(11):
            x_val = round(min_x + i * x_step, 2)
            x_canvas = self.margin + i * (self.canvas_width - 2 * self.margin) / 10
            self.canvas.create_line(x_canvas, x_axis_y - 5, x_canvas, x_axis_y + 5)
            self.canvas.create_text(x_canvas, x_axis_y + 20, text=f"{x_val}", font=("Arial", 10))

        y_step = (max_y - min_y) / 10
        for i in range(11):
            y_val = round(min_y + i * y_step, 2)
            y_canvas = self.canvas_height - self.margin - i * (self.canvas_height - 2 * self.margin) / 10
            self.canvas.create_line(y_axis_x - 5, y_canvas, y_axis_x + 5, y_canvas)
            self.canvas.create_text(y_axis_x - 20, y_canvas, text=f"{y_val}", font=("Arial", 10))

    def update_points(self, new_points):
        self.points = sorted(new_points, key=lambda p: p[0])
        self.draw_graph()

    def show_graph(self):
        root = tk.Tk()
        root.title("Object3 Graph Plotter")
        screen_width = root.winfo_screenwidth()
        if self.x_offset + 500 > screen_width:
            self.x_offset = 0
        root.geometry(f"550x450+{self.x_offset}+{self.y_offset}")
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()
        self.canvas.bind("<Motion>", self._on_mouse_move)
        self.draw_graph()
        root.mainloop()

def start_listening(plotter):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('localhost', 65433))
        server_socket.listen()
        while True:
            conn, _ = server_socket.accept()
            with conn:
                data = conn.recv(1024).decode('utf-8')
                if data == "1":
                    try:
                        clipboard_data = pyperclip.paste()
                        points = ast.literal_eval(clipboard_data)
                        if isinstance(points, list) and all(isinstance(i, tuple) and len(i) == 2 for i in points):
                            plotter.update_points(points)
                            conn.sendall(b"End")
                        pyperclip.copy("")
                    except Exception as e:
                        print(f"Error updating graph: {e}")

if __name__ == "__main__":
    x_offset = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    y_offset = int(sys.argv[2]) if len(sys.argv) > 2 else 100

    plotter = GraphPlotter(x_offset, y_offset)
    threading.Thread(target=start_listening, args=(plotter,), daemon=True).start()
    plotter.show_graph()




