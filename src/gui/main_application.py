from ttkthemes import ThemedTk

from src.core.manager.state_manager import StateManager
from src.core.manager.task_manager import TaskManager
from src.gui.styles import Styles
from src.gui.controller.main_frame_controller import MainFrameController
from src.gui.windows.message_box import CustomMessageBox


class MainApplication(ThemedTk):
    def __init__(self):
        super().__init__()
        self.state_manager = StateManager()
        self.task_manager = TaskManager(self, self.state_manager)

        self.title("Сбор постов для ПГАС")
        self.geometry("800x800")

        # Set a modern theme
        self.set_theme("arc")

        # Configure application styles and fonts
        self.style = Styles.configure_styles(self)  # Pass the root window to style manager

        # Configure background color and remove extraneous padding
        self.configure(bg="white")
        # self.main_frame = MainFrame(self, self.manager)  # Frame for content, with minimal padding
        # self.main_frame.pack(fill="both", expand=True)

        # Initialize main application window
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.main_frame = MainFrameController(self, self.state_manager, self.task_manager)

        # todo: add error processing and showing windows with them

        # Disable focus indicator for buttons in "Accent" style
        # self.style.map("Accent.TButton", focus=[("focus", "!focus", "")])

        # Configure grid layout for dynamic resizing
        # self.main_frame.columnconfigure(1, weight=1)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        try:
            if self.task_manager.is_task_stopped():
                self.task_manager.stop_task()
                CustomMessageBox(self, "Информация", "Все фоновые задачи остановлены.")
        except Exception as e:
            print(f"Ошибка при завершении программы: {str(e)}")
        finally:
            self.destroy()
