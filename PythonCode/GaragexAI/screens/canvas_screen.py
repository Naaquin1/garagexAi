from blocks.ai_block import AIBlock
from tools.move_tool import MoveTool  # แก้ไขตามโครงสร้างโฟลเดอร์
import tkinter as tk
from tkinter import ttk


class CanvasScreen:
    def __init__(self, parent, logger):
        self.parent = parent
        self.logger = logger
        self.ai_blocks = []
        
        # Initialize UI
        self.frame = tk.Frame(self.parent, bg="#1e1e1e")
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.notebook = ttk.Notebook(self.frame)
        self.canvas_tab = tk.Frame(self.notebook, bg="#2e2e2e")
        self.notebook.add(self.canvas_tab, text="Main Scene")
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Canvas setup
        self.grid_canvas = tk.Canvas(
            self.canvas_tab, 
            bg="#2e2e2e", 
            highlightthickness=0
        )
        self.grid_canvas.pack(fill=tk.BOTH, expand=True)
        self.grid_canvas.bind("<Configure>", self.draw_grid)
        
        # Tool initialization
        try:
            self.move_tool = MoveTool(self.grid_canvas, self.logger)
            self.move_tool.activate()
            self.logger("[Canvas] Tools initialized successfully")
        except Exception as e:
            self.logger(f"[ERROR] Tool init failed: {str(e)}")

        # Add first block
        self.add_ai_block()

    def draw_grid(self, event=None):
        """Draw grid lines on canvas"""
        self.grid_canvas.delete("grid_line")
        grid_size = 30
        w = self.grid_canvas.winfo_width()
        h = self.grid_canvas.winfo_height()
        
        # Vertical lines
        for i in range(0, w, grid_size):
            self.grid_canvas.create_line(
                i, 0, i, h,
                tag="grid_line",
                fill="#444444"
            )
            
        # Horizontal lines
        for i in range(0, h, grid_size):
            self.grid_canvas.create_line(
                0, i, w, i,
                tag="grid_line",
                fill="#444444"
            )

    def add_ai_block(self):
        """Add a new AI block to canvas"""
        if not hasattr(self, 'grid_canvas'):
            self.logger("[ERROR] Canvas not initialized")
            return

        try:
            x_pos = 150 + len(self.ai_blocks) * 30
            y_pos = 150
            block = AIBlock(self.grid_canvas, x=x_pos, y=y_pos)
            self.ai_blocks.append(block)
            self.logger(
                f"[Block] Added '{block.label}' at ({x_pos}, {y_pos}) "
                f"(Total: {len(self.ai_blocks)})"
            )
        except Exception as e:
            self.logger(f"[ERROR] Failed to add block: {str(e)}")