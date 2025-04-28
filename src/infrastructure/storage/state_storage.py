import json
import os
from dataclasses import asdict

from src.core.model.state_app import StateApp
from src.infrastructure.logger.logger import setup_logger

logger = setup_logger(__name__)


class StateStorage:
    _DEFAULT_FILENAME = "state.json"

    def __init__(self):
        # Set the path where the application state will be stored
        self.state_path = self._get_storage_path()

    @staticmethod
    def _get_storage_path() -> str:
        """
        Determines the directory where the application state will be saved.
        On Windows, the data is stored in the AppData directory;
        on Unix-like systems, it is stored in the user's configuration folder.
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
        Saves the current application state to a JSON file.
        If the storage directory does not exist, it creates it.
        """

        if not os.path.exists(self.state_path):
            os.makedirs(self.state_path)
            logger.info("Create dir for state storage: " + self.state_path)

        file_path = os.path.join(self.state_path, self._DEFAULT_FILENAME)

        # Write the state to a JSON file with formatting
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(asdict(state), f, ensure_ascii=False, indent=4)
        logger.debug("State saved")

    def load_state(self) -> StateApp | None:
        """
        Loads the application state from a JSON file.
        If the file does not exist, returns a new instance of `StateApp`.
        """

        file_path = os.path.join(self.state_path, self._DEFAULT_FILENAME)
        if not os.path.exists(file_path):
            logger.info("State file not found. Create new manager")
            return StateApp()
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

                # Deserialize the JSON data into a StateApp instance
                state = StateApp(**data)
                logger.info("State file loaded")
        except Exception as e:
            # If an error occurs, delete the corrupted storage and create a new state
            logger.error(f"Failed to load state: {e}")
            self.delete_state_storage()
            return StateApp()

        return state

    def delete_state_storage(self) -> None:
        """
        Deletes the state file (state.json) and the entire directory
        if it becomes empty after file deletion.
        """
        try:
            if os.path.exists(self.state_path):
                # Iterate through all files and directories in the state path
                for root, dirs, files in os.walk(self.state_path, topdown=False):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Delete individual files
                        os.remove(file_path)
                        logger.debug(f"File {file_path} deleted successfully")

                    for directory in dirs:
                        dir_path = os.path.join(root, directory)
                        # Delete directories if empty
                        os.rmdir(dir_path)
                        logger.debug(f"Directory {dir_path} deleted successfully")
                # Remove the main state path directory
                os.rmdir(self.state_path)
                logger.info(
                    f"State storage directory {self.state_path} deleted successfully"
                )
            else:
                logger.info(f"State storage directory {self.state_path} does not exist")
        except Exception as e:
            logger.error(f"Failed to delete state storage: {e}")

    def update(self, state: StateApp):
        """
        Updates and saves the current application state to a JSON file.
        """
        self.save_state(state)
