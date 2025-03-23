import os

from .logger import get_logger

logger = get_logger()


class Project:
    def __init__(self, app_name: str, project_path: str):
        self.app = app_name
        self.name = os.path.basename(project_path)
        self.path = project_path


if __name__ == "__main__":
    pass
