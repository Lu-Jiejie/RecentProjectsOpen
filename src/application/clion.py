from src.application.base_jetbrains import Jetbrains

from ..core.registry import ApplicationRegistry


@ApplicationRegistry.register("CLION")
class Clion(Jetbrains):
    def __init__(self, download_path: str, storage_file: str):
        super().__init__(download_path, storage_file)
        self.name = "CLION"
        self.acronyms = "cl"
