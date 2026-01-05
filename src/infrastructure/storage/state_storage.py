import json
import os
from dataclasses import asdict

from src.core.model.state_app import StateApp
from src.infrastructure.logger.logger import setup_logger

logger = setup_logger(__name__)


class StateStorage:
    """Хранит и управляет состоянием приложения."""

    _DEFAULT_FILENAME = "state.json"

    def __init__(self):
        self.state_path = self._get_storage_path()

    @staticmethod
    def _get_storage_path() -> str:
        """Определяет директорию хранения состояния.

        Returns:
            str: Абсолютный путь к директории.

        """
        if os.name == "nt":
            base_dir = os.getenv("APPDATA", os.getcwd())
            logger.info(f"System: Windows. APPDATA: {base_dir}")
        else:
            base_dir = os.getenv("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
            logger.info(f"System: Unix. APPDATA: {base_dir}")
        return os.path.join(base_dir, "vk_parser_pgas")

    def save_state(self, state: StateApp) -> None:
        """Сохраняет состояние в JSON.

        Args:
            state (StateApp): Текущее состояние.

        Returns:
            None: Ничего не возвращает.

        """
        if not os.path.exists(self.state_path):
            os.makedirs(self.state_path)
            logger.info("Create dir for state storage: " + self.state_path)

        file_path = os.path.join(self.state_path, self._DEFAULT_FILENAME)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(asdict(state), f, ensure_ascii=False, indent=4)
        logger.debug("State saved")

    def load_state(self) -> StateApp:
        """Загружает состояние из JSON.

        Returns:
            StateApp: Загруженное состояние.

        """
        file_path = os.path.join(self.state_path, self._DEFAULT_FILENAME)
        if not os.path.exists(file_path):
            logger.info("State file not found. Create new manager")
            return StateApp()
        try:
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)
                state = StateApp(**data)
                logger.info("State file loaded")
        except Exception as e:
            logger.error(f"Failed to load state: {e}")
            self.delete_state_storage()
            return StateApp()

        return state

    def delete_state_storage(self) -> None:
        """Удаляет файл состояния и директорию хранения при необходимости.

        Returns:
            None: Ничего не возвращает.

        """
        try:
            if os.path.exists(self.state_path):
                for root, dirs, files in os.walk(self.state_path, topdown=False):
                    for file in files:
                        file_path = os.path.join(root, file)
                        os.remove(file_path)
                        logger.debug(f"File {file_path} deleted successfully")

                    for directory in dirs:
                        dir_path = os.path.join(root, directory)
                        os.rmdir(dir_path)
                        logger.debug(f"Directory {dir_path} deleted successfully")
                os.rmdir(self.state_path)
                logger.info(
                    f"State storage directory {self.state_path} deleted successfully",
                )
            else:
                logger.info(f"State storage directory {self.state_path} does not exist")
        except Exception as e:
            logger.error(f"Failed to delete state storage: {e}")

    def update(self, state: StateApp) -> None:
        """Обновляет и сохраняет состояние.

        Args:
            state (StateApp): Новое состояние.

        Returns:
            None: Ничего не возвращает.

        """
        self.save_state(state)
