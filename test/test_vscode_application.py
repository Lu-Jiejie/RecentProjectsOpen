import os
import sys
import unittest

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(TEST_DIR)
sys.path.append(PROJECT_ROOT)

from src.application.vscode import Vscode  # noqa: E402
from src.core.project import Project  # noqa: E402


class TestVscodeApplication(unittest.TestCase):
    def setUp(self):
        """测试初始化"""
        self.mock_data_dir = os.path.join(TEST_DIR, "mock_data")
        self.valid_config_path = os.path.join(
            self.mock_data_dir, "test_vscode_storage.json"
        )
        self.invalid_config_path = os.path.join(self.mock_data_dir, "nonexistent.json")

        # 初始化VSCode应用
        self.vscode_app = Vscode(
            download_path="",
            storage_file=self.valid_config_path,
        )

    def test_vscode_init(self):
        """测试VSCode初始化属性"""
        self.assertEqual(self.vscode_app.name, "VSCODE")
        self.assertEqual(self.vscode_app.storage_file, self.valid_config_path)

    def test_get_vscode_projects_with_valid_file(self):
        """测试从有效配置文件中获取VSCode项目列表"""
        projects = self.vscode_app.get_projects()
        self.assertEqual(len(projects), 3)

        expected_data = [
            ("D:/Project/PythonProject/ai-tagging", "ai-tagging"),
            ("D:/Project/C#Project/Flow.Launcher", "Flow.Launcher"),
            ("D:/Project/PythonProject/microsearch", "microsearch"),
        ]

        for project, (expected_path, expected_name) in zip(projects, expected_data):
            self.assertIsInstance(project, Project)
            self.assertEqual(project.path, expected_path)
            self.assertEqual(project.name, expected_name)
            self.assertEqual(project.app_name, self.vscode_app.name)

    def test_get_vscode_projects_with_invalid_file(self):
        """测试使用不存在的配置文件时的VSCode错误处理"""
        invalid_app = Vscode("", self.invalid_config_path)
        with self.assertRaises(FileNotFoundError):
            invalid_app.get_projects()


if __name__ == "__main__":
    unittest.main()
