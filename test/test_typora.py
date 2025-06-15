import json
from datetime import datetime
from typing import List

if __name__ == "__main__":
    storage_file = r"C:/Users/xuwenjie/AppData/Roaming/Typora/history.data"

    def get_projects() -> List:
        """获取Typora最近打开的项目"""
        projects = []

        try:
            with open(storage_file, "r", encoding="utf-8") as file:
                settings_content = file.read()
        except FileNotFoundError:
            print(f"Settings file not found: {storage_file}")
            return projects

        # decoding the hex string to bytes
        buffer = bytes.fromhex(settings_content)
        settings_content = json.loads(buffer.decode("utf-8"))

        # combine recentFolder and recentDocument
        all_items = []

        if "recentFolder" in settings_content:
            for folder in settings_content["recentFolder"]:
                if "path" in folder and "date" in folder:
                    # convert ISO 8601 date string to timestamp
                    timestamp = datetime.fromisoformat(
                        folder["date"].replace("Z", "+00:00")
                    ).timestamp()
                    all_items.append({"path": folder["path"], "timestamp": timestamp})

        if "recentDocument" in settings_content:
            for document in settings_content["recentDocument"]:
                if "path" in document and "date" in document:
                    timestamp = document["date"] / 1000
                    all_items.append({"path": document["path"], "timestamp": timestamp})

        # sort all items by timestamp in descending order
        all_items.sort(key=lambda x: x["timestamp"], reverse=True)

        for item in all_items:
            projects.append(item["path"])

        return projects

    projects = get_projects()
    for project in projects:
        print(project)
