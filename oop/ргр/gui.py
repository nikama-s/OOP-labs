import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import ttkthemes
from edit_classes_window import EditClassesWindow
from edit_connections_window import EditConnectionsWindow

class GUI:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, root, ClassAnalyzer, UMLDiagram, ClassManager):
        if not hasattr(self, "initialized"):
            self.initialized = True
            self.root = root
            self.analyzer = ClassAnalyzer
            self.uml_diagram = UMLDiagram
            self.class_manager = ClassManager
            self.shortened_details = True
            self.edit_classes_window_opened = False
            self.edit_connections_window_opened = False
            self.setup_gui()

    def setup_gui(self):
        self.root.title("UML Class Diagram Generator")
        self.root.geometry("1000x700")
        self.root.minsize(700, 500)

        style = ttkthemes.ThemedStyle(self.root)
        style.set_theme("vista")
        style.configure("TButton", font=("Helvetica", 10, "bold"), padding=6)
        style.configure("TScrollbar", arrowcolor="lightgray", troughcolor="lightgray", background="gray", bordercolor="gray")

        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(self.frame, bg="white")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.v_scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")

        self.h_scrollbar = ttk.Scrollbar(self.frame, orient="horizontal", command=self.canvas.xview)
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")

        self.canvas.configure(xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)

        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(fill="x", padx=10, pady=10)

        self.create_buttons()

    def create_buttons(self):
        ttk.Button(self.button_frame, text="Select Folder", command=self.select_folder, width=6).pack(side="left", padx=5,fill="x", expand=True)
        ttk.Button(self.button_frame, text="Select File", command=self.select_file, width=6).pack(side="left", padx=5,fill="x", expand=True)
        ttk.Button(self.button_frame, text="Edit Classes", command=self.edit_classes, width=6).pack(side="left", padx=5,fill="x", expand=True)
        ttk.Button(self.button_frame, text="Edit Connections", command=self.manage_connections, width=6).pack(side="left",padx=5,fill="x",expand=True)
        self.btn_toggle = ttk.Button(self.button_frame, text="Full Details", command=self.toggle_shortened_details, width=6)
        self.btn_toggle.pack(side="left", padx=5, fill="x", expand=True)
        ttk.Button(self.button_frame, text="Save as image", command=self.save_image, width=6).pack(side="left", padx=5, fill="x",expand=True)
        ttk.Button(self.button_frame, text="Save as JSON", command=self.save_as_json, width=6).pack(side="left", padx=5,fill="x", expand=True)
        ttk.Button(self.button_frame, text="Open JSON", command=self.open_json, width=6).pack(side="left", padx=5, fill="x",expand=True)
        ttk.Button(self.button_frame, text="Legend", command=self.show_legend, width=6).pack(side="left", padx=5,fill="x", expand=True)

    def show_legend(self):
        legend_window = tk.Toplevel(self.root)
        legend_window.title("Arrow Legend")
        legend_window.geometry("400x250")

        label = ttk.Label(legend_window, text="UML Arrow Legend", font=("Helvetica", 12, "bold"))
        label.pack(pady=10)

        text = """\
        Inheritance: Solid arrow with an empty arrowhead.
        Composition: Solid arrow with a diamond arrowhead.
        Aggregation: Solid arrow with an empty diamond arrowhead.
        Dependency: Dashed arrow.
        Association: Solid arrow.
        Realization: Dashed arrow with an empty arrowhead.
        """
        legend_label = ttk.Label(legend_window, text=text, font=("Helvetica", 10))
        legend_label.pack(padx=20, pady=10)

        # Add a close button
        close_button = ttk.Button(legend_window, text="Close", command=legend_window.destroy)
        close_button.pack(pady=10)
    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.class_manager.classes_data = self.analyzer.analyze_python_files(folder_path)
            self.render_diagram()

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if file_path:
            self.class_manager.classes_data = self.analyzer.analyze_file(file_path)
            self.render_diagram()

    def render_diagram(self):
        self.uml_diagram.render_and_display_diagram(self.canvas, self.class_manager.get_classes(), self.shortened_details)

    def toggle_shortened_details(self):
        self.shortened_details = not self.shortened_details
        self.btn_toggle.config(text="Full Details" if self.shortened_details else "Shortened Details")
        self.render_diagram()

    def save_image(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            title="Save UML Diagram As"
        )
        if file_path:
            try:
                self.uml_diagram.save_image(file_path)
                messagebox.showinfo("Success", "Diagram saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save diagram: {e}")

    def edit_classes(self):
        if not self.edit_classes_window_opened or self.edit_classes_window is None or not self.edit_classes_window.edit_window.winfo_exists():
            self.edit_classes_window = EditClassesWindow(self.root, self.class_manager, self.render_diagram)
            self.edit_classes_window_opened = True
        else:
            self.edit_classes_window.edit_window.focus_force()

    def manage_connections(self):
        if len(self.class_manager.classes_data) < 2:
            messagebox.showerror("Error", "Not enough classes")
            return

        if not self.edit_connections_window_opened or self.edit_connections_window is None or not self.edit_connections_window.conn_window.winfo_exists():
            self.edit_connections_window = EditConnectionsWindow(self.root, self.class_manager, self.render_diagram)
            self.edit_connections_window_opened = True
        else:
            self.edit_connections_window.conn_window.focus_force()

    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")

    def save_as_json(self):
        self.class_manager.save_json()

    def open_json(self):
        self.class_manager.open_json()
        self.render_diagram()