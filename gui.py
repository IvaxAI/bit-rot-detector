import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import detector

class BitRotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bit Rot Detector 🛡️")
        self.root.geometry("700x500")

        # Controls
        self.frame_top = tk.Frame(root)
        self.frame_top.pack(pady=20)

        self.btn_files = tk.Button(self.frame_top, text="Select Files", command=self.select_files)
        self.btn_files.pack(side=tk.LEFT, padx=10)

        self.btn_dir = tk.Button(self.frame_top, text="Scan Directory", command=self.select_directory)
        self.btn_dir.pack(side=tk.LEFT, padx=10)

        self.var_recursive = tk.BooleanVar(value=True)
        self.chk_recursive = tk.Checkbutton(self.frame_top, text="Recursive", variable=self.var_recursive)
        self.chk_recursive.pack(side=tk.LEFT, padx=10)

        # Output
        self.text_output = tk.Text(root, height=20, width=80)
        self.text_output.pack(pady=10, padx=10)

    def log(self, message):
        self.text_output.insert(tk.END, message + "\n")
        self.text_output.see(tk.END)

    def select_files(self):
        files = filedialog.askopenfilenames(title="Select Video Files")
        if files:
            self.start_scan(files)

    def select_directory(self):
        directory = filedialog.askdirectory(title="Select Directory to Scan")
        if directory:
            files = detector.scan_directory(directory, self.var_recursive.get())
            self.start_scan(files)

    def start_scan(self, files):
        self.text_output.delete(1.0, tk.END)
        self.log(f"Starting Scan for {len(files)} files...")
        threading.Thread(target=self.run_scan, args=(files,), daemon=True).start()

    def run_scan(self, files):
        corrupt_count = 0
        for file in files:
            self.log(f"Scanning: {os.path.basename(file)}")
            status, detail = detector.check_video_integrity(file)
            self.log(f"  Result: [{status}]")
            if status == "Corrupt":
                corrupt_count += 1
                if detail:
                    self.log(f"  Error: {detail[:100]}...")
        
        self.log(f"\n--- Scan Complete ---")
        self.log(f"Total Files: {len(files)}")
        self.log(f"Healthy: {len(files) - corrupt_count}")
        self.log(f"Corrupt: {corrupt_count}")
        
        if corrupt_count > 0:
            messagebox.showwarning("Scan Complete", f"Found {corrupt_count} potentially corrupt files!")
        else:
            messagebox.showinfo("Scan Complete", "All files appear healthy!")

if __name__ == "__main__":
    root = tk.Tk()
    app = BitRotGUI(root)
    root.mainloop()
