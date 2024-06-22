import urllib.parse


class MessageDTO:
    """消息传输对象
    用于封装flowlauncher的消息对象
    example: MessageDTO("title", "subtitle", "images/app.png",
                        "method", "parameters").asFlowMessage()
    """

    def __init__(self, title="title", subtitle="subtitle", icopath="images/app.png", method="open_url", parameters=[""]) -> None:
        self.title = title
        self.subtitle = subtitle
        self.icopath = icopath
        self.method = method
        self.parameters = parameters

    def asFlowMessage(self) -> list:
        return [{
            "Title": urllib.parse.unquote(self.title),
            "SubTitle": self.subtitle,
            "IcoPath": self.icopath,
            "jsonRPCAction": {
                "method": self.method,  # 自定义插件的方法
                "parameters": self.parameters  # 自定义插件类的参数
            }
        }]

    def asMultiFlowMessage(self, title_list, subtitle_list, icopath, method, parameters_list) -> list:
        """生成多个消息对象
        """
        message_list = []
        for i in range(len(title_list)):
            message_list.append({
                "Title": urllib.parse.unquote(title_list[i]),
                "SubTitle": subtitle_list[i],
                "IcoPath": icopath,
                "jsonRPCAction": {
                    "method": method,
                    "parameters": parameters_list[i]
                }
            })
        return message_list


if __name__ == '__main__':
    res = MessageDTO("title", "subtitle", "Images/app.png",
                     "method", "parameters")
    # print(res.asFlowMessage())
    app = "e"
    keyword = "a"
    print(MessageDTO(title=app, subtitle=keyword).asFlowMessage())
