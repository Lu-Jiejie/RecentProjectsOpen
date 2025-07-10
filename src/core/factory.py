from abc import ABC, abstractmethod
from typing import Dict, List

from .registry import ApplicationRegistry


class AbstractFactory(ABC):
    @classmethod
    @abstractmethod
    def create_app(cls, name: str, download_path: str, storage_file: str):
        pass


class ConcreteFactory(AbstractFactory):
    @classmethod
    def create_app(cls, name: str, download_path: str, storage_file: str):
        """通过注册表创建应用实例"""
        ApplicationRegistry.load_applications()
        try:
            application_class = ApplicationRegistry.get_application(name)
            if application_class is None:
                raise NotImplementedError(f"Application {name} not registered")
            return application_class(download_path, storage_file)
        except FileNotFoundError as e:
            raise e

    @classmethod
    def get_supported_applications(cls):
        """
        获取所有支持的应用列表
        """
        return list(ApplicationRegistry.get_all_applications().keys())

    @classmethod
    def get_application_acronyms(cls) -> Dict[str, str]:
        """
        获取应用的缩写字典
        返回格式:
        {
            "vsc": "VSCODE",
            "idea": "IDEA",
            "pycharm": "PYCHARM"
        }
        """
        ApplicationRegistry.load_applications()
        return ApplicationRegistry.get_acronyms_map()

    @classmethod
    def get_application_message(cls) -> List[Dict[str, str]]:
        """获得所有applications的消息列表
        Returns:
            [
                {
                    "title": "VSCODE",
                    "subTitle": "vsc",
                    "icoPath": "icons/app.png",
                    "jsonRPCAction": {
                        "method": "Flow.Launcher.ChangeQuery",
                        "parameters": ["r vsc", False],
                        "dontHideAfterAction": True,
                    },
                    "score": 0,
                },
            ]
        """
        application_dict = ConcreteFactory.get_application_acronyms()
        keys = list(application_dict.keys())
        return [
            {
                "title": application_dict[keys[i]],
                "subTitle": keys[i],
                "icoPath": f"icons/{keys[i]}_icon.png",
                "jsonRPCAction": {
                    "method": "Flow.Launcher.ChangeQuery",
                    "parameters": [f"r {keys[i]}", False],
                    "dontHideAfterAction": True,
                },
                "score": 0,
            }
            for i in range(len(keys))
        ]
