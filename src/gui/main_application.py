from ttkthemes import ThemedTk

from src.core.manager.state_manager import StateManager
from src.gui.styles import Styles
from src.gui.windows.main_frame import MainFrame


class MainApplication(ThemedTk):
    def __init__(self):
        super().__init__()
        self.state_manager = StateManager()

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

        self.main_frame = MainFrame(self, self.state_manager)

        # todo: add error processing and showing windows with them

        # Disable focus indicator for buttons in "Accent" style
        # self.style.map("Accent.TButton", focus=[("focus", "!focus", "")])

        # Configure grid layout for dynamic resizing
        # self.main_frame.columnconfigure(1, weight=1)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """Обрабатываем закрытие приложения (например, сохранить данные)"""
        # todo
        print("Сохраняем состояние перед закрытием...")
        self.destroy()
