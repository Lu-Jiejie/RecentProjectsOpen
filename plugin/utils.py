import json
import logging
import os
import urllib.parse
import xml.etree.ElementTree as ElementTree

from fuzzywuzzy import process
from log_config import setup_logging
from pypinyin import Style, lazy_pinyin

setup_logging()


class Project:
    def __init__(self, project: str):
        self.name = os.path.basename(project)
        self.path = project


class Application:
    def __init__(
        self,
        name: str,
        installation_path: str,
        recent_projects_file: str,
    ):
        self.name = name
        self.installation_path = installation_path
        self.recent_projects_file = recent_projects_file
        self.projects = None

    def get_vscode_projects(self) -> list:
        """获取vscode最近打开项目路径"""
        recent_projects_file = self.recent_projects_file
        if recent_projects_file is None:
            recent_projects_file = os.path.join(
                os.getenv("APPDATA"), "Code", "User", "globalStorage", "storage.json"
            )
            if not os.path.exists(recent_projects_file):
                raise FileNotFoundError("recent_projects_file not found")
        folder_urls = []
        # 读取文件storage.json
        with open(recent_projects_file, "r", encoding="utf8") as f:
            data = json.loads(f.read())
            profileAssociations = data.get("profileAssociations")
            workspaces = profileAssociations.get("workspaces")
            keys_list = list(workspaces.keys())
            for i in range(len(keys_list) - 1, -1, -1):  # 倒序
                folder_urls.append(keys_list[i])
        projects = []
        for folder_url in folder_urls:
            folder_url = folder_url.replace("file:///", "")
            folder_url.replace("%3A", ":").replace("/", "\\")
            folder_url = urllib.parse.unquote(folder_url)
            projects.append(folder_url)
        projects = convert_first_letter_upper(projects)

        return projects

    def get_jetbrains_projects(self) -> list:
        """获取JetBrains项目列表

        Args:
            recent_projects_file (_type_): _description_

        Returns:
            list: _description_
        """
        recent_projects_file = self.recent_projects_file
        if recent_projects_file is None:
            recent_projects_file = os.path.join(
                os.getenv("APPDATA"), "Code", "User", "globalStorage", "storage.json"
            )
            if not os.path.exists(recent_projects_file):
                raise FileNotFoundError("recent_projects_file not found")
        tree = ElementTree.parse(recent_projects_file)
        projects = [
            t.attrib["key"].replace("$USER_HOME$", "~")
            for t in tree.findall(
                ".//component[@name='RecentProjectsManager']/option[@name='additionalInfo']/map/entry"
            )
        ]
        # return reversed(projects)  # 返回一个可迭代对象
        return projects

    def get_recent_projects(self) -> list[str]:
        """依据名称获取最近打开的项目

        Args:
            name (_type_): _description_

        Returns:
            list[str]: _description_
        """
        if self.name == "Visual_Studio_Code":
            return self.get_vscode_projects()
        elif self.name in {
            "Android_Studio",
            "IntelliJ_IDEA",
            "PyCharm",
            "GoLand",
            "Clion",
        }:
            return self.get_jetbrains_projects()
        else:
            raise NotImplementedError("Not implemented")

    @staticmethod
    def fuzzy_match(query: str, projects: list[Project]) -> list[Project]:
        """模糊匹配项目

        Args:
            query (str): _description_
            projects (Project): _description_

        Returns:
            Project: _description_
        """
        match = fuzzy_match(query, [project.name for project in projects])
        res = []
        for project in projects:
            if project.name in match:
                res.append(project)
        return res


def fuzzy_match(query: str, items: list) -> list:
    """模糊匹配，返回匹配到的项目名称

    Args:
        query (str): _description_
        items (list): _description_

    Returns:
        _type_: _description_
    """
    if len(query) < 1:  # 空查询
        return items
    # 转换查询为拼音小写，拼音list转str
    query_pinyin = "".join(lazy_pinyin(query, style=Style.NORMAL)).lower()
    logging.debug(f"query_pinyin:{query_pinyin}")
    # 对每个项进行匹配
    matches = []
    for item in items:
        item_pinyin = "".join(lazy_pinyin(item, style=Style.NORMAL)).lower()
        if item_pinyin.startswith(query_pinyin):
            matches.append(item)
            logging.debug(f"matched:{item}")
        else:
            result = process.extractOne(query_pinyin, item_pinyin)
            logging.debug("result: ", item_pinyin)
            if result is not None and result[1] > 90:
                logging.debug(f"extractOne matched:{item}")
                matches.append(item)

    return matches


def convert_first_letter_upper(projects: list[str]) -> list[str]:
    """将项目列表的首字母转换为大写

    Args:
        projects (list[str]): _description_

    Raises:
        ValueError: _description_
        ValueError: _description_

    Returns:
        list[str]: _description_
    """
    # 处理空列表的情况
    if not projects:
        return []

    # 确保每个项目名称首字母大写
    capitalized_projects = []
    for project in projects:
        # 检查是否为字符串
        if not isinstance(project, str):
            raise ValueError("All projects must be strings")

        # 检查是否为空字符串
        if not project:
            raise ValueError("Project name cannot be an empty string")

        # 首字母大写
        capitalized_project = project[0].upper() + project[1:]
        capitalized_projects.append(capitalized_project)

    return capitalized_projects


if __name__ == "__main__":
    a = "who arE you?"
    print(convert_first_letter_upper([a]))
    pass
