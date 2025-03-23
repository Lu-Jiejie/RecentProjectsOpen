from .vscode import Vscode


class Cursor(Vscode):
    def __init__(self,  download_path: str, storage_file: str):
        super().__init__( download_path, storage_file)
        self.name = "CURSOR"
        self.acronyms = "cur"
