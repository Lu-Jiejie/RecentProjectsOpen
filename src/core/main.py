import subprocess
import sys
import webbrowser
from os.path import abspath, dirname

from click import UsageError
from flowlauncher import FlowLauncher

# 添加根目录到sys.path
sys.path.append(dirname(dirname(dirname(abspath(__file__)))))
from src.core.config import config
from src.core.factory import ConcreteFactory
from src.core.filter import Fuzzy_Filter
from src.core.logger import get_logger
from src.core.message import MessageDTO

logger = get_logger()


class RecentProjectsOpen(FlowLauncher):
    def __init__(self):
        super().__init__()
        self.context = {}

    def query(self, param: str) -> list:
        # 读取参数，解析acronyms和query
        args = param.strip()
        if len(args) == 0:
            return MessageDTO.asWarnFlowMessage(
                "param is empty", "Please input your query"
            )
        acronyms = args.split(" ")[0]
        acronyms_dict = ConcreteFactory.get_application_acronyms()
        if acronyms not in acronyms_dict.keys():
            return MessageDTO.asWarnFlowMessage(
                "{} is not supported".format(acronyms),
                "Please input your software acronyms",
            )
        else:
            app_name = acronyms_dict[acronyms]
            logger.debug(f"app_name: {app_name}")
        icon_path = "icons/{}_icon.png".format(acronyms)
        query = "".join(args.split(" ")[1:])

        # 读取配置
        try:
            app_download = config.get(app_name + "_DOWNLOAD")
            app_storage = config.get(app_name + "_STORAGE")
        except UsageError as e:
            return MessageDTO.asWarnFlowMessage(
                "{0} app_download or app_storage is None".format(app_name) + str(e),
                "Please check your settings",
            )
        logger.debug(f"app_download: {app_download}, app_storage: {app_storage}")
        # 读取recent_projects
        try:
            app = ConcreteFactory.create_app(app_name, app_download, app_storage)
            projects = app.get_projects()
            res = Fuzzy_Filter.query_filter(query, projects)  # 项目查询结果
        except NotImplementedError:
            return MessageDTO.asWarnFlowMessage(
                "this app is not supported", "Welcome to provide PR"
            )
        except FileNotFoundError:
            return MessageDTO.asWarnFlowMessage(
                "app_download or app_storage is Error", "Please check your settings"
            )
        return MessageDTO().asMultiFlowMessage(
            projects=res,
            icopath=icon_path,
            method="cmd_command",
            app_download=app_download,
        )

    def context_menu(self, data: str) -> list:
        """
        使用任务管理器打开文件夹
        复制文件夹路径
        """
        if data is None:
            return MessageDTO.asDebugFlowMessage("data is None")
        import re

        # 正则表达式
        pattern = r"^[A-Za-z]:/[\w\-/]+$"

        if len(data) > 1 and re.match(pattern, data[1]):
            return [
                {
                    "title": "Open in explorer",
                    "subTitle": "Press enter to open the explorer",
                    "icoPath": "icons/app.png",  # related path to the image
                    "jsonRPCAction": {
                        "method": "cmd_command",
                        "parameters": ["start", data[1]],
                    },
                    "score": 0,
                },
                {
                    "title": "Copy path",
                    "subTitle": "Press enter to copy the path",
                    "icoPath": "icons/app.png",  # related path to the image
                    "jsonRPCAction": {
                        "method": "copy_to_clipboard",
                        "parameters": [data[1]],
                    },
                    "score": 0,
                },
                {
                    "title": "RecentProjectsOpen's Context menu",
                    "subTitle": "Press enter to open Flow the plugin's repo in GitHub",
                    "icoPath": "icons/app.png",
                    "jsonRPCAction": {
                        "method": "open_url",
                        "parameters": [
                            "https://github.com/Attack825/RecentProjectsOpen"
                        ],
                    },
                },
            ]
        else:
            return MessageDTO.asWarnFlowMessage(
                {
                    "title": "RecentProjectsOpen's Context menu",
                    "subTitle": "Press enter to open Flow the plugin's repo in GitHub",
                    "icoPath": "icons/app.png",
                    "jsonRPCAction": {
                        "method": "open_url",
                        "parameters": [
                            "https://github.com/Attack825/RecentProjectsOpen"
                        ],
                    },
                },
            )

    def open_url(self, url):
        webbrowser.open(url)

    def cmd_command(self, *args):
        """
        由于json_rpc只会传输字符串，所以需要将字符串转换为list
        ["D:/IntelliJ IDEA 2024.3/bin/idea64.exe", "D:/Project/CloneProject/JavaProject/LeetcodeHot"]
        """
        _ = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )

    def copy_to_clipboard(self, text: str):
        _ = subprocess.Popen(
            ["echo", text, "|", "clip"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )


if __name__ == "__main__":
    RecentProjectsOpen()

    # query
    # & D:\PythonPackage\Python311\python.exe D:\Project\MyProject\PythonProject\RecentProjectsOpen\src\core\main.py '{\"method\": \"query\", \"parameters\": [\"vsc \"], \"settings\": {\"VISUAL_STUDIO_CODE_DOWNLOAD\": \"D:/VSCode/bin/code\", \"VISUAL_STUDIO_CODE_STORAGE\": \"C:/Users/xuwenjie/AppData/Roaming/Code/User/globalStorage/storage.json\"}}'
    # & D:\PythonPackage\Python311\python.exe D:\Project\MyProject\PythonProject\RecentProjectsOpen\src\core\main.py '{\"method\": \"query\", \"parameters\": [\"vsc \"]}'

    # context_menu
    # & D:\PythonPackage\Python311\python.exe D:\Project\MyProject\PythonProject\RecentProjectsOpen\src\core\main.py '{\"method\": \"context_menu\", \"parameters\": [{\"title\": \"D:/Project/CloneProject/JavaProject/LeetcodeHot\"}]}'
