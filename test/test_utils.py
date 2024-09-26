import os
import sys
import unittest
from os.path import abspath, dirname, join

parent_folder_path = abspath(dirname(dirname(__file__)))
sys.path.append(parent_folder_path)
sys.path.append(join(parent_folder_path, "plugin"))


from plugin.utils import (  # noqa: E402
    Application,
    Project,
    convert_first_letter_upper,
    fuzzy_match,
)


class TestProject(unittest.TestCase):
    @unittest.skip("跳过")
    def test_project_init(self):
        # 测试路径以斜杠结尾
        project_path = "/path/to/project/"
        project = Project(project_path)
        self.assertEqual(project.name, "project")
        self.assertEqual(project.path, project_path)

    def test_project_init_without_trailing_slash(self):
        # 测试路径不以斜杠结尾
        project_path = "/path/to/project"
        project = Project(project_path)
        self.assertEqual(project.name, "project")
        self.assertEqual(project.path, project_path)

    def test_project_init_with_filename(self):
        # 测试路径包含文件名
        project_path = "/path/to/project/filename.ext"
        project = Project(project_path)
        self.assertEqual(project.name, "filename.ext")
        self.assertEqual(project.path, project_path)

    def test_project_init_with_whitespace(self):
        # 测试路径包含空格
        project_path = "/path/to/project with space"
        project = Project(project_path)
        self.assertEqual(project.name, "project with space")
        self.assertEqual(project.path, project_path)


class TestFuzzyMatch(unittest.TestCase):
    def test_empty_query(self):
        """测试空查询字符串"""
        query = ""
        items = ["item1", "item2", "item3"]
        expected = items
        result = fuzzy_match(query, items)
        self.assertEqual(result, expected)

    def test_fuzzy_match(self):
        """测试模糊匹配"""
        query = "item"
        items = ["item1", "item2", "item3", "itasde", "item"]
        expected = [
            "item1",
            "item2",
            "item3",
            "item",
        ]  # 假设 'item3' 有一个好的模糊匹配得分
        result = fuzzy_match(query, items)
        self.assertEqual(result, expected)

    def test_pinyin_match(self):
        """测试拼音匹配"""
        query = "空洞武士"
        items = ["空洞武士", "kongdongwushi"]
        expected = ["空洞武士", "kongdongwushi"]
        result = fuzzy_match(query, items)
        self.assertEqual(result, expected)

    def test_no_match(self):
        """测试没有匹配的情况"""
        query = "nonexistent"
        items = ["item1", "item2", "item3"]
        expected = []
        result = fuzzy_match(query, items)
        self.assertEqual(result, expected)


class TestGetJetbrainsProjects(unittest.TestCase):
    def setUp(self):
        # 获取当前项目的绝对路径
        current_dir = dirname(abspath(__file__))
        self.app = Application(
            name="test_ide",
            installation_path="test",
            recent_projects_file=os.path.join(
                current_dir, "test_jetbrains_recent_project.xml"
            ),
        )

    def test_get_jetbrains_projects_success(self):
        # 设置mock App.get_recent_projects返回XML文件
        projects = self.app.get_jetbrains_projects()

        self.assertEqual(
            projects,
            [
                "D:/javaproject/java_classroom",
                "D:/Project/JavaProject/RuoYi",
                "D:/Project/JavaProject/RuoYi/ruoyi-admin",
            ],
        )

    def test_get_jetbrains_projects_none(self):
        self.app.recent_projects_file = None
        with self.assertRaises(Exception):
            self.app.get_jetbrains_projects()


class TestGetVscodeProjects(unittest.TestCase):
    def setUp(self):
        # 获取当前项目的绝对路径
        current_dir = dirname(abspath(__file__))
        self.app = Application(
            name="test_vscode",
            installation_path="test",
            recent_projects_file=os.path.join(current_dir, "test_vscode_storage.json"),
        )

    def test_get_vscode_projects_success(self):
        projects = self.app.get_vscode_projects()
        self.assertEqual(
            projects,
            [
                "D:/Project/PythonProject/ai-tagging",
                "D:/Project/C#Project/Flow.Launcher",
                "D:/Project/PythonProject/microsearch",
            ],
        )

    def test_get_vscode_projects_none(self):
        self.app.recent_projects_file = None
        recent_projects_file = os.path.join(
            os.getenv("APPDATA"), "Code", "User", "globalStorage", "storage.json"
        )
        if not os.path.exists(recent_projects_file):
            with self.assertRaises(Exception):
                self.app.get_vscode_projects()
        else:
            projects = self.app.get_vscode_projects()
            self.assertIsNotNone(projects)


class TestConvertFirstLetterUpper(unittest.TestCase):
    def test_empty_list(self):
        """测试空列表"""
        self.assertEqual(convert_first_letter_upper([]), [])

    def test_single_project(self):
        """测试单个项目"""
        projects = ["test_project"]
        expected = ["Test_project"]
        self.assertEqual(convert_first_letter_upper(projects), expected)

    def test_multiple_projects(self):
        """测试多个项目"""
        projects = ["test_project1", "test_project2"]
        expected = ["Test_project1", "Test_project2"]
        self.assertEqual(convert_first_letter_upper(projects), expected)

    def test_non_string_project(self):
        """测试包含非字符串的项目"""
        projects = ["test_project", 123]
        with self.assertRaises(ValueError):
            convert_first_letter_upper(projects)

    def test_empty_string_project(self):
        """测试包含空字符串的项目"""
        projects = ["test_project", ""]
        with self.assertRaises(ValueError):
            convert_first_letter_upper(projects)

    def test_mixed_case_projects(self):
        """测试混合大小写的项目"""
        projects = ["Test_project", "testProject"]
        expected = ["Test_project", "TestProject"]
        self.assertEqual(convert_first_letter_upper(projects), expected)


if __name__ == "__main__":
    unittest.main()
