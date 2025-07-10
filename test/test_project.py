import os
import sys
import unittest

# 设置项目根目录到sys.path
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(TEST_DIR)
sys.path.append(PROJECT_ROOT)

from src.core.filter import Fuzzy_Filter  # noqa: E402
from src.core.project import Project  # noqa: E402


class TestProject(unittest.TestCase):
    def setUp(self):
        """测试初始化"""
        self.app_name = "vscode"
        self.project_path = "/path/to/project1"
        self.project = Project(self.app_name, self.project_path)

    def test_project_initialization(self):
        """测试Project类的初始化"""
        self.assertEqual(self.project.app_name, self.app_name)
        self.assertEqual(self.project.path, self.project_path)
        self.assertEqual(self.project.name, "project1")
        self.assertIsNone(self.project.command_args)

    def test_project_with_command_args(self):
        """测试带有command_args的Project初始化"""
        command_args = ["--remote", "ssh-remote+host", "/path/to/remote"]
        project = Project(self.app_name, self.project_path, command_args)

        self.assertEqual(project.command_args, command_args)
        self.assertEqual(project.app_name, self.app_name)
        self.assertEqual(project.path, self.project_path)

    def test_get_command_without_args(self):
        """测试不带command_args的get_command方法"""
        app_download = "code"
        expected_command = [app_download, self.project_path]
        self.assertEqual(self.project.get_command(app_download), expected_command)

    def test_get_command_with_args(self):
        """测试带command_args的get_command方法"""
        command_args = ["--remote", "ssh-remote+host", "/path/to/remote"]
        project = Project(self.app_name, self.project_path, command_args)

        app_download = "code"
        expected_command = [app_download] + command_args
        self.assertEqual(project.get_command(app_download), expected_command)


class TestFuzzyFilter(unittest.TestCase):
    def setUp(self):
        """测试初始化"""
        self.projects = [
            Project("vscode", "/path/to/project1"),
            Project("vscode", "/path/to/project2"),
            Project("vscode", "/path/to/测试项目"),
        ]

    def test_query_filter_empty_query(self):
        """测试空查询字符串"""
        result = Fuzzy_Filter.query_filter("", self.projects)
        self.assertEqual(result, self.projects)

    def test_query_filter_exact_match(self):
        """测试精确匹配"""
        result = Fuzzy_Filter.query_filter("project1", self.projects)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "project1")

    def test_query_filter_partial_match(self):
        """测试部分匹配"""
        result = Fuzzy_Filter.query_filter("project", self.projects)
        self.assertEqual(len(result), 2)
        self.assertIn(self.projects[0], result)
        self.assertIn(self.projects[1], result)

    def test_query_filter_chinese_match(self):
        """测试中文匹配"""
        result = Fuzzy_Filter.query_filter("测试", self.projects)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "测试项目")

    def test_query_filter_pinyin_match(self):
        """测试拼音匹配"""
        result = Fuzzy_Filter.query_filter("ceshi", self.projects)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "测试项目")

    def test_query_filter_no_match(self):
        """测试无匹配结果"""
        result = Fuzzy_Filter.query_filter("nonexistent", self.projects)
        self.assertEqual(len(result), 0)


if __name__ == "__main__":
    unittest.main()
