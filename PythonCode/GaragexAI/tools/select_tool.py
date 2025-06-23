class SelectTool:
    def __init__(self, canvas, logger):
        self.canvas = canvas
        self.logger = logger
        self.selected_items = []
        self.highlight_color = "#ffff00"
        self.normal_color = "#ffffff"
        self.highlight_width = 2
        self.normal_width = 1

    def activate(self):
        """เปิดใช้งานเครื่องมือเลือก"""
        self.canvas.bind("<Button-1>", self.on_click)
        self.logger("[SelectTool] เปิดใช้งานเครื่องมือเลือก")

    def deactivate(self):
        """ปิดใช้งานเครื่องมือเลือก"""
        self.canvas.unbind("<Button-1>")
        self.deselect_all()

    def on_click(self, event):
        """จัดการเมื่อคลิกเมาส์"""
        clicked_items = self.canvas.find_overlapping(
            event.x - 5, event.y - 5, event.x + 5, event.y + 5)

        # ยกเลิกการเลือกทั้งหมดก่อน
        self.deselect_all()

        for item in clicked_items:
            tags = self.canvas.gettags(item)
            for tag in tags:
                if tag.startswith("block_"):
                    self.select_item(item)
                    block_idx = int(tag.split("_")[1])
                    self.logger(f"เลือกบล็อก #{block_idx}")
                    return

    def select_item(self, item):
        """เลือกวัตถุและเน้นสี"""
        self.canvas.itemconfig(item, outline=self.highlight_color, width=self.highlight_width)
        self.selected_items.append(item)

    def deselect_all(self):
        """ยกเลิกการเลือกทั้งหมด"""
        for item in self.selected_items:
            self.canvas.itemconfig(item, outline=self.normal_color, width=self.normal_width)
        self.selected_items = []