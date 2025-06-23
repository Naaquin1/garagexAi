import tkinter as tk
from tkinter import Menu, Text, ttk, messagebox
import math

class AIStudioPrototype:
    def __init__(self, root):
        self.root = root
        self.root.title("GaragexAI Studio - โหมด 3D")
        self.root.geometry("1200x800")
        self.root.configure(bg="#2e2e2e")
        
        # ตัวแปรระบบ 3D
        self.blocks = []
        self.camera_angle_x = 30
        self.camera_angle_y = -30
        self.camera_distance = 800
        self.rotation_speed = 0.5
        self.show_axes = True
        self.show_grid = True
        
        # ระบบลากและวางบล็อก
        self.selected_block = None
        self.drag_start = None
        
        # สร้างส่วนประกอบ UI
        self.create_menu()
        self.create_3d_layout()
        self.create_toolbox()
        self.create_explorer()
        self.create_terminal()
        self.create_status_bar()
        
        # ระบบควบคุม 3D
        self.setup_3d_controls()
        
        # วาดฉากเริ่มต้น
        self.redraw_scene()

    def create_menu(self):
        """สร้างเมนูภาษาไทย"""
        menubar = Menu(self.root)
        
        # เมนูไฟล์
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="สร้างใหม่", command=self.new_project)
        file_menu.add_command(label="เปิด...", command=self.open_project)
        file_menu.add_separator()
        file_menu.add_command(label="ออก", command=self.root.quit)
        menubar.add_cascade(label="ไฟล์", menu=file_menu)
        
        # เมนูมุมมอง
        view_menu = Menu(menubar, tearoff=0)
        view_menu.add_checkbutton(label="แสดงแกน", variable=tk.BooleanVar(value=True), 
                                command=self.toggle_axes)
        view_menu.add_checkbutton(label="แสดงกริด", variable=tk.BooleanVar(value=True),
                                command=self.toggle_grid)
        menubar.add_cascade(label="มุมมอง", menu=view_menu)
        
        # เมนูช่วยเหลือ
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="เกี่ยวกับ", command=self.show_about)
        menubar.add_cascade(label="ช่วยเหลือ", menu=help_menu)
        
        self.root.config(menu=menubar)

    def create_3d_layout(self):
        """สร้าง Layout แบบ 3D"""
        self.main_frame = tk.Frame(self.root, bg="#2e2e2e")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Toolbox ด้านซ้าย
        self.toolbox_frame = tk.Frame(self.main_frame, width=150, bg="#1e1e1e")
        self.toolbox_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Canvas กลาง (แบบ 3D)
        self.canvas_frame = tk.Frame(self.main_frame, bg="#000000")
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.grid_canvas = tk.Canvas(
            self.canvas_frame, 
            bg="#1a1a1a", 
            highlightthickness=0,
            bd=0
        )
        self.grid_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Explorer ด้านขวา
        self.explorer_frame = tk.Frame(self.main_frame, width=150, bg="#1e1e1e")
        self.explorer_frame.pack(side=tk.RIGHT, fill=tk.Y)

    def create_toolbox(self):
        """สร้างกล่องเครื่องมือ"""
        lbl = tk.Label(self.toolbox_frame, text="เครื่องมือ", bg="#1e1e1e", fg="white", font=("Tahoma", 10, "bold"))
        lbl.pack(pady=5)
        
        # ปุ่มเพิ่มบล็อก
        ttk.Button(
            self.toolbox_frame,
            text="เพิ่มบล็อก AI",
            command=self.add_ai_block
        ).pack(pady=5)
        
        ttk.Button(
            self.toolbox_frame,
            text="เพิ่มโมเดล 3D",
            command=self.add_3d_model
        ).pack(pady=5)
        
        ttk.Button(
            self.toolbox_frame,
            text="ล้างฉาก",
            command=self.clear_scene
        ).pack(pady=5)

    def create_explorer(self):
        """สร้าง Explorer"""
        lbl = tk.Label(self.explorer_frame, text="โครงสร้างโปรเจค", bg="#1e1e1e", fg="white", font=("Tahoma", 10, "bold"))
        lbl.pack(pady=5)
        
        self.tree = ttk.Treeview(self.explorer_frame)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # เพิ่มโฟลเดอร์เริ่มต้น
        self.tree.insert("", "end", text="ฉากหลัก", iid="main_scene", open=True)
        self.tree.insert("main_scene", "end", text="วัตถุ 3D")

    def create_terminal(self):
        """สร้าง Terminal"""
        terminal_frame = tk.Frame(self.root, height=150, bg="#1e1e1e")
        terminal_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        lbl = tk.Label(terminal_frame, text="Terminal", bg="#1e1e1e", fg="white", font=("Tahoma", 10, "bold"))
        lbl.pack(side=tk.TOP, anchor=tk.W, padx=5)
        
        self.terminal = Text(
            terminal_frame,
            bg="#252526",
            fg="#cccccc",
            insertbackground="white",
            wrap=tk.WORD,
            font=("Consolas", 10)
        )
        self.terminal.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0,5))
        
        self.log_to_terminal("ยินดีต้อนรับสู่ GaragexAI Studio")
        self.log_to_terminal("ระบบพร้อมใช้งาน โหมด 3D")

    def create_status_bar(self):
        """สร้าง Status Bar"""
        self.status_var = tk.StringVar()
        self.status_var.set("พร้อม | มุมกล้อง: X=30° Y=-30° | ระยะทาง: 800")
        
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg="#007acc",
            fg="white"
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_3d_controls(self):
        """ตั้งค่าการควบคุม 3D"""
        # หมุนกล้องด้วยคลิกขวา
        self.grid_canvas.bind("<Button-3>", self.start_rotate)
        self.grid_canvas.bind("<B3-Motion>", self.rotate_scene)
        self.grid_canvas.bind("<ButtonRelease-3>", self.stop_rotate)
        
        # ย้ายวัตถุด้วยคลิกซ้าย
        self.grid_canvas.bind("<Button-1>", self.handle_click)
        self.grid_canvas.bind("<B1-Motion>", self.handle_drag)
        self.grid_canvas.bind("<ButtonRelease-1>", self.stop_drag)
        
        # ซูมด้วยเมาส์วีล
        self.grid_canvas.bind("<MouseWheel>", self.zoom_scene)
        
        # คีย์ลัด
        self.root.bind("<Left>", lambda e: self.rotate_scene_key(-5, 0))
        self.root.bind("<Right>", lambda e: self.rotate_scene_key(5, 0))
        self.root.bind("<Up>", lambda e: self.rotate_scene_key(0, -5))
        self.root.bind("<Down>", lambda e: self.rotate_scene_key(0, 5))
        self.root.bind("<Control-Left>", lambda e: self.rotate_scene_key(0, -5))
        self.root.bind("<Control-Right>", lambda e: self.rotate_scene_key(0, 5))
        self.root.bind("<Control-Up>", lambda e: self.zoom_scene_key(50))
        self.root.bind("<Control-Down>", lambda e: self.zoom_scene_key(-50))
        self.root.bind("<Escape>", lambda e: setattr(self, 'selected_block', None))

    def project_3d_to_2d(self, x, y, z):
        """แปลงพิกัด 3D เป็น 2D"""
        angle_x = math.radians(self.camera_angle_x)
        angle_y = math.radians(self.camera_angle_y)
        
        # หมุนรอบแกน Y
        cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
        x_rot = x * cos_y - z * sin_y
        z_rot = x * sin_y + z * cos_y
        
        # หมุนรอบแกน X
        cos_x, sin_x = math.cos(angle_x), math.sin(angle_x)
        y_rot = y * cos_x - z_rot * sin_x
        z_final = y * sin_x + z_rot * cos_x
        
        # ฉายภาพ Perspective
        factor = self.camera_distance / (self.camera_distance + z_final)
        x2d = x_rot * factor + self.grid_canvas.winfo_width() / 2
        y2d = -y_rot * factor + self.grid_canvas.winfo_height() / 2
        
        return x2d, y2d, factor

    def draw_3d_grid(self):
        """วาดกริด 3D"""
        if not self.show_grid:
            return
            
        self.grid_canvas.delete("grid")
        grid_size = 50
        grid_lines = 10
        
        # วาดเส้นกริดแกน XZ (พื้น)
        for i in range(-grid_lines, grid_lines+1):
            # เส้นแกน X
            x1, y1, _ = self.project_3d_to_2d(i*grid_size, 0, -grid_lines*grid_size)
            x2, y2, _ = self.project_3d_to_2d(i*grid_size, 0, grid_lines*grid_size)
            self.grid_canvas.create_line(x1, y1, x2, y2, fill="#444444", tags="grid", width=1)
            
            # เส้นแกน Z
            x1, y1, _ = self.project_3d_to_2d(-grid_lines*grid_size, 0, i*grid_size)
            x2, y2, _ = self.project_3d_to_2d(grid_lines*grid_size, 0, i*grid_size)
            self.grid_canvas.create_line(x1, y1, x2, y2, fill="#444444", tags="grid", width=1)

    def draw_3d_axes(self):
        """วาดแกน 3D"""
        if not self.show_axes:
            return
            
        length = 200
        thickness = 3
        
        # แกน X (สีแดง)
        x_end, y_end, _ = self.project_3d_to_2d(length, 0, 0)
        self.grid_canvas.create_line(
            self.grid_canvas.winfo_width()/2, self.grid_canvas.winfo_height()/2,
            x_end, y_end,
            fill="#ff5555", width=thickness, tags="axes"
        )
        
        # แกน Y (สีเขียว)
        x_end, y_end, _ = self.project_3d_to_2d(0, length, 0)
        self.grid_canvas.create_line(
            self.grid_canvas.winfo_width()/2, self.grid_canvas.winfo_height()/2,
            x_end, y_end,
            fill="#55ff55", width=thickness, tags="axes"
        )
        
        # แกน Z (สีน้ำเงิน)
        x_end, y_end, _ = self.project_3d_to_2d(0, 0, length)
        self.grid_canvas.create_line(
            self.grid_canvas.winfo_width()/2, self.grid_canvas.winfo_height()/2,
            x_end, y_end,
            fill="#5555ff", width=thickness, tags="axes"
        )

    def add_3d_block(self, x=0, y=0, z=0, size=50, color="#4e88e3", text="บล็อก"):
        """เพิ่มบล็อก 3D"""
        block_id = len(self.blocks)
        self.blocks.append({
            "id": block_id,
            "x": x, "y": y, "z": z,
            "size": size,
            "color": color,
            "text": text
        })
        
        # อัพเดต Explorer
        self.tree.insert("main_scene", "end", text=text, iid=f"block_{block_id}")
        
        self.redraw_scene()
        self.log_to_terminal(f"เพิ่มบล็อก 3D: {text} ที่ตำแหน่ง ({x}, {y}, {z})")

    def handle_click(self, event):
        """จัดการการคลิกเมาส์"""
        # ค้นหาวัตถุที่คลิก
        clicked_items = []
        for item in self.grid_canvas.find_overlapping(event.x-5, event.y-5, event.x+5, event.y+5):
            tags = self.grid_canvas.gettags(item)
            if tags and tags[0].startswith("block_"):
                clicked_items.append(item)
        
        if clicked_items:
            # เลือกวัตถุที่อยู่ด้านหน้า (Z สูงสุด)
            front_item = max(clicked_items, key=lambda item: self.blocks[int(self.grid_canvas.gettags(item)[0].split("_")[1])]['z'])
            block_id = int(self.grid_canvas.gettags(front_item)[0].split("_")[1])
            self.selected_block = self.blocks[block_id]
            self.drag_start = (event.x, event.y, 
                             self.selected_block['x'],
                             self.selected_block['y'],
                             self.selected_block['z'])
            self.log_to_terminal(f"เลือกบล็อก: {self.selected_block['text']}")
        else:
            self.selected_block = None
        
        self.redraw_scene()

    def handle_drag(self, event):
        """จัดการการลากเมาส์"""
        if self.selected_block and self.drag_start:
            self.move_block(event)

    def move_block(self, event):
        """ย้ายบล็อกที่เลือก"""
        dx = event.x - self.drag_start[0]
        dy = event.y - self.drag_start[1]
        
        # แปลงการเคลื่อนที่ตามมุมกล้อง
        angle_y = math.radians(self.camera_angle_y)
        move_x = dx * math.cos(angle_y) - dy * math.sin(angle_y)
        move_z = dx * math.sin(angle_y) + dy * math.cos(angle_y)
        
        # ปรับความเร็วตามระยะกล้อง
        sensitivity = 0.5 * (self.camera_distance / 800)
        
        # อัปเดตตำแหน่งวัตถุ
        self.selected_block['x'] = self.drag_start[2] + move_x * sensitivity
        self.selected_block['z'] = self.drag_start[4] + move_z * sensitivity
        
        self.redraw_scene()
        self.update_status()

    def stop_drag(self, event):
        """หยุดการลาก"""
        self.drag_start = None

    def start_rotate(self, event):
        """เริ่มต้นการหมุน"""
        self.drag_start = (event.x, event.y)

    def rotate_scene(self, event):
        """หมุนฉาก"""
        if self.drag_start:
            dx = event.x - self.drag_start[0]
            dy = event.y - self.drag_start[1]
            
            # หมุนแกน Y (แนวนอน)
            self.camera_angle_y += dx * self.rotation_speed
            
            # หมุนแกน X (แนวตั้ง) - จำกัดมุมไม่ให้เกิน 90 องศา
            new_angle_x = self.camera_angle_x + dy * self.rotation_speed
            self.camera_angle_x = max(-90, min(90, new_angle_x))
            
            self.redraw_scene()
            self.drag_start = (event.x, event.y)
            self.update_status()

    def stop_rotate(self, event):
        """หยุดการหมุน"""
        self.drag_start = None

    def zoom_scene(self, event):
        """ซูมฉาก"""
        if event.delta > 0:
            self.camera_distance = max(100, self.camera_distance - 50)
        else:
            self.camera_distance = min(2000, self.camera_distance + 50)
        
        self.redraw_scene()
        self.update_status()

    def rotate_scene_key(self, dx, dy):
        """หมุนฉากด้วยคีย์บอร์ด"""
        self.camera_angle_y += dx
        self.camera_angle_x += dy
        self.redraw_scene()
        self.update_status()

    def zoom_scene_key(self, delta):
        """ซูมฉากด้วยคีย์บอร์ด"""
        self.camera_distance = max(100, min(2000, self.camera_distance + delta))
        self.redraw_scene()
        self.update_status()

    def draw_block(self, block):
        """วาดบล็อกเดียว"""
        size = block["size"]
        points = []
        for dx in [-size, size]:
            for dy in [-size, size]:
                for dz in [-size, size]:
                    points.append((block["x"]+dx, block["y"]+dy, block["z"]+dz))
        
        points_2d = []
        for point in points:
            x2d, y2d, _ = self.project_3d_to_2d(*point)
            points_2d.extend([x2d, y2d])
        
        faces = [
            [0,1,3,2], [4,5,7,6], [0,1,5,4],
            [2,3,7,6], [0,2,6,4], [1,3,7,5]
        ]
        
        for face in faces:
            face_points = [points_2d[i] for idx in face for i in (idx*2, idx*2+1)]
            
            # กำหนดสีสำหรับแต่ละด้าน
            face_colors = [
                self.adjust_color(block["color"], 0.7),  # ด้านหลัง
                self.adjust_color(block["color"], 1.0),  # ด้านหน้า
                self.adjust_color(block["color"], 0.5),  # ด้านล่าง
                self.adjust_color(block["color"], 0.8),  # ด้านบน
                self.adjust_color(block["color"], 0.6),  # ด้านซ้าย
                self.adjust_color(block["color"], 0.9)   # ด้านขวา
            ]
            
            self.grid_canvas.create_polygon(
                face_points,
                fill=face_colors[faces.index(face)],
                outline="#ffffff",
                width=1,
                tags=(f"block_{block['id']}", "3d_block")
            )
        
        # วาดข้อความ
        text_x, text_y, _ = self.project_3d_to_2d(
            block["x"], block["y"], block["z"]+size
        )
        self.grid_canvas.create_text(
            text_x, text_y,
            text=block["text"],
            fill="white",
            font=("Tahoma", 10),
            tags=(f"text_{block['id']}", "3d_text")
        )
        
        # ถ้าเป็นบล็อกที่เลือก ให้วาดเส้นขอบ
        if block == self.selected_block:
            for face in faces:
                face_points = [points_2d[i] for idx in face for i in (idx*2, idx*2+1)]
                self.grid_canvas.create_polygon(
                    face_points,
                    outline="#ffff00",
                    width=3,
                    tags=(f"sel_{block['id']}", "selection")
                )

    def adjust_color(self, color, factor):
        """ปรับสีตามด้านของบล็อก"""
        rgb = tuple(int(color[i+1:i+3], 16) for i in (0, 2, 4))
        new_rgb = tuple(min(255, max(0, int(c * factor))) for c in rgb)
        return "#{:02x}{:02x}{:02x}".format(*new_rgb)

    def redraw_scene(self):
        """วาดฉากใหม่ทั้งหมด"""
        self.grid_canvas.delete("all")
        
        if self.show_grid:
            self.draw_3d_grid()
        
        if self.show_axes:
            self.draw_3d_axes()
        
        # วาดบล็อกทั้งหมดใหม่ (เรียงตามระยะ Z)
        for block in sorted(self.blocks, key=lambda b: -b['z']):
            self.draw_block(block)

    def log_to_terminal(self, message):
        """แสดงข้อความใน Terminal"""
        self.terminal.insert(tk.END, message + "\n")
        self.terminal.see(tk.END)

    def update_status(self):
        """อัพเดต Status Bar"""
        status = f"พร้อม | มุมกล้อง: X={self.camera_angle_x:.1f}° Y={self.camera_angle_y:.1f}° | ระยะทาง: {self.camera_distance}"
        if self.selected_block:
            status += f" | เลือก: {self.selected_block['text']} (X={self.selected_block['x']:.1f}, Z={self.selected_block['z']:.1f})"
        self.status_var.set(status)

    def toggle_axes(self):
        """สลับการแสดงแกน"""
        self.show_axes = not self.show_axes
        self.redraw_scene()

    def toggle_grid(self):
        """สลับการแสดงกริด"""
        self.show_grid = not self.show_grid
        self.redraw_scene()

    def clear_scene(self):
        """ล้างฉากทั้งหมด"""
        self.blocks = []
        self.selected_block = None
        self.grid_canvas.delete("all")
        self.redraw_scene()
        
        # ล้าง Explorer
        for item in self.tree.get_children("main_scene"):
            if item.startswith("block_"):
                self.tree.delete(item)
        
        self.log_to_terminal("ล้างฉากเรียบร้อย")

    def add_ai_block(self):
        """เพิ่มบล็อก AI"""
        self.add_3d_block(
            x=0, y=50, z=0,
            size=40,
            color="#4e88e3",
            text="บล็อก AI"
        )

    def add_3d_model(self):
        """เพิ่มโมเดล 3D"""
        self.add_3d_block(
            x=100, y=30, z=-50,
            size=35,
            color="#e34e4e",
            text="โมเดล 3D"
        )

    def new_project(self):
        """สร้างโปรเจคใหม่"""
        if messagebox.askyesno("สร้างใหม่", "คุณต้องการสร้างโปรเจคใหม่หรือไม่?\nการเปลี่ยนแปลงทั้งหมดจะไม่ถูกบันทึก"):
            self.clear_scene()
            self.log_to_terminal("สร้างโปรเจคใหม่เรียบร้อย")

    def open_project(self):
        """เปิดโปรเจค"""
        messagebox.showinfo("เปิดโปรเจค", "คุณเลือกเปิดโปรเจค (ฟังก์ชันนี้ยังไม่สมบูรณ์)")

    def show_about(self):
        """แสดงข้อมูลเกี่ยวกับโปรแกรม"""
        about_msg = """GaragexAI Studio - โหมด 3D
เวอร์ชัน 1.0
        
พัฒนาโดย GaragexAI
© 2023 ทุกสิทธิ์ถูกสงวนไว้"""
        messagebox.showinfo("เกี่ยวกับ", about_msg)

if __name__ == "__main__":
    root = tk.Tk()
    
    # ตั้งค่าสไตล์
    style = ttk.Style()
    style.theme_use('clam')
    
    style.configure("TButton", 
        background="#333", 
        foreground="white",
        padding=5,
        font=("Tahoma", 10),
        borderwidth=2,
        relief=tk.RAISED
    )
    
    style.map("TButton",
        background=[('active', '#007acc')],
        foreground=[('active', 'white')]
    )
    
    app = AIStudioPrototype(root)
    root.mainloop()