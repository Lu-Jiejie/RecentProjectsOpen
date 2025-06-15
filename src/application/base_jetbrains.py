import os
import xml.etree.ElementTree as ElementTree
from typing import List

from ..core.logger import get_logger
from ..core.project import Project
from .base_application import BaseApplication

logger = get_logger()


class Jetbrains(BaseApplication):
    def __init__(self, download_path: str, storage_file: str):
        super().__init__(download_path, storage_file)

    def get_projects(self) -> List[Project]:
        """获取JetBrains项目列表"""
        storage_file = self.storage_file
        if not os.path.exists(storage_file):
            raise FileNotFoundError("storage_file not found")
        tree = ElementTree.parse(storage_file)
        projects = []
        for t in tree.findall(
            ".//component[@name='RecentProjectsManager']/option[@name='additionalInfo']/map/entry"
        ):
            folder_url = t.attrib["key"].replace("$USER_HOME$", "~")
            project = Project(self.name, folder_url)
            projects.append(project)
        return projects
