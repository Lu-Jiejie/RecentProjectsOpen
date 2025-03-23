from typing import List

from ..core.logger import get_logger
from ..core.project import Project
from .base_application import BaseApplication

logger = get_logger()


class SumatraPDF(BaseApplication):
    def __init__(self, download_path: str, storage_file: str):
        super().__init__(download_path, storage_file)
        self.name = "SUMATRA_PDF"
        self.acronyms = "pdf"

    def get_projects(self) -> List[Project]:
        """获取SumatraPDF最近打开项目路径"""
        projects = []

        return projects
