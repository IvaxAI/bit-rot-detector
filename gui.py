import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import detector  # Import our core logic

class BitRotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bit Rot Detector 🛡️")
        self.root.geometry("600x400")

        # Layout
        self.label = tk.Label(root, text="Select or Drag & Drop Video Files", font=("Arial", 14))
        self.label.pack(pady=20)

        self.btn_select = tk.Button(root, text="Select Files", command=self.select_files)
        self.btn_select.pack(pady=10)

        self.text_output = tk.Text(root, height=15, width=70)
        self.text_output.pack(pady=10)

    def log(self, message):
        self.text_output.insert(tk.END, message + "\n")
        self.text_output.see(tk.END)

    def select_files(self):
        files = filedialog.askopenfilenames(title="Select Video Files")
        if files:
            self.text_output.delete(1.0, tk.END)
            self.log(f"Starting Scan for {len(files)} files...")
            threading.Thread(target=self.run_scan, args=(files,), daemon=True).start()

    def run_scan(self, files):
        for file in files:
            self.log(f"Scanning: {file}")
            status, detail = detector.check_video_integrity(file)
            self.log(f"  Result: [{status}]")
            if detail:
                self.log(f"  Error: {detail[:100]}...")
        self.log("\n--- Scan Complete ---")
        messagebox.showinfo("Done", "Scanning complete!")

if __name__ == "__main__":
    root = tk.Tk()
    app = BitRotGUI(root)
    root.mainloop()
