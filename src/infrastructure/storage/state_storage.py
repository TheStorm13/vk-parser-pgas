import json
import os
from dataclasses import asdict

from src.core.model.state_app import StateApp
from src.infrastructure.logger.logger import setup_logger

logger = setup_logger(__name__)


class StateStorage:
    _DEFAULT_FILENAME = "state.json"

    def __init__(self):

        self.state_path = self._get_storage_path()

    @staticmethod
    def _get_storage_path() -> str:
        """
        Определяет директорию, в которую будет сохраняться состояние приложения.
        На Windows данные сохраняются в AppData, на Unix-системах в конфигурационной папке пользователя.
        """
        if os.name == "nt":  # Windows
            base_dir = os.getenv("APPDATA", os.getcwd())
            logger.info(f"System: Windows. APPDATA: {base_dir}")
        else:  # Unix-like (Linux, macOS)
            base_dir = os.getenv("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
            logger.info(f"System: Unix. APPDATA: {base_dir}")
        return os.path.join(base_dir, "vk_parser_pgas")

    def save_state(self, state: StateApp) -> None:
        """
        Сохраняет текущее состояние в JSON-файл.
        """
        if not os.path.exists(self.state_path):
            os.makedirs(self.state_path)
            logger.info("Create dir for state storage: " + self.state_path)

        file_path = os.path.join(self.state_path, self._DEFAULT_FILENAME)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(asdict(state), f, ensure_ascii=False, indent=4)
        logger.debug("State saved")

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
            state = StateApp(**data)
            logger.info("State file loaded")

        return state

    def delete_state_storage(self) -> None:
        """
        Удаляет файлы состояния (state.json) и всю директорию, если она пуста.
        """
        try:
            if os.path.exists(self.state_path):
                # Удаляем все файлы в директории
                for root, dirs, files in os.walk(self.state_path, topdown=False):
                    for file in files:
                        file_path = os.path.join(root, file)
                        os.remove(file_path)
                        logger.debug(f"File {file_path} deleted successfully")
                    # Удаляем вложенные директории
                    for directory in dirs:
                        dir_path = os.path.join(root, directory)
                        os.rmdir(dir_path)
                        logger.debug(f"Directory {dir_path} deleted successfully")
                # Удаляем саму директорию
                os.rmdir(self.state_path)
                logger.info(f"State storage directory {self.state_path} deleted successfully")
            else:
                logger.info(f"State storage directory {self.state_path} does not exist")
        except Exception as e:
            logger.error(f"Failed to delete state storage: {e}")
