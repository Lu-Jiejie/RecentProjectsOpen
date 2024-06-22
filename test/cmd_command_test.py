import subprocess

DEFAULT_VSCODE_PATH = r"D:\VSCode\bin\code"


def cmd_command(command: list):
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)


def software_startup(software_path, file_path_list):
    for file_path in file_path_list:
        cmd_command(f'"{software_path}" "{file_path}"')


if __name__ == '__main__':
    # cmd_command(DEFAULT_VSCODE_PATH + " "
    #             "D:\Project\BlogProject\hugoBlog")
    software_startup(DEFAULT_VSCODE_PATH, [
                     "D:\Project\BlogProject\hugoBlog", "D:\Project\BlogProject"])
