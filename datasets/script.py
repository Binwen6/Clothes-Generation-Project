import os
import shutil
from pathlib import Path

def find_lowest_directories(root_path):
    """
    This function recursively finds all lowest-level directories in the given root path.
    """
    lowest_dirs = []
    for dirpath, dirnames, filenames in os.walk(root_path):
        # If a directory has no subdirectories, it is considered a lowest-level directory
        if not dirnames:
            lowest_dirs.append(dirpath)
    return lowest_dirs

def rename_and_move_images(lowest_dirs, start_index=405, target_dir="D:/Code/datasets/necklaces/model"):
    """
    Rename and move images from the lowest directories to a target directory, starting from a given index.
    """
    Path(target_dir).mkdir(parents=True, exist_ok=True)  # Create target directory if it doesn't exist
    current_index = start_index
    
    for directory in lowest_dirs:
        for filename in os.listdir(directory):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                old_path = os.path.join(directory, filename)
                new_filename = f"necklace_model{current_index}.jpg"
                new_path = os.path.join(target_dir, new_filename)
                shutil.copy(old_path, new_path)
                print(f"Copied {old_path} to {new_path}")
                current_index += 1

if __name__ == "__main__":
    root_directory = "D:/Users/lenovo/Downloads/图片助手(ImageAssistant)_批量图片下载器"  # Change this if the path is incorrect
    lowest_dirs = find_lowest_directories(root_directory)
    rename_and_move_images(lowest_dirs)
