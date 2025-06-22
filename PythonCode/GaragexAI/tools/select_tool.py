import tkinter as tk
from tkinter import ttk
from tkinter import Menu, Text
from tools.select_tool import SelectTool # type: ignore

class AIStudioPrototype:
    def __init__(self, root):
        self.root = root
        self.root.title("GaragexAI Studio")
        self.root.geometry("1400x900")
        self.root.configure(bg="#1e1e1e")

        self.setup_style()
        self.create_menu()
        self.create_layout()
        self.create_toolbox()
        self.create_explorer()
        self.create_terminal()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TNotebook", background="#2e2e2e", borderwidth=0)
        style.configure("TNotebook.Tab", background="#444", foreground="white", padding=(10, 5), font=("Segoe UI", 10))
        style.map("TNotebook.Tab", background=[("selected", "#666")])

        style.configure("TButton", font=("Segoe UI", 10), padding=6, relief="flat")
        style.configure("TLabel", background="#1e1e1e", foreground="white", font=("Segoe UI", 10))

    def create_menu(self):
        menubar = Menu(self.root, bg="#2e2e2e", fg="white", tearoff=0)
        file_menu = Menu(menubar, tearoff=0, bg="#2e2e2e", fg="white")
        file_menu.add_command(label="New Project")
        file_menu.add_command(label="Open")
        file_menu.add_command(label="Save")
        menubar.add_cascade(label="File", menu=file_menu)

        for menu in ["Model", "Input / Output", "Logic", "View", "Run"]:
            menubar.add_command(label=menu)

        self.root.config(menu=menubar)

    def create_layout(self):
        self.main_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.toolbox_frame = tk.Frame(self.main_frame, width=180, bg="#252526")
        self.toolbox_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.explorer_frame = tk.Frame(self.main_frame, width=200, bg="#252526")
        self.explorer_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.center_frame = tk.Frame(self.main_frame, bg="#1e1e1e")
        self.center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Canvas with Tabs
        self.notebook = ttk.Notebook(self.center_frame)
        self.canvas_tab = tk.Frame(self.notebook, bg="#2e2e2e")
        self.notebook.add(self.canvas_tab, text="Main Scene")
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.grid_canvas = tk.Canvas(self.canvas_tab, bg="#2e2e2e", highlightthickness=0)
        self.grid_canvas.pack(fill=tk.BOTH, expand=True)
        self.grid_canvas.bind("<Configure>", self.draw_grid)

    def draw_grid(self, event=None):
        self.grid_canvas.delete("grid_line")
        grid_size = 30
        w = self.grid_canvas.winfo_width()
        h = self.grid_canvas.winfo_height()
        for i in range(0, w, grid_size):
            self.grid_canvas.create_line([(i, 0), (i, h)], tag="grid_line", fill="#444444")
        for i in range(0, h, grid_size):
            self.grid_canvas.create_line([(0, i), (w, i)], tag="grid_line", fill="#444444")

    def create_toolbox(self):
        title = tk.Label(self.toolbox_frame, text="🧰 Toolbox", bg="#252526", fg="white", font=("Segoe UI", 12, "bold"))
        title.pack(pady=(10, 20))

        self.select_tool = SelectTool(self.grid_canvas, self.log_to_terminal)

        tools = [
            ("🔲 Select", self.select_tool.activate),
            ("✏️ Text Block", self.placeholder_action),
            ("🎙️ Voice Input", self.placeholder_action),
            ("🖼️ Image", self.placeholder_action),
            ("📷 Webcam", self.placeholder_action),
            ("📁 Upload", self.placeholder_action)
        ]

        for name, cmd in tools:
            btn = ttk.Button(self.toolbox_frame, text=name, command=cmd)
            btn.pack(pady=8, padx=10, fill=tk.X)

    def create_explorer(self):
        title = tk.Label(self.explorer_frame, text="🗂 Explorer", bg="#252526", fg="white", font=("Segoe UI", 12, "bold"))
        title.pack(pady=(10, 20))

        files = ["main.ai", "voice_input.py", "assets/image1.png", "data.csv"]
        for file in files:
            label = tk.Label(self.explorer_frame, text=f"📄 {file}", anchor="w", bg="#252526", fg="lightgray", padx=10)
            label.pack(fill=tk.X, pady=2)

    def create_terminal(self):
        terminal_frame = tk.Frame(self.root, height=150, bg="black")
        terminal_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.terminal = Text(terminal_frame, bg="black", fg="lime", insertbackground="white", height=10, font=("Consolas", 10))
        self.terminal.pack(fill=tk.BOTH, expand=True)
        self.terminal.insert(tk.END, "GaragexAI Terminal > Ready...\n")

    def placeholder_action(self):
        self.terminal.insert(tk.END, "[Info] Feature coming soon...\n")
        self.terminal.see(tk.END)

    def log_to_terminal(self, message):
        self.terminal.insert(tk.END, message + "\n")
        self.terminal.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = AIStudioPrototype(root)
    root.mainloop()