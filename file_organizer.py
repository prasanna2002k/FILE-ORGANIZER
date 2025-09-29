zaalima file automation project..  code  
import os
import shutil
import logging
import tkinter as tk
from tkinter import filedialog, messagebox

# -----------------------------
# Logging Configuration
# -----------------------------
log_file = "file_organizer.txt"  # logs will save in same folder as script
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Categories and file extensions
CATEGORIES = {
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Music": [".mp3", ".wav", ".aac"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Others": []
}

# -----------------------------
# File Organizer Logic
# -----------------------------
def organize_files(source_dir, target_dir=None):
    try:
        for filename in os.listdir(source_dir):
            file_path = os.path.join(source_dir, filename)

            if os.path.isfile(file_path):
                _, ext = os.path.splitext(filename)
                moved = False

                for category, extensions in CATEGORIES.items():
                    if ext.lower() in extensions:
                        # Decide destination folder
                        if target_dir:
                            category_folder = os.path.join(target_dir, category)
                        else:
                            category_folder = os.path.join(source_dir, category)

                        os.makedirs(category_folder, exist_ok=True)
                        shutil.move(file_path, os.path.join(category_folder, filename))
                        logging.info(f"Moved: {filename} -> {category_folder}")
                        moved = True
                        break

                if not moved:  # goes to "Others"
                    if target_dir:
                        other_folder = os.path.join(target_dir, "Others")
                    else:
                        other_folder = os.path.join(source_dir, "Others")

                    os.makedirs(other_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(other_folder, filename))
                    logging.info(f"Moved: {filename} -> {other_folder}")

        messagebox.showinfo("Success", "Files organized successfully!")
        messagebox.showinfo("Log File", f"Logs saved in:\n{os.path.abspath(log_file)}")

    except Exception as e:
        logging.error(f"Error: {e}")
        messagebox.showerror("Error", str(e))

# -----------------------------
# Tkinter GUI
# -----------------------------
def select_source():
    path = filedialog.askdirectory(title="Select Source Folder")
    if path:
        source_entry.delete(0, tk.END)
        source_entry.insert(0, path)

def select_target():
    path = filedialog.askdirectory(title="Select Target Folder")
    if path:
        target_entry.delete(0, tk.END)
        target_entry.insert(0, path)

def run_organizer():
    source = source_entry.get()
    target = target_entry.get().strip()

    if not source:
        messagebox.showerror("Error", "Please select a source folder!")
        return

    if target:
        organize_files(source, target)  # Between two folders
    else:
        organize_files(source)  # Within same folder

# -----------------------------
# GUI Layout
# -----------------------------
root = tk.Tk()
root.title("File Organizer")
root.geometry("500x250")

tk.Label(root, text="Source Folder:").pack(pady=5)
source_entry = tk.Entry(root, width=50)
source_entry.pack()
tk.Button(root, text="Browse", command=select_source).pack(pady=5)

tk.Label(root, text="Target Folder (Optional):").pack(pady=5)
target_entry = tk.Entry(root, width=50)
target_entry.pack()
tk.Button(root, text="Browse", command=select_target).pack(pady=5)

tk.Button(root, text="Organize Files", command=run_organizer, bg="green", fg="white").pack(pady=20)

root.mainloop()
