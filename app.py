import tkinter as tk 
from tkinter import ttk
import math

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("bfs-algorithm")
        self.geometry("900x600")

        self.create_widgets()
        self.setup_layout()
        self.draw_graph(graph)

        self.mainloop()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, bg='white', relief=tk.SUNKEN, borderwidth=2)

    def setup_layout(self):
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def draw_graph(self, graph):
        vertexes = set(graph.keys())
        edges = set((n, v) for n in graph for v in graph[n])

        coords = {}
        for i, vertex in enumerate(vertexes):
            angle = 2 * math.pi * (i / len(vertexes))

            coords[vertex] = (
                300 + 150 * math.cos(angle), 
                300 + 150 * math.sin(angle)
            )

        for v1, v2 in edges:
            self.canvas.create_line(*coords[v1], *coords[v2], width=3, fill='black')

        for vertex, (x, y) in coords.items():
            self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill='lightgreen', outline='black', width=3)
            self.canvas.create_text(x, y, text=str(vertex), font=('Arial', 12))
            


app = App()
app.mainloop()