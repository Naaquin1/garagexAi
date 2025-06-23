from blocks.ai_block import AIBlock  # type: ignore
import tkinter as tk
from tkinter import ttk

class CanvasScreen:
    def __init__(self, parent, logger):
        self.parent = parent
        self.logger = logger
        self.ai_blocks = []
        self.drag_data = {"block": None, "x": 0, "y": 0}

        self.frame = tk.Frame(self.parent, bg="#1e1e1e")
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.notebook = ttk.Notebook(self.frame)
        self.canvas_tab = tk.Frame(self.notebook, bg="#2e2e2e")
        self.notebook.add(self.canvas_tab, text="Main Scene")
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.grid_canvas = tk.Canvas(self.canvas_tab, bg="#2e2e2e", highlightthickness=0)
        self.grid_canvas.pack(fill=tk.BOTH, expand=True)
        self.grid_canvas.bind("<Configure>", self.draw_grid)

        self.grid_canvas.bind("<Button-1>", self.on_click)
        self.grid_canvas.bind("<B1-Motion>", self.on_drag)
        self.grid_canvas.bind("<ButtonRelease-1>", self.on_release)

        self.add_ai_block()

    def draw_grid(self, event=None):
        self.grid_canvas.delete("grid_line")
        grid_size = 30
        w = self.grid_canvas.winfo_width()
        h = self.grid_canvas.winfo_height()
        for i in range(0, w, grid_size):
            self.grid_canvas.create_line([(i, 0), (i, h)], tag="grid_line", fill="#444444")
        for i in range(0, h, grid_size):
            self.grid_canvas.create_line([(0, i), (w, i)], tag="grid_line", fill="#444444")

    def add_ai_block(self):
        block = AIBlock(self.grid_canvas, x=150 + len(self.ai_blocks) * 30, y=150)
        self.ai_blocks.append(block)
        self.logger(f"[Block] Added: {block.label}")

    def on_click(self, event):
        clicked = self.grid_canvas.find_closest(event.x, event.y)[0]
        for block in self.ai_blocks:
            if block.contains(clicked):
                self.drag_data["block"] = block
                self.drag_data["x"] = event.x
                self.drag_data["y"] = event.y
                self.logger(f"[DEBUG] Start dragging block: {block.label}")
                break

    def on_drag(self, event):
        block = self.drag_data["block"]
        if block:
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            block.move(dx, dy)
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
            self.logger(f"[DEBUG] Dragging block: {block.label} by ({dx}, {dy})")

    def on_release(self, event):
        if self.drag_data["block"]:
            self.logger(f"[DEBUG] Released block: {self.drag_data['block'].label}")
        self.drag_data["block"] = None