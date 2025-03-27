import json
import os
import re
from typing import List

from ..core.project import Project
from ..core.registry import ApplicationRegistry
from .vscode import Vscode


@ApplicationRegistry.register("VSCODE_SSH")
class VscodeSSH(Vscode):
    def __init__(self, download_path: str, storage_file: str):
        super().__init__(download_path, storage_file)
        self.name = "VSCODE_SSH"
        self.acronyms = "vscs"
        self.remote = True

    def get_projects(self) -> List[Project]:
        """
        # 示例：添加 SSH 远程连接
        projects.append(
            Project(
                app_name=self.name,
                path="ssh-remote+10.160.24.112-xwj /home/xwj/zywj",  # 显示用的路径
                command_args=[
                    "--remote",
                    "ssh-remote+10.160.24.112-xwj",
                    "/home/xwj/zywj",
                ],
            )
        )
        """
        storage_file = self.storage_file
        if storage_file is None:
            storage_file = os.path.join(
                os.getenv("APPDATA"), "Code", "User", "globalStorage", "storage.json"
            )
            if not os.path.exists(storage_file):
                raise FileNotFoundError("storage_file not found")
        storage_urls = []
        # 读取文件storage.json
        with open(storage_file, "r", encoding="utf8") as f:
            data = json.loads(f.read())
            profileAssociations = data.get("profileAssociations")
            workspaces = profileAssociations.get("workspaces")
            keys_list = list(workspaces.keys())
            for i in range(len(keys_list) - 1, -1, -1):  # 倒序
                if keys_list[i].startswith("vscode-remote"):
                    storage_urls.append(keys_list[i])
        # 实现本地项目列表获取逻辑
        projects = []
        pattern = r'(?:ssh-remote|wsl)\%2B([\w]+[^/]+)(/[^"]+)'
        for storage_url in storage_urls:
            # "vscode-remote://ssh-remote%2B10.160.24.112-root/home/zjh/LogisticsDesign": "__default__profile__",
            # & 'D:\Microsoft VS Code\Code.exe' "--remote ssh-remote+10.160.24.112-xwj /home/xwj/zywj"
            # 使用正则表达式提取 ssh-remote 部分
            # ssh-remote用户名部分可以是任意字符，但通常不包含斜杠
            match = re.search(pattern, storage_url)
            if match:
                ssh_remote = match.group(1)
                folder_url = match.group(2)
                vscode_remote = "ssh-remote+" if "ssh-remote" in storage_url else "wsl+"
            else:
                ssh_remote = ""
                folder_url = storage_url
            project = Project(
                app_name=self.name,
                path=ssh_remote + folder_url,
                command_args=[
                    "--remote",
                    vscode_remote + ssh_remote,
                    folder_url,
                ],
            )
            projects.append(project)

        return projects
