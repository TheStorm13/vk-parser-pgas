import json
import logging
import os
from dataclasses import asdict

from src.core.model.state_app import StateApp

logger = logging.getLogger(__name__)


class StateStorage:
    _DEFAULT_FILENAME = "manager.json"

    def __init__(self, state: StateApp = None):
        self.state: StateApp = state
        self.state_path = self._get_storage_path()

    @staticmethod
    def _get_storage_path() -> str:
        """
        Определяет директорию, в которую будет сохраняться состояние приложения.
        На Windows данные сохраняются в AppData, на Unix-системах в конфигурационной папке пользователя.
        """
        if os.name == "nt":  # Windows
            base_dir = os.getenv("APPDATA", os.getcwd())
        else:  # Unix-like (Linux, macOS)
            base_dir = os.getenv("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
        return os.path.join(base_dir, "vk_parser_pgas")

    def save_state(self) -> None:
        """
        Сохраняет текущее состояние в JSON-файл.
        """
        if not os.path.exists(self.state_path):
            # todo: Это точно должно быть???
            os.makedirs(self.state_path)

        file_path = os.path.join(self.state_path, self._DEFAULT_FILENAME)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(asdict(self.state), f, ensure_ascii=False, indent=4)

    def load_state(self) -> StateApp | None:
        """
        Загружает состояние из JSON-файла.
        Если файл отсутствует, возвращает None.
        """
        file_path = os.path.join(self.state_path, self._DEFAULT_FILENAME)
        if not os.path.exists(file_path):
            logger.info("State file not found. Create new manager")
            return StateApp()

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.state = StateApp(**data)
            logger.info("State file loaded")

        return self.state
