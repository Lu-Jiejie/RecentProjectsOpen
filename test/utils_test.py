
import os
import json
import urllib.parse
import sys  # 导入sys模块
sys.path.append("./")
DEFAULT_VSCODE_PATH = r"D:\VSCode\bin\code"


def get_vscode_project() -> list:
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


if __name__ == "__main__":
    from plugin.utils import get_all_workspaces
    # print(get_vscode_project())
    # print(get_all_workspaces())
    vscode_path = DEFAULT_VSCODE_PATH
    project_path_list = get_vscode_project()
    parameters_list = []
    for project_path in project_path_list:
        parameters_list.append([vscode_path, project_path])

    print(parameters_list)
