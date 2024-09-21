from typing import TypedDict

Settings = TypedDict(
    "Settings",
    {
        "vscode_download": str,
        "vscode_storage": str,
        "androidstudio_download": str,
        "androidstudio_storage": str,
        "clion_download": str,
        "clion_storage": str,
        "pycharm_download": str,
        "pycharm_storage": str,
        "goland_download": str,
        "goland_storage": str,
        "idea_download": str,
        "idea_storage": str,
    },
)
