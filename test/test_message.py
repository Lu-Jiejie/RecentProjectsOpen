# test_message.py
import sys
import unittest
from os.path import abspath, dirname, join
from unittest.mock import Mock

parent_folder_path = abspath(dirname(dirname(__file__)))
sys.path.append(parent_folder_path)
sys.path.append(join(parent_folder_path, "plugin"))
sys.path.append(join(parent_folder_path, "test"))

from plugin.message import MessageDTO  # noqa: E402


class TestMessageDTO(unittest.TestCase):
    def test_asMultiFlowMessage(self):
        # 准备测试数据
        projects = [
            Mock(spec=["name", "path"]),
            Mock(spec=["name", "path"]),
        ]
        # 正确设置 name 和 path 属性
        projects[0].name = "Project1"
        projects[0].path = "C:\\path\\to\\project1"
        projects[1].name = "Project2"
        projects[1].path = "C:\\path\\to\\project2"

        icopath = "C:\\path\\to\\icon.png"
        method = "openProject"
        app_download = "code"

        # 调用待测函数
        messages = MessageDTO.asMultiFlowMessage(
            projects, icopath, method, app_download
        )

        # 构建期望得到的结果
        expected_message_list = [
            {
                "Title": "Project1",
                "SubTitle": "C:\\path\\to\\project1",
                "IcoPath": icopath,
                "jsonRPCAction": {
                    "method": method,
                    "parameters": "code C:\\path\\to\\project1",
                },
            },
            {
                "Title": "Project2",
                "SubTitle": "C:\\path\\to\\project2",
                "IcoPath": icopath,
                "jsonRPCAction": {
                    "method": method,
                    "parameters": "code C:\\path\\to\\project2",
                },
            },
        ]
        self.assertEqual(projects[0].name, expected_message_list[0].get("Title"))
        self.assertEqual(projects[0].path, expected_message_list[0].get("SubTitle"))
        # 断言测试结果与期望结果是否一致
        self.assertEqual(messages, expected_message_list)


if __name__ == "__main__":
    unittest.main()
