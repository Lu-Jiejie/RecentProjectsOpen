from typing import TypedDict

Settings = TypedDict(
    "Settings",
    {
        "VSCODE_STUDIO_CODE_DOWNLOAD": str,
        "VISUAL_STUDIO_CODE_STORAGE": str,
        "ANDROID_STUDIO_DOWNLOAD": str,
        "ANDROID_STUDIO_STORAGE": str,
        "INTELLIJ_IDEA_DOWNLOAD": str,
        "INTELLIJ_IDEA_STORAGE": str,
        "GOLAND_DOWNLOAD": str,
        "GOLAND_STORAGE": str,
        "CLION_DOWNLOAD": str,
        "CLION_STORAGE": str,
        "PYCHARM_DOWNLOAD": str,
        "PYCHARM_STORAGE": str,
    },
)
