import re

if __name__ == "__main__":
    storage_file = r"C:\Users\xuwenjie\AppData\Local\SumatraPDF\SumatraPDF-settings.txt"

    def get_projects():
        """获取SumatraPDF最近打开项目路径"""
        projects = []

        try:
            with open(storage_file, "r", encoding="utf-8") as file:
                settings_content = file.read()
        except FileNotFoundError:
            print(f"Settings file not found: {storage_file}")
            return projects

        # 使用正则表达式匹配 FilePath
        file_path_pattern = re.compile(r"\s*FilePath\s*=\s*(.+)")
        matches = file_path_pattern.findall(settings_content)

        for match in matches:
            file_path = match.strip()
            if file_path:
                projects.append(file_path)

        return projects

    projects = get_projects()
    for project in projects:
        print(project)
