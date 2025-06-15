import json
from datetime import datetime
from typing import List

from ..core.logger import get_logger
from ..core.project import Project
from ..core.registry import ApplicationRegistry
from .base_application import BaseApplication

logger = get_logger()


@ApplicationRegistry.register("TYPORA")
class Typora(BaseApplication):
    def __init__(self, download_path: str, storage_file: str):
        super().__init__(download_path, storage_file)
        self.name = "TYPORA"
        self.acronyms = "ty"

    def get_projects(self) -> List[Project]:
        """获取Typora最近打开的项目"""
        projects = []

        try:
            with open(self.storage_file, "r", encoding="utf-8") as file:
                settings_content = file.read()
        except FileNotFoundError:
            print(f"Settings file not found: {self.storage_file}")
            return projects

        # decoding the hex string to bytes
        buffer = bytes.fromhex(settings_content)
        settings_content = json.loads(buffer.decode("utf-8"))

        # combine recentFolder and recentDocument
        all_items = []

        if "recentFolder" in settings_content:
            for folder in settings_content["recentFolder"]:
                if "path" in folder and "date" in folder:
                    # convert ISO 8601 date string to timestamp
                    timestamp = datetime.fromisoformat(
                        folder["date"].replace("Z", "+00:00")
                    ).timestamp()
                    all_items.append({"path": folder["path"], "timestamp": timestamp})

        if "recentDocument" in settings_content:
            for document in settings_content["recentDocument"]:
                if "path" in document and "date" in document:
                    timestamp = document["date"] / 1000
                    all_items.append({"path": document["path"], "timestamp": timestamp})

        # sort all items by timestamp in descending order
        all_items.sort(key=lambda x: x["timestamp"], reverse=True)

        for item in all_items:
            projects.append(Project(self.name, item["path"]))

        return projects
