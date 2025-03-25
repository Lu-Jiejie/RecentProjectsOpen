from typing import List

from .logger import get_logger
from .project import Project

logger = get_logger()


class MessageDTO:
    """消息传输对象"""

    @staticmethod
    def asMultiFlowMessage(
        projects: list[Project], icopath, method: str, app_download: str
    ) -> List:
        message_list = []

        titles = [project.name for project in projects]
        subtitles = [project.path for project in projects]
        parameters = []
        for project in projects:
            parameter = [app_download, project.path]
            parameters.append(parameter)

        for i in range(len(titles)):
            message_list.append(
                {
                    "Title": titles[i],  # unquote指示中文转码
                    "SubTitle": subtitles[i],
                    "IcoPath": icopath,
                    "ContextData": parameters[i],  # 传递参数给context menu
                    "jsonRPCAction": {
                        "method": method,
                        "parameters": parameters[i],
                    },
                }
            )
        return message_list

    @staticmethod
    def asWarnFlowMessage(title, subTitle) -> List:
        return [
            {
                "Title": title,
                "SubTitle": subTitle,
                "IcoPath": "icons/warn.png",
            }
        ]

    @staticmethod
    def asDebugFlowMessage(msg) -> List:
        return [
            {
                "Title": msg,
                "SubTitle": "Debug",
                "IcoPath": "icons/app.png",
            }
        ]
