from abc import ABC, abstractmethod

from .jetbrains_application import (
    AndroidStudio,
    Clion,
    Goland,
    IntelliJIdea,
    Pycharm,
)
from .vscode_application import (
    Vscode,
)


class AbstractFactory(ABC):
    @classmethod
    @abstractmethod
    def create_app(cls, name: str, download_path: str, storage_file: str):
        pass


class ConcreteFactory(AbstractFactory):
    def register(self, name, product):
        pass

    @classmethod
    def create_app(cls, name: str, download_path: str, storage_file: str):
        try:
            if name == "PYCHARM":
                return Pycharm(name, download_path, storage_file)
            elif name == "INTELLIJ_IDEA":
                return IntelliJIdea(name, download_path, storage_file)
            elif name == "ANDROID_STUDIO":
                return AndroidStudio(name, download_path, storage_file)
            elif name == "GOLAND":
                return Goland(name, download_path, storage_file)
            elif name == "CLION":
                return Clion(name, download_path, storage_file)
            elif name == "VISUAL_STUDIO_CODE":
                return Vscode(name, download_path, storage_file)
            else:
                raise NotImplementedError("Invalid product")
        except FileNotFoundError as e:
            raise e


if __name__ == "__main__":
    pass
