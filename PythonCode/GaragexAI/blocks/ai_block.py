class AIBlock:
    def __init__(self, canvas, x=100, y=100, width=120, height=60, label="AI Block"):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
        self.is_selected = False  # เพิ่มสถานะเลือก

        self.id = None
        self.text_id = None

        self.draw()

    def draw(self):
        # สร้างสี่เหลี่ยม (เพิ่ม activefill สำหรับเมื่อเลือก)
        self.id = self.canvas.create_rectangle(
            self.x, self.y,
            self.x + self.width, self.y + self.height,
            fill="#4e88e3", outline="white", width=2,
            tags=("draggable", "block", "ai_block"),  # ต้องมี 'draggable'
            activefill="#6ea8ff"  # สีเมื่อเมาส์อยู่เหนือ
        )
        
        # สร้างข้อความ
        self.text_id = self.canvas.create_text(
            self.x + self.width // 2,
            self.y + self.height // 2,
            text=self.label,
            fill="white",
            font=("Segoe UI", 10, "bold"),
            tags=("text", "draggable")
        )

    def move(self, dx, dy):
        """เคลื่อนย้ายบล็อกและอัปเดตตำแหน่ง"""
        self.canvas.move(self.id, dx, dy)
        self.canvas.move(self.text_id, dx, dy)
        self.x += dx
        self.y += dy

    def set_selected(self, selected):
        """เปลี่ยนสถานะเลือกและอัปเดตการแสดงผล"""
        self.is_selected = selected
        outline = "yellow" if selected else "white"
        self.canvas.itemconfig(self.id, outline=outline, width=3 if selected else 2)

    def get_ids(self):
        return [self.id, self.text_id]

    def contains(self, x, y):
        """ตรวจสอบว่าจุด (x,y) อยู่ในบล็อก"""
        return (self.x <= x <= self.x + self.width and 
                self.y <= y <= self.y + self.height)