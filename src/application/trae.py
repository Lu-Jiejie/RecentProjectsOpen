from ..core.registry import ApplicationRegistry
from .vscode import Vscode


@ApplicationRegistry.register("TRAE")
class Trae(Vscode):
    def __init__(self, download_path: str, storage_file: str):
        super().__init__(download_path, storage_file)
        self.name = "TRAE"
        self.acronyms = "trae"
