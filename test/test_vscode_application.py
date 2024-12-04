import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from plugin.application.vscode_application import Vscode


class TestVscode(unittest.TestCase):
    def test_get_projects(self):
        vscode = Vscode(
            name="",
            download_path="",
            storage_file=r"D:\Project\MyProject\PythonProject\RecentProjectsOpen\test\mock_data\test_vscode_storage.json",
        )

        projects = vscode.get_projects()
        for project in projects:
            print(project.path)
        self.assertEqual(len(projects), 3)
        self.assertEqual(projects[0].path, r"D:/Project/PythonProject/ai-tagging")
        self.assertEqual(projects[1].path, r"D:/Project/C#Project/Flow.Launcher")
        self.assertEqual(projects[2].path, r"D:/Project/PythonProject/microsearch")
        self.assertEqual(projects[0].name, "ai-tagging")
        self.assertEqual(projects[1].name, "Flow.Launcher")
        self.assertEqual(projects[2].name, "microsearch")


if __name__ == "__main__":
    unittest.main()
