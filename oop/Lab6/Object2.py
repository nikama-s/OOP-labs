import tkinter as tk
import random
import math
import sys
import socket
import threading
import pyperclip

class RandomPointGenerator:
    def __init__(self, n_points, x_min, x_max, y_min, y_max):
        self.n_points = n_points
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.points = []

    def generate(self):
        self.points = [
            (random.randint(math.ceil(self.x_min), math.floor(self.x_max)),
             random.randint(math.ceil(self.y_min), math.floor(self.y_max)))
            for _ in range(self.n_points)
        ]
        pyperclip.copy(self.points)

    def as_text(self):
        return "\n".join(f"{i + 1}: {point}" for i, point in enumerate(self.points))

class Object2App:
    def __init__(self, root, x_offset = 100, y_offset = 100):
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.root = root
        self.root.title("Object2 Points Generator")
        self.root.geometry(f"500x400+{self.x_offset}+{self.y_offset}")
        self.generator = None

        self.text_widget = tk.Text(self.root, font=("Arial", 12), wrap="none", width=50, height=20)
        self.text_widget.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.text_widget.yview)
        scrollbar.pack(side="right", fill="y")
        self.text_widget.configure(yscrollcommand=scrollbar.set)

        threading.Thread(target=self.start_listening, daemon=True).start()

    def update_display(self):
        self.text_widget.configure(state="normal")
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert("1.0", f"Generated Points:\n\n{self.generator.as_text()}")
        self.text_widget.configure(state="disabled")

    def start_listening(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(('localhost', 65432))
            server_socket.listen()
            while True:
                conn, _ = server_socket.accept()
                with conn:
                    data = conn.recv(1024).decode('utf-8')
                    if data:
                        try:
                            n_points, x_min, x_max, y_min, y_max = map(float, data.split(','))
                            self.generator = RandomPointGenerator(int(n_points), x_min, x_max, y_min, y_max)
                            self.generator.generate()
                            self.update_display()
                            conn.sendall(str(self.x_offset+500).encode('utf-8'))
                        except ValueError:
                            print("Error")

if __name__ == "__main__":
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    x_offset = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    y_offset = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    if x_offset+500 > screen_width:
        x_offset = 0
    app = Object2App(root, x_offset, y_offset)
    root.mainloop()
