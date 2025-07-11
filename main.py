import os
import sys

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, "lib"))
sys.path.append(os.path.join(parent_folder_path, "src"))

from src.core.main import RecentProjectsOpen  # noqa: E402

if __name__ == "__main__":
    RecentProjectsOpen()
