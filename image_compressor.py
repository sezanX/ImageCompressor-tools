import os
import csv
import time
from PIL import Image
import glob
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style
from threading import Thread

# ================= CONFIGURABLES =================
TARGET_SIZE_KB = 250           # Default target size
EXCLUDE_FILE = "exclude.txt"   # List filenames (one per line) to exclude
CONFIG_FILE = "config.csv"     # Optional: per-file target size (filename, target_kb)
REPORT_FILE = "compression_report.csv"
# ================================================

class ImageCompressorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Compressor Pro")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Variables
        self.input_dir = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.target_size_kb = tk.IntVar(value=TARGET_SIZE_KB)
        self.excluded_files = set()
        self.per_file_config = {}
        
        self.setup_ui()
        
    def setup_ui(self):
        style = Style(theme="flatly")  # Modern theme
        
        # Main container
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Image Compressor Pro", font=("Helvetica", 24, "bold"), bootstyle="primary")
        title_label.pack(pady=(0, 20))
        
        # Input Folder Selection
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill="x", pady=5)
        ttk.Label(input_frame, text="Input Folder:", font=("Helvetica", 12)).pack(side="left", padx=(0, 10))
        input_entry = ttk.Entry(input_frame, textvariable=self.input_dir, state="readonly", bootstyle="secondary")
        input_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ttk.Button(input_frame, text="Browse", command=self.select_input_dir, bootstyle="primary").pack(side="right")
        
        # Output Folder Selection
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(fill="x", pady=5)
        ttk.Label(output_frame, text="Output Folder:", font=("Helvetica", 12)).pack(side="left", padx=(0, 10))
        output_entry = ttk.Entry(output_frame, textvariable=self.output_dir, state="readonly", bootstyle="secondary")
        output_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ttk.Button(output_frame, text="Browse", command=self.select_output_dir, bootstyle="primary").pack(side="right")
        
        # Target Size
        target_frame = ttk.Frame(main_frame)
        target_frame.pack(fill="x", pady=5)
        ttk.Label(target_frame, text="Target Size (KB):", font=("Helvetica", 12)).pack(side="left", padx=(0, 10))
        target_entry = ttk.Entry(target_frame, textvariable=self.target_size_kb, width=10, bootstyle="secondary")
        target_entry.pack(side="left")
        
        # Start Button
        self.start_button = ttk.Button(main_frame, text="Start Compression", command=self.start_compression, 
                                     bootstyle="success-outline", style="TButton", padding=10)
        self.start_button.pack(pady=20)
        
        # Progress Bar
        self.progress = ttk.Progressbar(main_frame, orient="horizontal", length=500, mode="determinate", bootstyle="success-striped")
        self.progress.pack(pady=10)
        
        # Log Area
        log_label = ttk.Label(main_frame, text="Log:", font=("Helvetica", 12, "bold"))
        log_label.pack(anchor="w", pady=(10, 0))
        self.log_text = ttk.ScrolledText(main_frame, height=15, font=("Consolas", 10), state="disabled", wrap="word")
        self.log_text.pack(fill="both", expand=True, pady=5)
        
        # Footer (always visible)
        footer_frame = ttk.Frame(self.root)  # Moved to root for bottom anchoring
        footer_frame.pack(side="bottom", fill="x", pady=5)
        footer_label = ttk.Label(footer_frame, text="Developed by SezanX", font=("Helvetica", 10), 
                               bootstyle="info", cursor="hand2")
        footer_label.pack(side="left", padx=5)
        footer_label.bind("<Button-1>", lambda e: self.open_github())
        ttk.Label(footer_frame, text=" | ", bootstyle="secondary").pack(side="left")
        footer_link = ttk.Label(footer_frame, text="https://github.com/sezanX", font=("Helvetica", 10), 
                              bootstyle="info", cursor="hand2")
        footer_link.pack(side="left", padx=5)
        footer_link.bind("<Button-1>", lambda e: self.open_github())
        ttk.Label(footer_frame, text=" | ", bootstyle="secondary").pack(side="left")
        ttk.Label(footer_frame, text="© 2025 Sezan Mahmood", font=("Helvetica", 10), bootstyle="secondary").pack(side="right", padx=5)
        
    def open_github(self):
        import webbrowser
        webbrowser.open("https://github.com/sezanX")
    
    def log_message(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")
        self.root.update_idletasks()
    
    def select_input_dir(self):
        dir_path = filedialog.askdirectory(title="Select Input Folder")
        if dir_path:
            self.input_dir.set(dir_path)
            self.log_message(f"Input folder selected: {dir_path}")
    
    def select_output_dir(self):
        dir_path = filedialog.askdirectory(title="Select Output Folder")
        if dir_path:
            self.output_dir.set(dir_path)
            self.log_message(f"Output folder selected: {dir_path}")
    
    def load_exclusion_list(self):
        exclude_path = os.path.join(self.input_dir.get(), EXCLUDE_FILE)
        if not os.path.exists(exclude_path):
            self.log_message(f"No exclusion file found at {exclude_path}")
            return set()
        try:
            with open(exclude_path, 'r', encoding='utf-8') as f:
                return set(line.strip() for line in f if line.strip())
        except Exception as e:
            self.log_message(f"Error reading {exclude_path}: {e}")
            return set()
    
    def load_config(self):
        config_path = os.path.join(self.input_dir.get(), CONFIG_FILE)
        config = {}
        if not os.path.exists(config_path):
            self.log_message(f"No config file found at {config_path}")
            return config
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    filename = row['filename'].strip()
                    try:
                        target_kb = int(row['target_kb'])
                        config[filename] = target_kb
                    except:
                        self.log_message(f"Invalid config for {filename}, skipping...")
        except Exception as e:
            self.log_message(f"Error reading {config_path}: {e}")
        return config
    
    def compress_image(self, input_path, output_path, target_size_kb=250, step=5):
        try:
            img = Image.open(input_path)
            original_format = img.format or "JPEG"
            original_size = img.size
            original_filesize_kb = os.path.getsize(input_path) / 1024

            if original_format == 'PNG' and original_filesize_kb > target_size_kb:
                img = img.convert("RGB")
                save_format = "JPEG"
                output_path = os.path.splitext(output_path)[0] + ".jpg"
            else:
                save_format = original_format if original_format in ["JPEG", "WEBP"] else "JPEG"

            quality = 95
            min_quality = 10

            while quality >= min_quality:
                img.save(output_path, format=save_format, quality=quality, optimize=True)
                current_size_kb = os.path.getsize(output_path) / 1024

                if current_size_kb <= target_size_kb:
                    break
                quality -= step

            # Final check & restore resolution if needed
            img_final = Image.open(output_path)
            if img_final.size != original_size:
                img_final = img_final.resize(original_size, Image.LANCZOS)
                img_final.save(output_path, format=save_format, quality=quality, optimize=True)

            final_size_kb = os.path.getsize(output_path) / 1024
            compression_percent = 100 * (1 - final_size_kb / original_filesize_kb) if original_filesize_kb > 0 else 0

            return {
                "success": True,
                "original_size_kb": round(original_filesize_kb, 2),
                "final_size_kb": round(final_size_kb, 2),
                "quality_used": quality,
                "compression_percent": round(compression_percent, 1),
                "resolution": f"{original_size[0]}x{original_size[1]}",
                "format": save_format
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "original_size_kb": 0,
                "final_size_kb": 0,
                "quality_used": 0,
                "compression_percent": 0,
                "resolution": "N/A",
                "format": "N/A"
            }
    
    def write_report(self, report_data, output_dir):
        report_path = os.path.join(output_dir, REPORT_FILE)
        try:
            with open(report_path, 'w', newline='', encoding='utf-8') as f:
                fieldnames = [
                    "filename", "success", "original_size_kb", "final_size_kb",
                    "compression_percent", "quality_used", "resolution", "format", "error"
                ]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for row in report_data:
                    writer.writerow(row)
            self.log_message(f"Report saved to: {report_path}")
        except Exception as e:
            self.log_message(f"Error writing report: {e}")
    
    def start_compression(self):
        input_dir = self.input_dir.get()
        output_dir = self.output_dir.get()
        try:
            target_size = self.target_size_kb.get()
            if target_size <= 0:
                raise ValueError("Target size must be positive.")
        except:
            messagebox.showerror("Error", "Please enter a valid positive number for target size.")
            return
        
        if not input_dir or not output_dir:
            messagebox.showerror("Error", "Please select both input and output folders.")
            return
        
        if not os.path.exists(input_dir):
            messagebox.showerror("Error", "Input folder does not exist.")
            return
        
        # Disable start button
        self.start_button.config(state="disabled")
        
        # Start in thread to avoid freezing UI
        thread = Thread(target=self.run_compression, args=(input_dir, output_dir))
        thread.daemon = True
        thread.start()
    
    def run_compression(self, input_dir, output_dir):
        start_time = time.time()
        
        self.log_message("Starting compression...")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Load configs
        self.excluded_files = self.load_exclusion_list()
        self.per_file_config = self.load_config()
        
        # Get image files
        extensions = ["*.jpg", "*.jpeg", "*.png", "*.webp"]
        image_files = []
        for ext in extensions:
            image_files.extend(glob.glob(os.path.join(input_dir, ext)))
        
        # Filter out excluded files
        filtered_files = [f for f in image_files if os.path.basename(f) not in self.excluded_files]
        
        total_files = len(filtered_files)
        if total_files == 0:
            self.log_message(f"No images found in {input_dir}. Please add images (jpg, jpeg, png, webp).")
            self.start_button.config(state="normal")
            return
        
        self.log_message(f"Processing {total_files} images...")
        self.log_message(f"Target: {self.target_size_kb.get()} KB")
        if self.excluded_files:
            self.log_message(f"Excluded: {len(self.excluded_files)} files")
        
        report_data = []
        success_count = 0
        
        for idx, img_path in enumerate(filtered_files, 1):
            filename = os.path.basename(img_path)
            output_path = os.path.join(output_dir, filename)
            
            # Override target size if config exists
            target_kb = self.per_file_config.get(filename, self.target_size_kb.get())
            
            self.log_message(f"[{idx}/{total_files}] {filename} (Target: {target_kb} KB)")
            
            result = self.compress_image(img_path, output_path, target_size_kb=target_kb)
            
            if result["success"]:
                self.log_message(f"  ✅ {result['final_size_kb']} KB | Quality: {result['quality_used']} | Saved {result['compression_percent']}%")
                success_count += 1
            else:
                self.log_message(f"  ❌ Failed: {result['error']}")
            
            # Add to report
            report_data.append({
                "filename": filename,
                "success": result["success"],
                "original_size_kb": result["original_size_kb"],
                "final_size_kb": result["final_size_kb"],
                "compression_percent": result["compression_percent"],
                "quality_used": result["quality_used"],
                "resolution": result["resolution"],
                "format": result["format"],
                "error": result.get("error", "")
            })
            
            # Update progress
            progress_value = (idx / total_files) * 100
            self.progress["value"] = progress_value
            self.root.update_idletasks()
        
        # Generate report
        self.write_report(report_data, output_dir)
        
        # Summary
        end_time = time.time()
        total_time = round(end_time - start_time, 2)
        self.log_message(f"DONE! {success_count}/{total_files} succeeded in {total_time} seconds.")
        self.log_message(f"Output folder: {output_dir}")
        
        # Re-enable start button
        self.start_button.config(state="normal")
        self.progress["value"] = 0

def main():
    root = ttk.Window()
    app = ImageCompressorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()