import os
from abc import ABC, abstractmethod
from typing import List

from fuzzywuzzy import process
from pypinyin import Style, lazy_pinyin

from .config import get_logger

logger = get_logger()


class Project:
    def __init__(self, app_name: str, project_path: str):
        self.app = app_name
        self.name = os.path.basename(project_path)
        self.path = project_path


class Filter(ABC):
    @classmethod
    @abstractmethod
    def query_filter(cls, query: str, items: List[Project]) -> List[Project]:
        pass


class Fuzzy_Filter(Filter):
    @classmethod
    def query_filter(cls, query: str, items: List[Project]) -> List[Project]:
        """模糊匹配字符串列表，返回匹配到的项目名称"""

        if len(query) < 1:
            return items
        query_pinyin = "".join(lazy_pinyin(query, style=Style.NORMAL)).lower()
        matches = []
        for item in items:
            project_name = item.name
            project_name_pinyin = "".join(
                lazy_pinyin(project_name, style=Style.NORMAL)
            ).lower()
            if project_name_pinyin.startswith(query_pinyin):
                matches.append(item)
            else:
                result = process.extractOne(query_pinyin, project_name_pinyin)
                if result is not None and result[1] > 90:
                    matches.append(item)

        return matches


if __name__ == "__main__":
    pass
