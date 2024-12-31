# Flow.Launcher.Plugin.RecentProjectsOpen

A plugin that allows users to quickly open recent projects with ease.

## Installation

Download from the store

## Configuration

To get the most out of the `RecentProjectsOpen` plugin, you may need to configure it according to your preferences and environment.

1. **Open Flow Launcher Settings**: Launch Flow Launcher and navigate to the settings page where plugins are managed.
2. **Find the Plugin**: Locate the `RecentProjectsOpen` plugin in the list of installed plugins.
3. **Access Configuration Options**: Click on the plugin to access its configuration options. There should be a settings icon or a similar indicator that allows you to open the configuration page.

Now, to input the software download paths and storage file addresses, you would use the following format as an example:

```plaintext
VISUAL_STUDIO_CODE_DOWNLOAD=D:/VSCode/bin/code

VISUAL_STUDIO_CODE_STORAGE=C:/Users/YourUsername/AppData/Roaming/Code/User/globalStorage/storage.json

ANDROID_STUDIO_DOWNLOAD=D:/Android Studio/bin/studio64.exe

ANDROID_STUDIO_STORAGE=C:/Users/YourUsername/AppData/Roaming/Google/AndroidStudio2024.1/options/recentProjects.xml

INTELLIJ_IDEA_DOWNLOAD=D:/IntelliJ IDEA 2024.3/bin/idea64.exe

INTELLIJ_IDEA_STORAGE=C:/Users/YourUsername/AppData/Roaming/JetBrains/IntelliJIdea2024.3/options/recentProjects.xml

GOLAND_DOWNLOAD=D:/goland/GoLand 2023.2/bin/goland64.exe

GOLAND_STORAGE=C:/Users/YourUsername/AppData/Roaming/JetBrains/GoLand2023.2/options/recentProjects.xml

CLION_DOWNLOAD=D:/Clion/CLion 2024.1.4/bin/clion64.exe

CLION_STORAGE=C:/Users/YourUsername/AppData/Roaming/JetBrains/CLion2024.1/options/recentProjects.xml
```

Replace `YourUsername` with your actual Windows username to point to the correct directories. These paths are essential for the plugin to function correctly by opening the appropriate IDEs and accessing their recent projects.

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
