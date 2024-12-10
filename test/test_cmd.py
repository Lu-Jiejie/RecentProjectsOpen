import subprocess
from typing import List


def cmd_command(command: List[str]):
    _ = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )


if __name__ == "__main__":
    cmd_command(
        [
            "D:/IntelliJ IDEA 2024.3/bin/idea64.exe",
            "D:/Project/CloneProject/JavaProject/LeetcodeHot",
        ],
    )
