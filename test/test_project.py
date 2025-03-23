import os
import sys
import unittest
from unittest.mock import MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.project import Fuzzy_Filter, Project


class TestFuzzyFilter(unittest.TestCase):
    def setUp(self):
        self.app = MagicMock()
        self.app.name = "TestApp"
        self.projects = [
            Project(self.app, "/path/to/project1"),
            Project(self.app, "/path/to/project2"),
            Project(self.app, "/path/to/测试项目"),
        ]

    def test_query_filter_empty_query(self):
        result = Fuzzy_Filter.query_filter("", self.projects)
        self.assertEqual(result, self.projects)

    def test_query_filter_exact_match(self):
        result = Fuzzy_Filter.query_filter("project1", self.projects)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "project1")

    def test_query_filter_partial_match(self):
        result = Fuzzy_Filter.query_filter("project", self.projects)
        self.assertEqual(len(result), 2)
        self.assertIn(self.projects[0], result)
        self.assertIn(self.projects[1], result)

    def test_query_filter_pinyin_match(self):
        result = Fuzzy_Filter.query_filter("测试", self.projects)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "测试项目")

    def test_query_filter_no_match(self):
        result = Fuzzy_Filter.query_filter("nonexistent", self.projects)
        self.assertEqual(len(result), 0)


if __name__ == "__main__":
    unittest.main()
