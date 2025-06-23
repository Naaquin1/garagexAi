import math

class MoveTool:
    def __init__(self, studio):
        self.studio = studio
        self.canvas = studio.grid_canvas
        self.selected_block = None
        self.drag_offset = (0, 0)
        self.text_mapping = {}  # เก็บ mapping: block_id → text_id

    def activate(self):
        """เปิดใช้งานเครื่องมือเคลื่อนย้าย"""
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.studio.log_to_terminal("[MoveTool] เปิดใช้งานเครื่องมือเคลื่อนย้าย")

    def deactivate(self):
        """ปิดใช้งานเครื่องมือเคลื่อนย้าย"""
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.selected_block = None

    def register_block(self, block_id, text_id):
        """ลงทะเบียนบล็อกและข้อความ"""
        self.text_mapping[block_id] = text_id

    def on_click(self, event):
        """จัดการเมื่อคลิกเมาส์"""
        clicked_items = self.canvas.find_overlapping(
            event.x-5, event.y-5, event.x+5, event.y+5)
        
        for item in clicked_items:
            tags = self.canvas.gettags(item)
            for tag in tags:
                if tag.startswith("block_"):
                    block_idx = int(tag.split("_")[1])
                    self.selected_block = self.studio.blocks[block_idx]
                    
                    # คำนวณตำแหน่งสัมพัทธ์
                    x, y, _ = self.studio.project_3d_to_2d(
                        self.selected_block["x"],
                        self.selected_block["y"],
                        self.selected_block["z"]
                    )
                    self.drag_offset = (event.x - x, event.y - y)
                    self.highlight_block(block_idx)
                    return

    def on_drag(self, event):
        """จัดการเมื่อลากเมาส์"""
        if self.selected_block:
            # คำนวณตำแหน่งใหม่ในโลก 3D
            x2d = event.x - self.drag_offset[0]
            y2d = event.y - self.drag_offset[1]
            
            # แปลงพิกัด 2D เป็น 3D
            x = (x2d - self.canvas.winfo_width()/2) / 2
            z = (y2d - self.canvas.winfo_height()/2) / 2
            
            # อัพเดตตำแหน่งบล็อก
            self.selected_block["x"] = x
            self.selected_block["z"] = -z  # กลับทิศทาง Z
            
            # วาดฉากใหม่
            self.studio.redraw_scene()
            
            # อัพเดตข้อความใน Terminal
            self.studio.log_to_terminal(
                f"ย้ายบล็อกไปที่ตำแหน่ง ({x:.1f}, "
                f"{self.selected_block['y']:.1f}, "
                f"{-z:.1f})"
            )

    def on_release(self, event):
        """จัดการเมื่อปล่อยเมาส์"""
        self.selected_block = None

    def highlight_block(self, block_idx):
        """เน้นบล็อกที่เลือก"""
        # ยกเลิกการเน้นบล็อกเดิม
        if self.studio.selected_block is not None:
            for item in self.canvas.find_withtag(f"block_{self.studio.selected_block}"):
                self.canvas.itemconfig(item, outline="#ffffff")
        
        # เน้นบล็อกใหม่
        self.studio.selected_block = block_idx
        for item in self.canvas.find_withtag(f"block_{block_idx}"):
            self.canvas.itemconfig(item, outline="#ffff00", width=2)