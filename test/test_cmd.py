import subprocess
from typing import List


def cmd_command(command: List[str]):
    _ = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )


if __name__ == "__main__":
    # cmd_command(
    #     [
    #         "C:/Users/xuwenjie/AppData/Local/Programs/cursor/Cursor.exe",
    #         "D:/Project/CloneProject/PythonProject/langchain",
    #     ],
    # )
    # cmd_command(["echo", "c", "|", "clip"])
    # cmd_command(["start", "D:/Project/MyProject/AndroidStudioProject/HelloWorld"])
    # cmd_command(
    #     [
    #         "D:/Microsoft VS Code/Code.exe",
    #         "--remote",
    #         "ssh-remote+10.160.24.112-xwj",
    #         "/home/xwj/zywj",
    #     ]
    # )
    cmd_command(
        ["D:/Microsoft VS Code/Code.exe", "--remote", "wsl+ubuntu", "/home/xwj/project"]
    )
