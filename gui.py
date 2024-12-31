import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedTk
from compression import compress_files
from converters.pdf_converter import pdf_to_docx, docx_to_pdf
from converters.image_converter import convert_image_format
import threading
from pathlib import Path
import sv_ttk

class HoverButton(tk.Canvas):
    def __init__(self, parent, text, command=None, width=200, height=40, corner_radius=10, **kwargs):
        # Initialize with explicit background color instead of parent's bg
        super().__init__(parent, width=width, height=height, highlightthickness=0,
                        background='#1e1e1e', **kwargs)
        self.command = command
        self.corner_radius = corner_radius
        
        # Colors
        self.normal_color = "#2962ff"
        self.hover_color = "#1565c0"
        self.click_color = "#0d47a1"
        self.current_color = self.normal_color
        
        # Text properties
        self.text = text
        self.text_color = "white"
        
        # Draw initial button
        self._draw()
        
        # Bind events
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _draw(self):
        self.delete("all")
        
        # Draw button background
        self.create_rounded_rect(0, 0, self.winfo_width(), self.winfo_height(), 
                               self.corner_radius, fill=self.current_color)
        
        # Draw text
        self.create_text(self.winfo_width()/2, self.winfo_height()/2, 
                        text=self.text, fill=self.text_color, 
                        font=("Segoe UI", 10, "bold"))

    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def _on_enter(self, e):
        self.current_color = self.hover_color
        self._draw()

    def _on_leave(self, e):
        self.current_color = self.normal_color
        self._draw()

    def _on_press(self, e):
        self.current_color = self.click_color
        self._draw()

    def _on_release(self, e):
        self.current_color = self.hover_color
        self._draw()
        if self.command:
            self.command()

class ModernFrame(ttk.Frame):
    def __init__(self, parent, title, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Title label
        title_label = ttk.Label(
            self,
            text=title,
            font=("Segoe UI", 12, "bold"),
            padding=(10, 5)
        )
        title_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Content frame
        self.content = ttk.Frame(self)
        self.content.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

class KonvataApp:
    def __init__(self):
        self.root = ThemedTk(theme="equilux")
        self.root.title("KONVATA")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Apply Fluent design
        sv_ttk.set_theme("dark")
        
        # Variables
        self.current_task = tk.StringVar(value="Ready")
        self.progress_var = tk.DoubleVar(value=0)
        
        self.setup_ui()
        self.create_menu()

    def setup_ui(self):
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(
            header_frame,
            text="KONVATA",
            font=("Segoe UI", 32, "bold")
        )
        title_label.pack(anchor="w")
        
        subtitle_label = ttk.Label(
            header_frame,
            text="File Conversion Suite",
            font=("Segoe UI", 12)
        )
        subtitle_label.pack(anchor="w")

        # Create main content area with grid layout
        content = ttk.Frame(main_container)
        content.pack(fill=tk.BOTH, expand=True)
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)

        # Document conversion section
        doc_frame = ModernFrame(content, "Document Conversion")
        doc_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        HoverButton(
            doc_frame.content,
            text="PDF to DOCX",
            command=lambda: self.convert_ui(pdf_to_docx, [("PDF files", "*.pdf")])
        ).pack(pady=5, padx=10, fill=tk.X)
        
        HoverButton(
            doc_frame.content,
            text="DOCX to PDF",
            command=lambda: self.convert_ui(docx_to_pdf, [("Word files", "*.docx")])
        ).pack(pady=5, padx=10, fill=tk.X)

        # Image conversion section
        img_frame = ModernFrame(content, "Image Conversion")
        img_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        HoverButton(
            img_frame.content,
            text="JPEG to PNG",
            command=lambda: self.convert_ui(
                lambda x, y: convert_image_format(x, "png"),
                [("JPEG files", "*.jpg *.jpeg")]
            )
        ).pack(pady=5, padx=10, fill=tk.X)
        
        HoverButton(
            img_frame.content,
            text="PNG to JPEG",
            command=lambda: self.convert_ui(
                lambda x, y: convert_image_format(x, "jpeg"),
                [("PNG files", "*.png")]
            )
        ).pack(pady=5, padx=10, fill=tk.X)

        # Compression section
        comp_frame = ModernFrame(content, "Compression Tools")
        comp_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        HoverButton(
            comp_frame.content,
            text="Compress Files",
            command=self.compress_ui
        ).pack(pady=5, padx=10, fill=tk.X)

        # Status bar
        self.create_status_bar(main_container)

    def create_status_bar(self, parent):
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(20, 0))
        
        # Progress bar
        self.progress = ttk.Progressbar(
            status_frame,
            mode='determinate',
            variable=self.progress_var
        )
        self.progress.pack(fill=tk.X, pady=(0, 5))
        
        # Status label
        self.status_label = ttk.Label(
            status_frame,
            textvariable=self.current_task
        )
        self.status_label.pack(side=tk.LEFT)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Settings", command=self.show_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Documentation", command=self.show_docs)

    def show_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        # Add settings controls here

    def show_about(self):
        messagebox.showinfo(
            "About KONVATA",
            "KONVATA v1.0\nFile Conversion & Compression Suite\n\n" +
            "A powerful tool for all your file conversion needs."
        )

    def show_docs(self):
        # Open documentation in default browser
        pass

    def compress_ui(self):
        files = filedialog.askopenfilenames(
            title="Select Files to Compress",
            filetypes=[("All files", "*.*")]
        )
        if files:
            output = filedialog.asksaveasfilename(
                title="Save Compressed File",
                defaultextension=".zip",
                filetypes=[("ZIP files", "*.zip")]
            )
            if output:
                self.run_task(
                    lambda: compress_files(files, output),
                    "Compressing files..."
                )

    def convert_ui(self, convert_func, filetypes):
        input_file = filedialog.askopenfilename(
            title="Select File to Convert",
            filetypes=filetypes
        )
        if input_file:
            # Suggest output filename based on input
            suggested_name = Path(input_file).stem
            output_ext = ".docx" if "pdf" in filetypes[0][1] else ".pdf"
            if "jpeg" in filetypes[0][1]:
                output_ext = ".png"
            elif "png" in filetypes[0][1]:
                output_ext = ".jpg"
                
            output_file = filedialog.asksaveasfilename(
                title="Save Converted File",
                initialfile=suggested_name + output_ext,
                defaultextension=output_ext
            )
            if output_file:
                self.run_task(
                    lambda: convert_func(input_file, output_file),
                    f"Converting {Path(input_file).name}..."
                )

    def run_task(self, task_func, status_message):
        def task_wrapper():
            try:
                self.current_task.set(status_message)
                self.progress_var.set(0)
                task_func()
                self.progress_var.set(100)
                self.current_task.set("Task completed successfully!")
                messagebox.showinfo("Success", "Operation completed successfully!")
            except Exception as e:
                self.current_task.set("Error occurred!")
                messagebox.showerror("Error", str(e))
            finally:
                self.progress_var.set(0)
                self.current_task.set("Ready")

        thread = threading.Thread(target=task_wrapper)
        thread.daemon = True
        thread.start()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = KonvataApp()
    app.run()