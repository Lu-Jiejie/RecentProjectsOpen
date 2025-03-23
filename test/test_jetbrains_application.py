import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.application.base_jetbrains import (
    Jetbrains,
)


class TestJetbrainsApplication(unittest.TestCase):
    def test_get_projects(self):
        jetbrains_app = Jetbrains(
            "",
            "",
            r"D:\Project\MyProject\PythonProject\RecentProjectsOpen\test\mock_data\test_jetbrains_recent_project.xml",
        )

        projects = jetbrains_app.get_projects()
        for project in projects:
            print(project.path)
        self.assertEqual(len(projects), 3)
        self.assertEqual(projects[0].path, r"D:/javaproject/java_classroom")
        self.assertEqual(projects[1].path, r"D:/Project/JavaProject/RuoYi")
        self.assertEqual(projects[2].path, r"D:/Project/JavaProject/RuoYi/ruoyi-admin")


if __name__ == "__main__":
    unittest.main()
