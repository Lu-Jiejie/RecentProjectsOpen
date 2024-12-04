import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from plugin.main import RecentProjectsOpen


class TestVscodeRecentProjectsOpen(unittest.TestCase):
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

    sys.argv = [
        r"D:\Project\MyProject\PythonProject\RecentProjectsOpen\plugin\main.py",
        r'{"method": "query", "parameters": ["vsc "], "settings": {"VISUAL_STUDIO_CODE_DOWNLOAD": "D:/VSCode/bin/code", "VISUAL_STUDIO_CODE_STORAGE": "C:/Users/xuwenjie/AppData/Roaming/Code/User/globalStorage/storage.json"}}',
    ]
    res = RecentProjectsOpen()


class TestIntellijIdea(unittest.TestCase):
    # 模拟传递给脚本的参数
    # command:
    # & D:\PythonPackage\Python311\python.exe d:\Project\MyProject\PythonProject\RecentProjectsOpen\plugin\main.py '{\"method\": \"query\", \"parameters\": [\"idea \"], \"settings\": {\"INTELLIJ_IDEA_DOWNLOAD\": \"D:/IntelliJ IDEA/bin/idea64.exe\", \"INTELLIJ_IDEA_STORAGE\": \"C:/Users/xuwenjie/AppData/Roaming/JetBrains/IntelliJIdea2021.1/options/recentProjectDirectories.xml\"}}'
    # json:
    idea_dict = {
        "method": "query",
        "parameters": ["id "],
        "settings": {
            "INTELLIJ_IDEA_DOWNLOAD": "D:/IntelliJ IDEA 2024.3/bin/idea64.exe",
            "INTELLIJ_IDEA_STORAGE": r"C:\Users\xuwenjie\AppData\Roaming\JetBrains\IntelliJIdea2024.3\options\recentProjects.xml",
        },
    }
    import json

    print(json.dumps(idea_dict))
    # {"method": "query", "parameters": ["id "], "settings": {"INTELLIJ_IDEA_DOWNLOAD": "D:/IntelliJ IDEA 2024.3/bin/idea64.exe", "INTELLIJ_IDEA_STORAGE": "C:\\Users\\xuwenjie\\AppData\\Roaming\\JetBrains\\IntelliJIdea2024.3\\options\\recentProjects.xml"}}
    sys.argv = [
        r"D:\Project\MyProject\PythonProject\RecentProjectsOpen\plugin\main.py",
        r'{"method": "query", "parameters": ["in "], "settings": {"INTELLIJ_IDEA_DOWNLOAD": "D:/IntelliJ IDEA 2024.3/bin/idea64.exe", "INTELLIJ_IDEA_STORAGE": "C:\\Users\\xuwenjie\\AppData\\Roaming\\JetBrains\\IntelliJIdea2024.3\\options\\recentProjects.xml"}}',
    ]
    res = RecentProjectsOpen()


if __name__ == "__main__":
    # unittest.main()
    pass
