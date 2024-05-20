import webbrowser
from flowlauncher import FlowLauncher
import sys
import os
import json
import random
import subprocess
import urllib.parse
from typing import Any, Mapping, Dict

if sys.version_info < (3, 11):
    from typing_extensions import NotRequired, TypedDict
else:
    from typing import NotRequired, TypedDict

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))
DEFAULT_VSCODE_PATH = r"D:\VSCode\bin\code"


class JsonRPCRequest(TypedDict):
    method: str
    parameters: list
    settings: NotRequired[dict[Any, Any]]


class JsonRPCClient:

    def send(self, data: Mapping) -> None:
        json.dump(data, sys.stdout)

    def recieve(self):
        try:
            return json.loads(sys.argv[1])
        except (IndexError, json.JSONDecodeError):
            return {'method': 'query', 'parameters': ['']}


def settings() -> Dict[str, Any]:
    """Retrieve the settings from Flow Launcher."""
    return JsonRPCClient().recieve().get('settings', {})


def debug_str(str):
    return [
        {
            "Title": "Hello World Python's Context menu",
            "SubTitle": str,
            "IcoPath": "Images/app.png",
            "JsonRPCAction": {
                "method": "open_url",
                "parameters": ["https://github.com/Flow-Launcher/Flow.Launcher.Plugin.HelloWorldPython"]
            }
        }
    ]


class MessageDTO:
    def __init__(self, project_list: dict, vscode_path) -> None:
        self.title = project_list["name"]
        self.subtitle = "Press Enter to open the project."
        self.image = project_list["icon"]
        # todo:无法获得flow launcher客户端的配置设置，只能被调用
        if not vscode_path is None:
            self.cmd = vscode_path + " " + project_list["path"]
        else:
            self.cmd = DEFAULT_VSCODE_PATH + " " + project_list["path"]

    def asFlowMessage(self) -> dict:
        return {
            "Title": urllib.parse.unquote(self.title),
            "SubTitle": self.subtitle,
            "IcoPath": self.image,
            "jsonRPCAction": {
                "method": "cmd_command",
                "parameters": [self.cmd]
            }
        }


def check_path(path):
    if os.path.exists(path):
        return True, os.path.getatime(path), os.path.getmtime(path)
    else:
        return False, 0, 0


def get_vscode_project() -> list:
    file = os.path.join(os.getenv("APPDATA"), "Code",
                        "User", "globalStorage", "storage.json")
    exist, atime, mtime = check_path(file)
    # todo: 缓存，避免关机丢失工作区
    if not exist:
        return []
    with open(file, 'r') as f:
        data = json.loads(f.read())
        folder_urls = [folder["folderUri"]
                       for folder in data["backupWorkspaces"]["folders"]]
    projectList = []
    for folder_url in folder_urls:
        projectList.append({
            'key': random.randint(0, 1000000),
            'ide': 'Visual Studio Code',
            'icon': 'images/app.png',
            'name': os.path.basename(folder_url),
            'path': get_project_url(folder_url),
            'atime': atime,
            'mtime': mtime
        })

    return projectList


def get_project_url(folder_url):
    folder_url = folder_url.replace("file:///", "")
    return folder_url.replace("%3A", ":").replace("/", "\\")


def debug(str):
    return [{
        "Title": "title",
        "SubTitle": str,
        "IcoPath": "image/app.png",
        # "jsonRPCAction": {
        #     "method": "cmd_command",
        #     "parameters": [self.cmd]
        # }
    }]


class HelloWorld(FlowLauncher):

    messages = []

    def addMessage(self, message: MessageDTO):
        self.messages.append(message.asFlowMessage())

    def query(self,  params: str) -> list:
        """
        当flow launcher 触发关键词时，flow会向插件发送query，同时附带了一些信息，需要接受这些信息获取配置信息
        """
        settings = JsonRPCClient().recieve().get("settings", {})
        vscode_path = settings.get("vscode_path", None) or None
        project_list = get_vscode_project()
        # todo: 搜索项目
        project_list.sort(key=lambda x: x["mtime"], reverse=True)
        for project in project_list:
            self.addMessage(MessageDTO(project, vscode_path))
        return self.messages

    def open_url(self, url):
        webbrowser.open(url)

    def cmd_command(self, command):
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)


if __name__ == "__main__":
    HelloWorld()
