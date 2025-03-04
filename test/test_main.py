import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from plugin.main import RecentProjectsOpen


class TestRecentProjectsOpen(unittest.TestCase):
    def test_cursor(self):
        sys.argv = [
            r"D:\Project\MyProject\PythonProject\RecentProjectsOpen\plugin\main.py",
            r'{"method": "query", "parameters": ["cur "], "settings": {"CURSOR_DOWNLOAD": "C:/Users/xuwenjie/AppData/Local/Programs/cursor/Cursor.exe", "CURSOR_STORAGE": "C:/Users/xuwenjie/AppData/Roaming/Cursor/User/globalStorage/storage.json"}}',
        ]
        res = RecentProjectsOpen()

    def test_vscode(self):
        sys.argv = [
            r"D:\Project\MyProject\PythonProject\RecentProjectsOpen\plugin\main.py",
            r'{"method": "query", "parameters": ["vsc "], "settings": {"VISUAL_STUDIO_CODE_DOWNLOAD": "D:/Microsoft VS Code/Code.exe", "VISUAL_STUDIO_CODE_STORAGE": "C:/Users/xuwenjie/AppData/Roaming/Code/User/globalStorage/storage.json"}}',
        ]
        res = RecentProjectsOpen()

    @unittest.skip("")
    def test_jetbrains(self):
        sys.argv = [
            r"D:\Project\MyProject\PythonProject\RecentProjectsOpen\plugin\main.py",
            r'{"method": "query", "parameters": ["in "], "settings": {"INTELLIJ_IDEA_DOWNLOAD": "D:/IntelliJ IDEA 2024.3/bin/idea64.exe", "INTELLIJ_IDEA_STORAGE": "C:\\Users\\xuwenjie\\AppData\\Roaming\\JetBrains\\IntelliJIdea2024.3\\options\\recentProjects.xml"}}',
        ]
        res = RecentProjectsOpen()


if __name__ == "__main__":
    unittest.main()
    # 模拟传递给脚本的参数
    # command:
    # & D:\PythonPackage\Python311\python.exe d:\Project\MyProject\PythonProject\RecentProjectsOpen\plugin\main.py '{\"method\": \"query\", \"parameters\": [\"vsc \"], \"settings\": {\"VISUAL_STUDIO_CODE_DOWNLOAD\": \"D:/VSCode/bin/code\", \"VISUAL_STUDIO_CODE_STORAGE\": \"C:/Users/xuwenjie/AppData/Roaming/Code/User/globalStorage/storage.json\"}}'
    # json:
    # vsc_dict = {
    #     "method": "query",
    #     "parameters": ["vsc "],
    #     "settings": {
    #         "VISUAL_STUDIO_CODE_DOWNLOAD": "D:/VSCode/bin/code",
    #         "VISUAL_STUDIO_CODE_STORAGE": "C:/Users/xuwenjie/AppData/Roaming/Code/User/globalStorage/storage.json",
    #     },
    # }
    # import json

    # print(json.dumps(vsc_dict))
    # {"method": "query", "parameters": ["vsc "], "settings": {"VISUAL_STUDIO_CODE_DOWNLOAD": "D:/VSCode/bin/code", "VISUAL_STUDIO_CODE_STORAGE": "C:/Users/xuwenjie/AppData/Roaming/Code/User/globalStorage/storage.json"}}
