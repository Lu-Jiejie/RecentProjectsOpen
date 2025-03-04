import logging
import os
import pathlib
import time
from pathlib import Path
from typing import Any

from click import UsageError

LOG_PATH = Path(__file__).parent / "logs"


def get_logger(log_path=None):
    # log_path是存放日志的路径,如果不存在这个logs文件夹，那么需要创建出来。
    if not log_path:
        log_path = LOG_PATH
    else:
        log_path = pathlib.Path(log_path)
    if not log_path.exists():
        log_path.mkdir()
    logname = str(log_path.joinpath("chat_%s.log" % time.strftime("%Y_%m_%d")))
    logger = logging.getLogger()
    # 设置日志级别
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s"
    )
    # 创建一个FileHandler
    fh = logging.FileHandler(logname, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    # 创建一个StreamHandler,用于输出到控制台
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(formatter)
    # 添加两个Handler
    if not logger.handlers:
        logger.addHandler(sh)
        logger.addHandler(fh)
    return logger


CONFIG_FOLDER = Path(__file__).parent
CONFIG_PATH = CONFIG_FOLDER / ".env"

DEFAULT_CONFIG = {
    "VISUAL_STUDIO_CODE_DOWNLOAD": os.getenv("VISUAL_STUDIO_CODE_DOWNLOAD", ""),
    "VISUAL_STUDIO_CODE_STORAGE": os.getenv("VISUAL_STUDIO_CODE_STORAGE", ""),
    "ANDROID_STUDIO_DOWNLOAD": os.getenv("ANDROID_STUDIO_DOWNLOAD", ""),
    "ANDROID_STUDIO_STORAGE": os.getenv("ANDROID_STUDIO_STORAGE", ""),
    "INTELLIJ_IDEA_DOWNLOAD": os.getenv("INTELLIJ_IDEA_DOWNLOAD", ""),
    "INTELLIJ_IDEA_STORAGE": os.getenv("INTELLIJ_IDEA_STORAGE", ""),
    "GOLAND_DOWNLOAD": os.getenv("GOLAND_DOWNLOAD", ""),
    "GOLAND_STORAGE": os.getenv("GOLAND_STORAGE", ""),
    "CLION_DOWNLOAD": os.getenv("CLION_DOWNLOAD", ""),
    "CLION_STORAGE": os.getenv("CLION_STORAGE", ""),
    "PYCHARM_DOWNLOAD": os.getenv("PYCHARM_DOWNLOAD", ""),
    "PYCHARM_STORAGE": os.getenv("PYCHARM_STORAGE", ""),
    "CURSOR_DOWNLOAD": os.getenv("CURSOR_DOWNLOAD", ""),
    "CURSOR_STORAGE": os.getenv("CURSOR_STORAGE", ""),
}


class Config(dict):
    def __init__(self, config_path: Path, **defaults: Any):
        self.config_path = config_path
        # 如果配置文件存在，读取配置文件，如果有默认配置项不在配置文件中，写入配置文件
        if self._exists:
            self._read()
            has_new_config = False
            for key, value in defaults.items():
                if key not in self:
                    has_new_config = True
                    self[key] = value
            if has_new_config:
                self._write()
        # 如果配置文件不存在，创建配置文件
        else:
            config_path.parent.mkdir(parents=True, exist_ok=True)
            super().__init__(**defaults)
            self._write()

    @property
    def _exists(self) -> bool:
        return self.config_path.exists()

    def _write(self) -> None:
        with open(self.config_path, "w", encoding="utf-8") as file:
            string_config = ""
            for key, value in self.items():
                string_config += f"{key}={value}\n"
            file.write(string_config)

    def _read(self) -> None:
        with open(self.config_path, "r", encoding="utf-8") as file:
            for line in file:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    self[key] = value

    def get(self, key: str) -> str:  # type: ignore
        value = os.getenv(key) or super().get(key)
        if not value:
            raise UsageError(f"Missing config key: {key}")
        return value

    def rewrite(self, new_config: dict[str]) -> None:
        with open(self.config_path, "w+", encoding="utf-8") as _:
            for key, value in new_config.items():
                self[key] = value
            self._write()


cfg = Config(CONFIG_PATH, **DEFAULT_CONFIG)


if __name__ == "__main__":
    for key, value in cfg.items():
        print(f"{key}: {value}")
