import tkinter as tk 
from tkinter import ttk, filedialog, messagebox
import math
import json
from bfs import bfs


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("bfs-algorithm")
        self.geometry("1200x700")

        self.graph = {
            'A': ['B', 'C'],
            'B': ['A', 'D', 'E'],
            'C': ['A', 'F'],
            'D': ['B'],
            'E': ['B', 'F'],
            'F': ['C', 'E'],
            'G': []
        }

        self.bfs_steps = []
        self.current_step = 0

        self.create_styles()
        self.create_widgets()
        self.setup_layout()
        self.draw_graph()

    def create_styles(self):
        self.style = ttk.Style()

        self.style.configure(
            "Custom.TLabel",
            font=("Arial", 14),
            padding=5
        )

        self.style.configure(
            "Custom.TButton",
            font=("Arial", 12),
            padding=5
        )

    def create_widgets(self):
        self.canvas = tk.Canvas(self, bg="white", relief=tk.SUNKEN, borderwidth=2)

        self.start_label = ttk.Label(self, text="Start vertex:", style="Custom.TLabel")
        self.start_entry = ttk.Entry(self, font=("Arial", 18, "bold"), width=3, justify="center")

        self.end_label = ttk.Label(self, text="End vertex:", style="Custom.TLabel")
        self.end_entry = ttk.Entry(self, font=("Arial", 18, "bold"), width=3, justify="center")

        self.initialize_button = ttk.Button(self, text="Initialize BFS", style="Custom.TButton", command=self.initialize_bfs)
        self.reset_button = ttk.Button(self, text="Reset graph", style="Custom.TButton", comma=self.draw_graph)
        self.load_button = ttk.Button(self, text="Load graph", style="Custom.TButton", command=self.load_graph)

        self.next_step_button = ttk.Button(self, text="Next step", style="Custom.TButton", command=self.next_step)
        self.previous_step_button = ttk.Button(self, text="Previous step", style="Custom.TButton", command=self.previous_step)

    def setup_layout(self):
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.start_label.pack(side=tk.LEFT, padx=(10, 0), pady=5)
        self.start_entry.pack(side=tk.LEFT, padx=10, pady=5)

        self.end_label.pack(side=tk.LEFT, padx=(10, 0), pady=5)
        self.end_entry.pack(side=tk.LEFT, padx=10, pady=5)

        self.initialize_button.pack(side=tk.LEFT, padx=(75, 10), pady=5)
        self.next_step_button.pack(side=tk.LEFT, padx=10, pady=5)
        self.previous_step_button.pack(side=tk.LEFT, padx=10, pady=5)
        self.reset_button.pack(side=tk.LEFT, padx=10, pady=5)
        self.load_button.pack(side=tk.LEFT, padx=10, pady=5)


    def draw_graph(self):
        vertexes = set(self.graph.keys())
        edges = set((n, v) for n in self.graph for v in self.graph[n])

        self.coords = {}
        for i, vertex in enumerate(vertexes):
            angle = 2 * math.pi * (i / len(vertexes))

            self.coords[vertex] = (
                450 + 200 * math.cos(angle), 
                275 + 200 * math.sin(angle)
            )

        for v1, v2 in edges:
            x1, y1, x2, y2 = *self.coords[v1], *self.coords[v2]

            self.canvas.create_line(x1, y1, x2, y2, width=3, fill="black")

            angle = math.atan2(y2 - y1, x2 - x1)

            end_x = x2 - 20 * math.cos(angle)
            end_y = y2 - 20 * math.sin(angle)
 
            arrow_x1 = end_x - 20 * math.cos(angle - math.pi / 12)
            arrow_y1 = end_y - 20 * math.sin(angle - math.pi / 12)
            arrow_x2 = end_x - 20 * math.cos(angle + math.pi / 12)  
            arrow_y2 = end_y - 20 * math.sin(angle + math.pi / 12)

            self.canvas.create_line(arrow_x1, arrow_y1, end_x, end_y, width=3, fill="black")
            self.canvas.create_line(arrow_x2, arrow_y2, end_x, end_y, width=3, fill="black")            

        for vertex, (x, y) in self.coords.items():
            self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="lightgreen", outline="black", width=3)
            self.canvas.create_text(x, y, text=str(vertex), font=("Arial", 12))

    def load_graph(self):
        file_path = filedialog.askopenfilename()

        with open(file_path) as file:
            try:
                self.graph = dict(json.load(file))
                self.canvas.delete("all")
                self.draw_graph()
            except:
                messagebox.showerror("Error", "Something wrong with file!!!")
    
    def initialize_bfs(self):
        try:
            self.coords[self.end_entry.get()]
            self.current_step = 0
            self.bfs_steps = bfs(self.graph, self.start_entry.get(), self.end_entry.get())
        except:
            messagebox.showerror("Error", "There are no such vertexes!!!")

    def draw_current(self, nodes):
        try:
            self.draw_graph()

            end_x, end_y = self.coords[self.end_entry.get()]

            for vertex in nodes:
                x, y = self.coords[vertex]
                self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="lightblue", outline="black", width=3)

                if (x, y) == (end_x, end_y):
                    self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="red", outline="black", width=3)

                self.canvas.create_text(x - 7, y, text=str(vertex), font=("Arial", 12))
                self.canvas.create_text(x + 7, y, text=nodes.index(vertex), font=("Arial", 12))

                self.update()
        except KeyError:
            messagebox.showerror("Error", "Graph is not initialized!!!")

    def next_step(self):
        if self.current_step < len(self.bfs_steps) - 1:
            self.current_step += 1
            self.draw_current(self.bfs_steps[self.current_step])


    def previous_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.draw_current(self.bfs_steps[self.current_step])

if __name__ == "__main__":
    app = App()
    app.mainloop()