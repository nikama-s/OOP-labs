import tkinter as tk
from analyzer import ClassAnalyzer
from uml_diagram import UMLDiagram
from class_manager import ClassManager
from gui import GUI

if __name__ == "__main__":
    root = tk.Tk()

    analyzer = ClassAnalyzer()
    uml_diagram = UMLDiagram()
    class_manager = ClassManager()

    app = GUI(root, analyzer, uml_diagram, class_manager)

    root.mainloop()