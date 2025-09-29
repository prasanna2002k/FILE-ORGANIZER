import os
import shutil
import logging
from datetime import datetime

# -----------------------------
# Configuration
# -----------------------------

# Categories and their file extensions
CATEGORIES = {
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Videos": [".mp4", ".mkv", ".flv", ".avi"],
    "Music": [".mp3", ".wav", ".aac"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Others": []
}

# Set up logging
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, f"file_organizer_{datetime.now().date()}.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# -----------------------------
# Helper Functions
# -----------------------------

def get_category(file_name):
    """Return the category of a file based on extension."""
    ext = os.path.splitext(file_name)[1].lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"


def organize_files(source_dir, target_dir):
    """Organize files from source_dir into target_dir based on file type."""
    try:
        if not os.path.exists(source_dir):
            logging.error(f"Source directory does not exist: {source_dir}")
            return

        os.makedirs(target_dir, exist_ok=True)

        for file in os.listdir(source_dir):
            file_path = os.path.join(source_dir, file)

            if os.path.isfile(file_path):
                category = get_category(file)
                category_path = os.path.join(target_dir, category)
                os.makedirs(category_path, exist_ok=True)

                new_path = os.path.join(category_path, file)

                try:
                    shutil.move(file_path, new_path)
                    logging.info(f"Moved: {file} → {category}/")
                    print(f"[OK] {file} → {category}/")
                except Exception as e:
                    logging.error(f"Error moving {file}: {e}")
                    print(f"[ERROR] Could not move {file}")

        print("\n✅ File organization completed successfully!")
        logging.info("File organization completed successfully.")

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"[FATAL] {e}")


# -----------------------------
# Main Execution
# -----------------------------

if __name__ == "__main__":
    print("=== File Organizer ===")
    source = input("Enter source directory path: ").strip()
    target = input("Enter target directory path: ").strip()

    organize_files(source, target)

