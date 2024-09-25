import logging
import subprocess
import webbrowser

from flowlauncher import FlowLauncher
from jsonrpc import JsonRPCClient
from log_config import setup_logging
from message import MessageDTO
from utils import Application, Project

setup_logging()

ICOPATH = "icons/app.png"

APPS = {
    "vsc": "vscode",
    "as": "androidstudio",
    "idea": "idea",
    "goland": "goland",
    "clion": "clion",
    "pycharm": "pycharm",
}


class RecentProjectsOpen(FlowLauncher):
    def query(self, param: str) -> list:
        """
        ide vsc query
        ide as
        ide idea
        ide goland
        ide clion
        ide pycharm
        """
        args = param.strip()
        logging.debug(f"param: {args}")
        if len(args) == 0:
            raise Exception("Invalid param")
        # 解析参数
        instruction = args.split(" ")[0]
        if instruction not in APPS.keys():
            raise Exception("Invalid instruction")
        else:
            app_name = APPS[instruction]
        icon_path = "icon/{}.png".format(APPS[instruction])
        logging.debug(f"icon_path:{icon_path}")

        query = "".join(args.split(" ")[1:])
        logging.debug(f"query: {query}")

        settings = JsonRPCClient().recieve().get("settings", {})
        logging.debug(f"settings: {settings}")
        app_download = settings.get(app_name + "_download", None)
        app_storage = settings.get(app_name + "_storage", None)
        if app_download is None or app_storage is None:
            raise Exception("Invalid settings")

        # 初始化app
        app = Application(
            name=app_name,
            installation_path=app_download,
            recent_projects_file=app_storage,
        )
        projects = []
        for project in app.get_recent_projects():
            project = Project(project)
            logging.debug(f"projects: {project.name}")
            projects.append(project)

        res = app.fuzzy_match(query, projects)

        return MessageDTO().asMultiFlowMessage(
            res,
            icon_path,
            "cmd_command",
            app_download,
        )

    def open_url(self, url):
        webbrowser.open(url)

    def context_menu(self, data):
        """用于定义查询结果的上下文菜单。它接收一个参数 `data`，并返回一个列表作为上下文菜单的条目。

        Args:
            data (_type_): _description_
        """
        pass

    def cmd_command(self, command: str):
        _ = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )


def test():
    import json

    # 在文件夹中复制地址时，文件夹中的地址是用 \ 来分隔不同文件夹的，而Python识别地址时只能识别用 / 分隔的地址。
    # 替换反斜杠为 正斜杠
    vscode_download = r"D:\VSCode\bin\code".replace("\\", "/")

    vscode_storage = r"C:\Users\xuwenjie\AppData\Roaming\Code\User\globalStorage\storage.json".replace(
        "\\", "/"
    )

    txt = {
        "method": "query",
        "parameters": ["vsc project_name"],
        "settings": {
            "vscode_download": vscode_download,
            "vscode_storage": vscode_storage,
        },
    }
    print(json.dumps(txt))


if __name__ == "__main__":
    test = RecentProjectsOpen()

    # liunx
    # python your_script.py '{"method": "query", "parameters": ["test"]}'
    # win
    # 需要为'"'添加\
    # & D:\PythonPackage\Python311\python.exe d:\Project\PythonProject\Flow.Launcher.Plugin.RecentProjectsOpen\plugin\main.py '{\"method\": \"query\", \"parameters\": [\"vsc MyKnowledgeBase\"], \"settings\": {\"vscode_download\": \"D:/VSCode/bin/code\", \"vscode_storage\": \"C:/Users/xuwenjie/AppData/Roaming/Code/User/globalStorage/storage.json\"}}'
