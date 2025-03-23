import urllib.parse
from typing import List

from .logger import get_logger
from .project import Project

logger = get_logger()


class MessageDTO:
    """消息传输对象"""

    def __init__(
        self,
        title: str = "title",
        subtitle: str = "subtitle",
        icopath: str = "images/app.png",
        method: str = "open_url",
        parameters: list[str] = [""],
    ) -> None:
        self.title = title
        self.subtitle = subtitle
        self.icopath = icopath
        self.method = method
        self.parameters = parameters

    def asFlowMessage(self) -> list:
        return [
            {
                "Title": urllib.parse.unquote(self.title),
                "SubTitle": self.subtitle,
                "IcoPath": self.icopath,
                "jsonRPCAction": {
                    "method": self.method,
                    "parameters": self.parameters,
                },
            }
        ]

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
                    "jsonRPCAction": {
                        "method": method,
                        "parameters": parameters[i],
                    },
                }
            )
        return message_list

    @staticmethod
    def asWarnFlowMessage(msg, operation) -> List:
        return [
            {
                "Title": msg,
                "SubTitle": operation,
                "IcoPath": "icons/app.png",
            }
        ]

    @staticmethod
    def asDebugFlowMessage(msg) -> List:
        return [
            {
                "Title": msg,
                "SubTitle": "Debug",
                "IcoPath": "icons/warn.png",
            }
        ]
