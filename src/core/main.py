import subprocess
import sys
import webbrowser
from os.path import abspath, dirname

from click import UsageError
from flowlauncher import FlowLauncher

# 添加根目录到sys.path
sys.path.append(dirname(dirname(dirname(abspath(__file__)))))
from src.core.config import cfg
from src.core.factory import ConcreteFactory
from src.core.filter import Fuzzy_Filter
from src.core.jsonrpc import JsonRPCClient
from src.core.logger import get_logger
from src.core.message import MessageDTO

logger = get_logger()


class RecentProjectsOpen(FlowLauncher):
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
        # 读取配置文件，如果配置文件中有对应的app_download和app_storage
        settings = JsonRPCClient().recieve().get("settings", {})
        logger.debug(f"settings: {settings}")
        if settings.get(app_name + "_DOWNLOAD", None):
            cfg.rewrite({app_name + "_DOWNLOAD": settings.get(app_name + "_DOWNLOAD")})
        if settings.get(app_name + "_STORAGE", None):
            cfg.rewrite({app_name + "_STORAGE": settings.get(app_name + "_STORAGE")})
        # 读取.env配置文件
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

    def cmd_command(self, app_download, project_path):
        """
        由于json_rpc只会传输字符串，所以需要将字符串转换为list
        ["D:/IntelliJ IDEA 2024.3/bin/idea64.exe", "D:/Project/CloneProject/JavaProject/LeetcodeHot"]
        """
        command = [app_download, project_path]
        logger.debug(f"command: {command}")
        _ = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )


if __name__ == "__main__":
    test = RecentProjectsOpen()

    # liunx
    # python your_script.py '{"method": "query", "parameters": ["test"]}'
    # win
    # 需要为'"'添加\
    # & D:\PythonPackage\Python311\python.exe D:\Project\MyProject\PythonProject\RecentProjectsOpen\src\core\main.py '{\"method\": \"query\", \"parameters\": [\"vsc \"], \"settings\": {\"VISUAL_STUDIO_CODE_DOWNLOAD\": \"D:/VSCode/bin/code\", \"VISUAL_STUDIO_CODE_STORAGE\": \"C:/Users/xuwenjie/AppData/Roaming/Code/User/globalStorage/storage.json\"}}'
