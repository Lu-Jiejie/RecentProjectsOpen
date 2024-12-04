import os
import subprocess
import sys
import webbrowser

from click import UsageError
from flowlauncher import FlowLauncher

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from plugin.application.factory import ConcreteFactory
from plugin.config import cfg, get_logger
from plugin.jsonrpc import JsonRPCClient
from plugin.message import MessageDTO
from plugin.project import Fuzzy_Filter

logger = get_logger()

ABBREVIATE = {
    "vsc": "VISUAL_STUDIO_CODE",
    "py": "PYCHARM",
    "cl": "CLION",
    "go": "GOLAND",
    "in": "INTELLIJ_IDEA",
    "as": "ANDROID_STUDIO",
}


class RecentProjectsOpen(FlowLauncher):
    def query(self, param: str) -> list:
        """ """
        # 读取参数，解析abbreviation和query
        args = param.strip()
        if len(args) == 0:
            return MessageDTO.asWarnFlowMessage(
                "param is empty", "Please input your query"
            )
        abbreviate = args.split(" ")[0]
        if abbreviate not in ABBREVIATE.keys():
            return MessageDTO.asWarnFlowMessage(
                "{} is not supported".format(abbreviate),
                "Please input your Software abbreviation",
            )
        else:
            app_name = ABBREVIATE[abbreviate]
            logger.debug(f"app_name: {app_name}")
        icon_path = "icons/{}_icon.png".format(abbreviate)
        query = "".join(args.split(" ")[1:])
        # 读取配置文件，如果配置文件中有对应的app_download和app_storage，使用配置文件中的，否则使用默认值
        settings = JsonRPCClient().recieve().get("settings", {})
        logger.debug(f"settings: {settings}")
        if settings.get(app_name + "_DOWNLOAD", None):
            cfg.rewrite({app_name + "_DOWNLOAD": settings.get(app_name + "_DOWNLOAD")})
        if settings.get(app_name + "_STORAGE", None):
            cfg.rewrite({app_name + "_STORAGE": settings.get(app_name + "_STORAGE")})
        try:
            app_download = cfg.get(app_name + "_DOWNLOAD")
            app_storage = cfg.get(app_name + "_STORAGE")
        except UsageError:
            return MessageDTO.asWarnFlowMessage(
                "app_download or app_storage is None", "Please check your settings"
            )
        # 读取recent_projects
        try:
            app = ConcreteFactory.create_app(app_name, app_download, app_storage)
            projects = app.get_projects()
            res = Fuzzy_Filter.query_filter(query, projects)
        except NotImplementedError:
            return MessageDTO.asWarnFlowMessage(
                "this app is not supported", "Welcome to provide PR"
            )
        except FileNotFoundError:
            return MessageDTO.asWarnFlowMessage(
                "app_download or app_storage is Error", "Please check your settings"
            )
        return MessageDTO().asMultiFlowMessage(
            res,
            icon_path,
            "cmd_command",
            app_download,
        )

    def open_url(self, url):
        webbrowser.open(url)

    def context_menu(self, data):
        """
        TODO：
        使用软件打开
        使用任务管理器打开文件夹
        复制文件夹路径
        """
        pass

    def cmd_command(self, command: str):
        _ = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )


if __name__ == "__main__":
    test = RecentProjectsOpen()

    # liunx
    # python your_script.py '{"method": "query", "parameters": ["test"]}'
    # win
    # 需要为'"'添加\
    # & D:\PythonPackage\Python311\python.exe d:\Project\MyProject\PythonProject\RecentProjectsOpen\plugin\main.py '{\"method\": \"query\", \"parameters\": [\"vsc \"], \"settings\": {\"VISUAL_STUDIO_CODE_DOWNLOAD\": \"D:/VSCode/bin/code\", \"VISUAL_STUDIO_CODE_STORAGE\": \"C:/Users/xuwenjie/AppData/Roaming/Code/User/globalStorage/storage.json\"}}'
