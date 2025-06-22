import tkinter as tk
from tkinter import Menu, Text

class AIStudioPrototype:
    def __init__(self, root):
        self.root = root  # สร้างหน้าต่างหลักของโปรแกรม
        self.root.title("GaragexAI Studio")  # ตั้งชื่อหน้าต่าง
        self.root.geometry("1200x800")  # กำหนดขนาดหน้าต่าง
        self.root.configure(bg="#2e2e2e")  # สีพื้นหลัง

        # สร้างส่วนต่าง ๆ ของ UI
        self.create_menu()
        self.create_layout()
        self.create_toolbox()
        self.create_explorer()
        self.create_terminal()

    def create_menu(self):
        menubar = Menu(self.root)  # สร้างแถบเมนูด้านบน
        for menu_name in ["Home", "Model", "Input / Output", "Logic Block", "View", "Run"]:
            menubar.add_command(label=menu_name)  # เพิ่มแต่ละเมนู
        self.root.config(menu=menubar)  # ผูกกับหน้าต่างหลัก

    def create_layout(self):
        self.main_frame = tk.Frame(self.root, bg="#2e2e2e")  # กรอบหลักทั้งหมด
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.toolbox_frame = tk.Frame(self.main_frame, width=150, bg="#1e1e1e")  # แถบเครื่องมือซ้าย
        self.toolbox_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.canvas_frame = tk.Frame(self.main_frame, bg="#3e3e3e")  # ฉากตรงกลาง
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.explorer_frame = tk.Frame(self.main_frame, width=150, bg="#1e1e1e")  # แถบขวา
        self.explorer_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.grid_canvas = tk.Canvas(self.canvas_frame, bg="#3e3e3e")  # Canvas วาง object
        self.grid_canvas.pack(fill=tk.BOTH, expand=True)
        self.draw_grid()  # วาดเส้น grid

    def draw_grid(self):
        grid_size = 25
        for i in range(0, 2000, grid_size):
            self.grid_canvas.create_line([(i, 0), (i, 2000)], fill="#555555")  # เส้นตั้ง
            self.grid_canvas.create_line([(0, i), (2000, i)], fill="#555555")  # เส้นนอน

    def create_toolbox(self):
        label = tk.Label(self.toolbox_frame, text="Toolbox", fg="white", bg="#1e1e1e", font=("Arial", 12, "bold"))
        label.pack(pady=10)

        tools = ["AI", "Text", "Voice Input", "Image", "Webcam", "File Upload"]
        for tool in tools:
            btn = tk.Button(self.toolbox_frame, text=tool, width=15, bg="#333", fg="white", relief=tk.FLAT)
            btn.pack(pady=5)

    def create_explorer(self):
        label = tk.Label(self.explorer_frame, text="Explorer", fg="white", bg="#1e1e1e", font=("Arial", 12, "bold"))
        label.pack(pady=10)
        file_icon = tk.Label(self.explorer_frame, text="📄", bg="#1e1e1e", fg="white", font=("Arial", 20))
        file_icon.pack(pady=5)

    def create_terminal(self):
        self.terminal = Text(self.root, height=6, bg="black", fg="lime", insertbackground="white")
        self.terminal.pack(fill=tk.X)
        self.terminal.insert(tk.END, "Terminal ready...\n")

# รันโปรแกรม
if __name__ == "__main__":
    root = tk.Tk()
    app = AIStudioPrototype(root)
    root.mainloop()