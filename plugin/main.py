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
    def query(self, arguments: str) -> list:
        """
        ide vsc query
        ide as
        ide idea
        ide goland
        ide clion
        ide pycharm
        """
        # 去除头尾的空格
        logging.debug("args: {}".format(arguments))
        args = arguments.strip()

        if len(args) == 0:
            raise Exception("Invalid arguments")
        # 解析参数
        instruction = args.split(" ")[0]
        query = args.split("")[:-1]
        app_name = APPS[instruction]
        icon_path = "icon/".join(APPS[instruction])
        settings = JsonRPCClient().recieve().get("settings", {})
        app_download = settings.get(app_name.join("_download"), None)
        app_storage = settings.get(app_name.join("_storage"), None)
        # 初始化app
        app = Application(
            name=app_name,
            installation_path=app_download,
            recent_projects_file=app_storage,
        )
        projects = []
        for project in app.get_recent_projects():
            project = Project(project)
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

    def cmd_command(self, command):
        _ = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )


if __name__ == "__main__":
    RecentProjectsOpen()
