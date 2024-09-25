import sys  # 导入sys模块
import unittest
from os.path import abspath, dirname, join
from unittest.mock import MagicMock, patch

parent_folder_path = abspath(dirname(dirname(__file__)))
sys.path.append(parent_folder_path)
sys.path.append(join(parent_folder_path, "plugin"))
sys.path.append(join(parent_folder_path, "test"))


from plugin.main import RecentProjectsOpen  # noqa: E402


class TestRecentProjectsOpen(unittest.TestCase):
    def setUp(self):
        self.rpo = RecentProjectsOpen()

    @patch("main.JsonRPCClient")  # patch是模拟一个类，用于替换一个模块中的类
    @patch("main.Application")
    @patch("main.Project")
    @patch("main.MessageDTO")
    def test_query(
        self, mock_MessageDTO, mock_Project, mock_Application, mock_JsonRPCClient
    ):
        # 设置mock对象的返回值
        mock_jsonrpc_client_instance = MagicMock()
        mock_jsonrpc_client_instance.recieve.return_value = {
            "settings": {
                "vscode_download": "/path/to/vscode",
                "vscode_storage": "/path/to/vscode/storage",
            }
        }
        mock_JsonRPCClient.return_value = mock_jsonrpc_client_instance

        mock_application_instance = MagicMock()
        mock_application_instance.get_recent_projects.return_value = [
            "/path/to/project1",
            "/path/to/project2",
        ]
        mock_application_instance.fuzzy_match.return_value = ["/path/to/project1"]
        mock_Application.return_value = mock_application_instance

        mock_project_instance = MagicMock()
        mock_Project.return_value = mock_project_instance

        mock_message_dto_instance = MagicMock()
        mock_MessageDTO.return_value = mock_message_dto_instance

        # 测试用例
        arguments = "vsc project_name "
        result = self.rpo.query(arguments)

        # 验证mock对象的调用情况
        mock_JsonRPCClient.assert_called_once()
        mock_Application.assert_called_once_with(
            name="vscode",
            installation_path="/path/to/vscode",
            recent_projects_file="/path/to/vscode/storage",
        )
        mock_Project.assert_called()
        mock_MessageDTO.assert_called_once()

        # 验证返回结果
        self.assertEqual(
            result, mock_message_dto_instance.asMultiFlowMessage.return_value
        )


if __name__ == "__main__":
    unittest.main()
