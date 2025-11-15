import tkinter as tk 
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("bfs-algorithm")
        self.geometry("900x600")

        self.create_widgets()
        self.setup_layout()
        self.draw_graph()

        self.mainloop()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, bg='white', relief=tk.SUNKEN, borderwidth=2)

    def setup_layout(self):
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def draw_graph(self):
        pass


app = App()
app.mainloop()