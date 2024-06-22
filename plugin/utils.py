
import os
import json
import urllib.parse


def get_vscode_project() -> list:
    """获取vscode最近打开的项目路径

    Returns:
        list: vscode最近打开的项目路径
        example: ['D:/VSCode/workspaces/project1', 'D:/VSCode/workspaces/project2']
    """
    file = os.path.join(os.getenv("APPDATA"), "Code",
                        "User", "globalStorage", "storage.json")
    folder_urls = []
    with open(file, 'r') as f:
        data = json.loads(f.read())
        profileAssociations = data.get("profileAssociations")
        workspaces = profileAssociations.get("workspaces")
        keys_list = list(workspaces.keys())
        for i in range(-1, -11, -1):  # 倒过来选取后10个
            folder_urls.append(keys_list[i])
    project_path = []
    for folder_url in folder_urls:
        folder_url = folder_url.replace("file:///", "")
        folder_url.replace("%3A", ":").replace("/", "\\")
        folder_url = urllib.parse.unquote(folder_url)
        project_path.append(folder_url)
    return project_path


def get_all_workspaces() -> list:
    file = os.path.join(os.getenv("APPDATA"), "Code",
                        "User", "globalStorage", "storage.json")
    folder_urls = []
    with open(file, 'r') as f:
        data = json.loads(f.read())
        profileAssociations = data.get("profileAssociations")
        workspaces = profileAssociations.get("workspaces")
        keys_list = list(workspaces.keys())
        for i in range(-1, -len(keys_list)-1, -1):
            folder_urls.append(keys_list[i])
    project_path = []
    for folder_url in folder_urls:
        folder_url = folder_url.replace("file:///", "")
        folder_url.replace("%3A", ":").replace("/", "\\")
        folder_url = urllib.parse.unquote(folder_url)
        project_path.append(folder_url)
    return project_path
