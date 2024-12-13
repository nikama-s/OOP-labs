import time
import tkinter as tk
from tkinter import messagebox
import pygetwindow as gw
import subprocess
import socket
from tkinter import ttk

class InputParameterApp:
    def __init__(self, root):
        self.root = root
        self.program_address_first = ('localhost', 65432)
        self.program_address_second = ('localhost', 65433)

        self.nPoint_entry = None
        self.xMin_entry = None
        self.xMax_entry = None
        self.yMin_entry = None
        self.yMax_entry = None

        self.setup_ui()

    def setup_ui(self):
        self.root.title("Input Parameters")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(False, False)

        title = tk.Label(self.root, text="Enter Parameters", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333")
        title.pack(pady=10)

        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(pady=10)

        self.create_input_row(frame, "nPoint:", 0)
        self.create_input_row(frame, "xMin:", 1)
        self.create_input_row(frame, "xMax:", 2)
        self.create_input_row(frame, "yMin:", 3)
        self.create_input_row(frame, "yMax:", 4)

        tk.Button(self.root, text="Submit", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                  command=self.on_submit).pack(pady=20)

    def clear_entries(self):
        for entry_name in ["nPoint_entry", "xMin_entry", "xMax_entry", "yMin_entry", "yMax_entry"]:
            entry = getattr(self, entry_name)
            entry.delete(0, tk.END)

    def create_input_row(self, frame, label, row):
        lbl = tk.Label(frame, text=label, font=("Arial", 12), bg="#f0f0f0", fg="#333")
        lbl.grid(row=row, column=0, padx=10, pady=5, sticky="e")

        entry = ttk.Entry(frame, font=("Arial", 12))
        entry.grid(row=row, column=1, padx=10, pady=5, sticky="w")
        setattr(self, f"{label[:-1]}_entry", entry)

    def terminate_processes(self, title):
        for window in gw.getWindowsWithTitle(title):
            try:
                window.close()
            except Exception:
                pass

    def is_program_running(self, name):
        return bool(gw.getWindowsWithTitle(name))

    def on_submit(self):
        try:
            nPoint, xMin, xMax, yMin, yMax = self.get_inputs()
            self.validate_inputs(nPoint, xMin, xMax, yMin, yMax)

            width, x, y = self.get_geometry()
            self.check_launch_process("Object2 Points Generator", "Object2.py", str(x + width + 10), str(y))

            self.send_to_program(self.program_address_first, f"{nPoint},{xMin},{xMax},{yMin},{yMax}")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def get_inputs(self):
        return (
            int(self.nPoint_entry.get()),
            float(self.xMin_entry.get()),
            float(self.xMax_entry.get()),
            float(self.yMin_entry.get()),
            float(self.yMax_entry.get())
        )

    def validate_inputs(self, nPoint, xMin, xMax, yMin, yMax):
        if nPoint <= 0:
            raise ValueError("Number of points (nPoint) must be greater than 0.")
        if xMin >= xMax:
            raise ValueError("xMin must be less than xMax.")
        if yMin >= yMax:
            raise ValueError("yMin must be less than yMax.")

    def check_launch_process(self, name, script, offset_x, offset_y):
        if not self.is_program_running(name):
            subprocess.Popen(["python", script, offset_x, offset_y])

    def get_geometry(self):
        geometry = self.root.geometry()
        width, height, x, y = map(int, geometry.replace("x", "+").split("+"))
        return width, x, y

    def send_to_program(self, program, data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            while True:
                try:
                    client_socket.connect(program)
                    client_socket.sendall(data.encode('utf-8'))

                    response = client_socket.recv(1024).decode('utf-8')
                    if response == "End":
                        self.root.focus_force()
                        self.clear_entries()
                    elif response and program == self.program_address_first:
                        _, _, y = self.get_geometry()
                        self.check_launch_process("Object3 Graph Plotter", "Object3.py", str(int(response)+10), str(y))
                        self.send_to_program(self.program_address_second, "1")
                    break

                except ConnectionRefusedError:
                    time.sleep(1)

    def close(self):
        self.terminate_processes("Object2 Points Generator")
        self.terminate_processes("Object3 Graph Plotter")
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = InputParameterApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()





