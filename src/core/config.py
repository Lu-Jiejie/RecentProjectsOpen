import os
from pathlib import Path

from click import UsageError

CONFIG_FOLDER = Path(__file__).parent.parent
CONFIG_PATH = CONFIG_FOLDER / ".env"


class Config(dict):
    def __init__(self, config_path: Path):
        self.config_path = config_path
        if self._exists:
            self._read()
            has_new_config = False
            if has_new_config:
                self._write()
        else:
            config_path.parent.mkdir(parents=True, exist_ok=True)
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

    def get(self, key: str) -> str:
        value = os.getenv(key) or super().get(key)
        if not value:
            raise UsageError(f"Missing config key: {key}")
        return value

    def rewrite(self, new_config: dict[str]) -> None:
        with open(self.config_path, "w+", encoding="utf-8") as _:
            for key, value in new_config.items():
                self[key] = value
            self._write()


cfg = Config(CONFIG_PATH)


if __name__ == "__main__":
    for key, value in cfg.items():
        print(f"{key}: {value}")
        print(cfg.get(key))
