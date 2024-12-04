# Flow.Launcher.Plugin.RecentProjectsOpen

A plugin that allows users to quickly open recent projects with ease.

## Installation

Download from the store

## Usage

You can access different IDEs using the following format:

```python
ABBREVIATE = {
    "vsc": "VISUAL_STUDIO_CODE",
    "py": "PYCHARM",
    "cl": "CLION",
    "go": "GOLAND",
    "in": "INTELLIJ_IDEA",
    "as": "ANDROID_STUDIO",
}
```

To open a project named "MyProject" in Visual Studio Code, you would use:

r vsc

![1733284352742](image/README/1733284352742.png)


r vsc My

![1733284374591](image/README/1733284374591.png)


r vsc 空

![1733284760505](image/README/1733284760505.png)

## TODO

IDE

* [X] Vscode
* [X] Jetbrains
* [X] Android Studio
* [ ] Visual Studio
* [ ] Aseprite

feature

* [X] fuzzy search
* [X] support pinyin
* [X] prevent configurations from disappearing after updates
