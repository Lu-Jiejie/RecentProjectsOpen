import os
import sys
import unittest

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(TEST_DIR)
sys.path.append(PROJECT_ROOT)

from src.application.sumatra import SumatraPDF  # noqa: E402
from src.core.project import Project  # noqa: E402


class TestSumatraApplication(unittest.TestCase):
    def setUp(self):
        """测试初始化"""
        self.mock_data_dir = os.path.join(TEST_DIR, "mock_data")
        self.valid_config_path = os.path.join(
            self.mock_data_dir, "SumatraPDF-settings.txt"
        )
        self.invalid_config_path = os.path.join(self.mock_data_dir, "nonexistent.txt")

        self.sumatra_app = SumatraPDF(
            download_path="",
            storage_file=self.valid_config_path,
        )

    def test_init(self):
        """测试初始化属性"""
        self.assertEqual(self.sumatra_app.name, "SUMATRA")
        self.assertEqual(self.sumatra_app.acronyms, "pdf")
        self.assertEqual(self.sumatra_app.storage_file, self.valid_config_path)

    def test_get_projects_with_valid_file(self):
        """测试从有效配置文件中获取项目列表"""
        projects = self.sumatra_app.get_projects()
        self.assertEqual(len(projects), 3)

        expected_paths = [
            "D:/Project/Document/test1.pdf",
            "D:/Project/Document/test2.pdf",
            "D:/Project/Document/test3.pdf",
        ]

        for project, expected_path in zip(projects, expected_paths):
            self.assertIsInstance(project, Project)
            self.assertEqual(project.path, expected_path)
            self.assertEqual(project.app_name, self.sumatra_app.name)

    def test_get_projects_with_invalid_file(self):
        """测试使用不存在的配置文件时的错误处理"""
        invalid_app = SumatraPDF("", self.invalid_config_path)
        projects = invalid_app.get_projects()
        self.assertEqual(len(projects), 0)


if __name__ == "__main__":
    unittest.main()
