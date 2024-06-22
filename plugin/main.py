import webbrowser
from flowlauncher import FlowLauncher
import sys
import os
import subprocess
from .jsonrpc import JsonRPCClient
from .message import MessageDTO
from .utils import *


parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))
DEFAULT_VSCODE_PATH = "D:/VSCode/bin/code"
ICOPATH = "images/app.png"


class VscodeOpen(FlowLauncher):
    def query(self,  params: str) -> list:
        """
        当flow launcher 触发关键词时，flow会向插件发送query
        """
        settings = JsonRPCClient().recieve().get("settings", {})
        vscode_path = settings.get("vscode_path", None) or DEFAULT_VSCODE_PATH
        vscode_path = DEFAULT_VSCODE_PATH
        project_path_list = get_vscode_project()
        project_name_list = []
        parameters_list = []
        for project_path in project_path_list:
            project_name = project_path.split("/")[-1]
            project_name_list.append(project_name)
            parameters_list.append([vscode_path + " " + project_path])

        return MessageDTO().asMultiFlowMessage(project_name_list, project_path_list, ICOPATH, "cmd_command", parameters_list)

    def open_url(self, url):
        webbrowser.open(url)

    def cmd_command(self, command):
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    def software_startup(self, software_path, file_path_list):
        for file_path in file_path_list:
            self.cmd_command(f'"{software_path}" "{file_path}"')


if __name__ == "__main__":
    VscodeOpen()
