import os
import json
import xml.etree.ElementTree as ET
from typing import List
from ..core.logger import get_logger
from ..core.project import Project
from ..core.registry import ApplicationRegistry
from .base_application import BaseApplication

logger = get_logger()


@ApplicationRegistry.register("VISUAL_STUDIO")
class VisualStudio(BaseApplication):
    def __init__(self, download_path: str, storage_file: str):
        super().__init__(download_path, storage_file)
        self.name = "VISUAL_STUDIO"
        self.acronyms = "vs"

    def get_projects(self) -> List[Project]:
        """获取Visual Studio最近打开项目路径"""
        storage_file = self.storage_file
        if storage_file is None or not os.path.exists(storage_file):
            raise FileNotFoundError("storage_file not found")
        try:
            tree = ET.parse(storage_file)
            root = tree.getroot()
            collection = next(
                (
                    col
                    for col in root.findall(".//collection")
                    if col.attrib.get("name") == "CodeContainers.Offline"
                ),
                None,
            )
            if collection is None:
                return []
            value_node = next(
                (
                    val
                    for val in collection.findall("value")
                    if val.attrib.get("name") == "value"
                ),
                None,
            )
            value_text = None
            if value_node is not None:
                value_text = value_node.text or (
                    value_node.find("data").text
                    if (value_node.find("data") is not None)
                    else None
                )
            if not value_text:
                return []
            projects_data = json.loads(value_text)
        except Exception:
            # logger.error(f"解析 Visual Studio 项目 JSON 失败: {e}")
            return []
        projects = []
        for proj in projects_data:
            path = proj.get("Value", {}).get("LocalProperties", {}).get("FullPath", "")
            if not path:
                continue
            path = path.replace("\\", "/")
            project = Project(self.name, path)
            projects.append(project)
        return projects
