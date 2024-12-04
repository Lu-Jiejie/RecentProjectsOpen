from abc import abstractmethod
from typing import List

from ..config import get_logger
from ..project import Project

logger = get_logger()
ICON_SUFFIX = "_icon.png"


class BaseApplication:
    def __init__(
        self,
        name: str,
        download_path: str,
        storage_file: str,
    ):
        self.name = name
        self.icon_path = name + ICON_SUFFIX
        self.download_path = download_path
        self.storage_file = storage_file
        self.projects = None

    @abstractmethod
    def get_projects(self) -> List[Project]:
        pass


if __name__ == "__main__":
    pass
