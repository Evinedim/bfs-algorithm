import tkinter as tk 
from tkinter import filedialog, messagebox
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

        self.create_widgets()
        self.setup_layout()
        self.draw_graph()

    def create_widgets(self):        
        self.left_frame = tk.Frame(self)
        
        self.left_title_label = tk.Label(self.left_frame, text="BFS Control", font=("Arial", 16, "bold"), pady=10)
        
        self.input_frame = tk.LabelFrame(self.left_frame, text="Input Vertices", font=("Arial", 12), padx=10, pady=10)
        self.start_label = tk.Label(self.input_frame, text="Start vertex:", font=("Arial", 12))
        self.start_entry = tk.Entry(self.input_frame, font=("Arial", 16, "bold"), 
                                   width=5, justify="center", relief=tk.SUNKEN, borderwidth=2) 
        self.end_label = tk.Label(self.input_frame, text="End vertex:", font=("Arial", 12))
        self.end_entry = tk.Entry(self.input_frame, font=("Arial", 16, "bold"), 
                                 width=5, justify="center", relief=tk.SUNKEN, borderwidth=2)
        
        self.initialize_button = tk.Button(self.left_frame, text="Initialize BFS", font=("Arial", 12, "bold"), bg="#4CAF50", 
                                           fg="white", relief=tk.RAISED, borderwidth=2, padx=20, pady=8, command=self.initialize_bfs)
        
        self.nav_frame = tk.LabelFrame(self.left_frame, text="Step Navigation", font=("Arial", 12), padx=10, pady=10)
        self.prev_button = tk.Button(self.nav_frame, text="◀ Previous Step", font=("Arial", 12, "bold"), bg="#2196F3", 
                                     fg="white", relief=tk.RAISED, borderwidth=2, width=15, command=self.previous_step)
        self.next_button = tk.Button(self.nav_frame, text="Next Step ▶", font=("Arial", 12, "bold"), bg="#2196F3", 
                                     fg="white", relief=tk.RAISED, borderwidth=2, width=15, command=self.next_step)
        
        self.step_info_frame = tk.Frame(self.nav_frame)
        self.step_label = tk.Label(self.step_info_frame, text="Step: 0/0", font=("Arial", 12, "bold"))
        
        self.graph_frame = tk.LabelFrame(self.left_frame, text="Graph Operations", font=("Arial", 12), padx=10, pady=10)
        self.reset_button = tk.Button(self.graph_frame, text="🔄 Reset Graph", font=("Arial", 12), bg="#FF9800", 
                                      fg="white", relief=tk.RAISED, borderwidth=2, width=15, command=self.draw_graph)
        self.load_button = tk.Button(self.graph_frame, text="📂 Load Graph", font=("Arial", 12), bg="#9C27B0", 
                                     fg="white", relief=tk.RAISED, borderwidth=2, width=15, command=self.load_graph)
        
        self.canvas = tk.Canvas(self, bg="white", relief=tk.SUNKEN, borderwidth=2)

        self.right_frame = tk.Frame(self)
        
        self.right_title_label = tk.Label(self.right_frame, text="BFS details", font=("Arial", 16, "bold"), pady=10)

        self.status_frame = tk.LabelFrame(self.right_frame, text="Algorithm Status", font=("Arial", 12), padx=10, pady=10)
        self.status_label = tk.Label(self.status_frame, text="Status: Ready", font=("Arial", 12), justify=tk.LEFT, wraplength=250)
        
        self.details_frame = tk.LabelFrame(self.right_frame, text="Current Step", font=("Arial", 12), padx=10, pady=10)
        self.path_label = tk.Label(self.details_frame, text="Current path: \n-", font=("Arial", 12), justify=tk.LEFT, wraplength=250)
        self.visited_label = tk.Label(self.details_frame, text="Visited vertices: \n-", font=("Arial", 12), justify=tk.LEFT, wraplength=250)
        self.queue_label = tk.Label(self.details_frame, text="Queue status: \n-", font=("Arial", 12), justify=tk.LEFT, wraplength=250)
        
    def setup_layout(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=1)
            
        self.left_frame.grid(row=0, column=0, sticky="nswe", padx=(5, 0), pady=5)
        self.left_frame.config(width=300)
        
        self.left_title_label.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        self.input_frame.pack(fill=tk.X, padx=10, pady=5)
        self.start_label.pack(anchor=tk.W, pady=(0, 5))
        self.start_entry.pack(fill=tk.X, pady=(0, 10))
        self.end_label.pack(anchor=tk.W, pady=(0, 5))
        self.end_entry.pack(fill=tk.X, pady=(0, 5))
        
        self.initialize_button.pack(pady=15, padx=10)
        
        self.nav_frame.pack(fill=tk.X, padx=10, pady=5)
        self.prev_button.pack(pady=5)
        self.next_button.pack(pady=5)
        self.step_info_frame.pack(pady=10)
        self.step_label.pack()
        
        self.graph_frame.pack(fill=tk.X, padx=10, pady=5)
        self.reset_button.pack(pady=5)
        self.load_button.pack(pady=5)
        
        self.canvas.grid(row=0, column=1, sticky="nswe", padx=5, pady=5)
        
        self.right_frame.grid(row=0, column=2, sticky="nswe", padx=(0, 5), pady=5)
        self.right_frame.config(width=300)
        
        self.right_title_label.pack(fill=tk.X, padx=10, pady=(10, 5))

        self.status_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        self.status_label.pack(fill=tk.X, pady=5)
        
        self.details_frame.pack(fill=tk.X, padx=10, pady=5)
        self.path_label.pack(anchor=tk.W, pady=2)
        self.visited_label.pack(anchor=tk.W, pady=2)
        self.queue_label.pack(anchor=tk.W, pady=2)

    def draw_graph(self):
        vertexes = set(self.graph.keys())
        edges = set((n, v) for n in self.graph for v in self.graph[n])

        self.coords = {}
        for i, vertex in enumerate(vertexes):
            angle = 2 * math.pi * (i / len(vertexes))

            self.coords[vertex] = (
                400 + 200 * math.cos(angle), 
                400 + 200 * math.sin(angle)
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