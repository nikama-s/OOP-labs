import io
from tkinter import messagebox
from graphviz import Digraph
from PIL import Image, ImageTk

class UMLDiagram:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.initialized = True
            self.diagram = None
            self.diagram_image = None

    def generate_class_diagram(self, classes, shortened_details):
        dot = Digraph(comment="Class Diagram", engine="dot")
        dot.attr("node", shape="plaintext", fontname="Helvetica")
        dot.attr(rankdir="BT")
        for cls, details in classes.items():
            label = self.build_class_label(cls, details, shortened_details)
            dot.node(cls, label=label)
        self.add_edges(classes, dot, "inheritance", shortened_details)
        self.add_edges(classes, dot, "compositions",shortened_details)
        self.add_edges(classes, dot, "aggregations", shortened_details)
        self.add_edges(classes, dot, "dependencies", shortened_details)
        self.add_edges(classes, dot, "associations", shortened_details)
        self.add_edges(classes, dot, "realizations", shortened_details)
        return dot

    def build_class_label(self, cls, details, shortened_details):
        attributes = list(details["attributes"])
        methods = details["methods"]
        if shortened_details:
            attributes = attributes[:2] + (["..."] if len(attributes) > 2 else [])
            methods = methods[:2] + (["..."] if len(methods) > 2 else [])
        label = f"""
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
            <TR><TD BGCOLOR="lightblue"><B>{cls}</B></TD></TR>
        """
        if attributes:
            label += f"""
            <TR><TD ALIGN="left">{'<BR ALIGN="left"/>'.join(attributes)}</TD></TR>
            """
        if methods:
            label += f"""
            <TR><TD ALIGN="left">{'<BR ALIGN="left"/>'.join(methods)}</TD></TR>
            """
        label += "</TABLE>"
        return f"<{label}>"

    def add_edges(self, classes, dot, relation_key, shortened_details):
        edge_style_map = {
            "inheritance": ("solid", "empty"),
            "compositions": ("solid",  "diamond"),
            "aggregations": ("solid", "odiamond"),
            "dependencies": ("dashed", "normal"),
            "associations": ("solid", "normal"),
            "realizations": ("dashed", "empty"),
        }
        edge_style, arrow_type = edge_style_map.get(relation_key, ("solid", "normal"))
        for cls, details in list(classes.items()):
            for related_cls in details[relation_key]:
                self.add_class_if_missing(classes, dot, related_cls, shortened_details)
                dot.edge(cls if relation_key == "inheritance" else related_cls, related_cls if relation_key == "inheritance" else cls, style=edge_style, arrowhead=arrow_type, arrowsize="0.8")

    def add_class_if_missing(self, classes, dot, cls_name, shortened_details):
        if cls_name not in classes:
            classes[cls_name] = {
                "inheritance": [],
                "attributes": [],
                "methods": [],
                "compositions": [],
                "aggregations": [],
                 "dependencies": [],
                "associations": [],
                "realizations": []
            }
            label = self.build_class_label(cls_name, classes[cls_name], shortened_details)
            dot.node(cls_name, label=label)

    def render_and_display_diagram(self, canvas, classes_data, shortened_details):
        try:
            self.diagram = self.generate_class_diagram(classes_data, shortened_details)
            diagram_bytes = self.diagram.pipe(format="png")
            diagram_image_pil = Image.open(io.BytesIO(diagram_bytes))
            self.diagram_image = ImageTk.PhotoImage(diagram_image_pil)
            canvas.config(scrollregion=(0, 0, self.diagram_image.width(), self.diagram_image.height()))
            canvas.create_image(0, 0, anchor="nw", image=self.diagram_image)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to render diagram: {e}")

    def save_image(self, file_path):
        if not self.diagram:
            raise ValueError("No diagram available to save.")
        with open(file_path, "wb") as file:
            file.write(self.diagram.pipe(format="png"))
