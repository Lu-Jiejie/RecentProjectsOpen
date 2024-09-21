import urllib.parse

from log_config import setup_logging
from utils import Project

setup_logging()


class MessageDTO:
    """消息传输对象"""

    def __init__(
        self,
        title="title",
        subtitle="subtitle",
        icopath="images/app.png",
        method="open_url",
        parameter_list=[""],
    ) -> None:
        self.title = title
        self.subtitle = subtitle
        self.icopath = icopath
        self.method = method
        self.parameter_list = parameter_list

    def asFlowMessage(self) -> list:
        return [
            {
                "Title": urllib.parse.unquote(self.title),
                "SubTitle": self.subtitle,
                "IcoPath": self.icopath,
                "jsonRPCAction": {
                    "method": self.method,
                    "parameter_list": self.parameter_list,
                },
            }
        ]

    @staticmethod
    def asMultiFlowMessage(
        project_list: list[Project], icopath, method: str, app_download: str
    ):
        message_list = []
        title_list = [project.name for project in project_list]
        subtitle_list = [project.path for project in project_list]
        parameter_list = []
        for project in project_list:
            parameter = app_download.join(" ").join(project.path)
            parameter_list.append(parameter)

        for i in range(len(title_list)):
            message_list.append(
                {
                    "Title": title_list[i],  # unquote指示中文转码
                    "SubTitle": subtitle_list[i],
                    "IcoPath": icopath,
                    "jsonRPCAction": {
                        "method": method,
                        "parameter_list": parameter_list[i],
                    },
                }
            )
        return message_list


if __name__ == "__main__":
    res = MessageDTO("title", "subtitle", "Images/app.png", "method", "parameter_list")
    app = "e"
    keyword = "a"
    print(MessageDTO(title=app, subtitle=keyword).asFlowMessage())
