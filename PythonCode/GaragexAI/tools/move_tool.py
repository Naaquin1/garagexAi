import tkinter as tk

class MoveTool:
    def __init__(self, canvas, logger):
        self.canvas = canvas
        self.logger = logger
        self.selected_item = None
        self.offset_x = 0
        self.offset_y = 0
        self.text_mapping = {}  # 🧠 เก็บ mapping: block id → text id

    def activate(self):
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.logger("[MoveTool] Activated")

    def register_block(self, block_id, text_id):
        self.text_mapping[block_id] = text_id  # 🧩 บอกว่า block นี้มีข้อความ id อะไร

    def on_click(self, event):
        items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        for item in items:
            if "block" in self.canvas.gettags(item):
                self.selected_item = item
                x1, y1, x2, y2 = self.canvas.coords(item)
                self.offset_x = event.x - x1
                self.offset_y = event.y - y1
                return

    def on_drag(self, event):
        if self.selected_item:
            x1 = event.x - self.offset_x
            y1 = event.y - self.offset_y
            x2 = x1 + 120
            y2 = y1 + 60
            self.canvas.coords(self.selected_item, x1, y1, x2, y2)

            # ✅ ขยับเฉพาะข้อความของ block นั้น ๆ
            text_id = self.text_mapping.get(self.selected_item)
            if text_id:
                self.canvas.coords(text_id, x1 + 60, y1 + 30)

    def on_release(self, event):
        self.selected_item = None