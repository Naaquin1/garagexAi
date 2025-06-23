import tkinter as tk
from tkinter import Menu, Text

class AIStudioPrototype:
    def __init__(self, root):
        self.root = root
        self.root.title("GaragexAI Studio")
        self.root.geometry("1200x800")
        self.root.configure(bg="#2e2e2e")

        self.create_menu()
        self.create_layout()
        self.create_toolbox()
        self.create_explorer()
        self.create_terminal()

    def create_menu(self):
        menubar = Menu(self.root)
        for menu_name in ["Home", "Model", "Input / Output", "Logic Block", "View", "Run"]:
            menubar.add_command(label=menu_name)
        self.root.config(menu=menubar)

    def create_layout(self):
        self.main_frame = tk.Frame(self.root, bg="#2e2e2e")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.toolbox_frame = tk.Frame(self.main_frame, width=150, bg="#1e1e1e")
        self.toolbox_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.canvas_frame = tk.Frame(self.main_frame, bg="#3e3e3e")
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.explorer_frame = tk.Frame(self.main_frame, width=150, bg="#1e1e1e")
        self.explorer_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.grid_canvas = tk.Canvas(self.canvas_frame, bg="#3e3e3e")
        self.grid_canvas.pack(fill=tk.BOTH, expand=True)
        self.draw_grid()

    def draw_grid(self):
        grid_size = 25
        for i in range(0, 2000, grid_size):
            self.grid_canvas.create_line([(i, 0), (i, 2000)], fill="#555555")
            self.grid_canvas.create_line([(0, i), (2000, i)], fill="#555555")

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

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = AIStudioPrototype(root)
    root.mainloop()