from tkinter import ttk

from ttkthemes import ThemedTk

from src.GUI.styles import Styles
from src.GUI.windows.main_window.main_window import MainWindow
from src.state import state_storage
from src.state.state_storage import StateStorage


class PostCollectorGui(ThemedTk):
    def __init__(self):
        super().__init__()
        self.state_storage = StateStorage()
        self.state = self.state_storage.load_state()
        self.title("Сбор постов для ПГАС")
        self.geometry("800x800")

        # Set a modern theme
        self.set_theme("arc")

        # Configure background color and remove extraneous padding
        self.configure(bg="white")
        self.main_frame = ttk.Frame(self, padding=10)  # Frame for content, with minimal padding
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Configure application styles and fonts
        self.style = Styles.configure_styles(self)  # Pass the root window to style manager

        # Set custom fonts for different UI elements
        self.title_font, self.label_font, self.button_font = Styles.get_custom_fonts()

        # Initialize main application window
        self.main_window = MainWindow(self, self.state)

        # todo: add error processing and showing windows with them

        # Disable focus indicator for buttons in "Accent" style
        self.style.map("Accent.TButton", focus=[("focus", "!focus", "")])

        # Configure grid layout for dynamic resizing
        self.main_frame.columnconfigure(1, weight=1)


if __name__ == "__main__":
    app = PostCollectorGui()
    app.mainloop()
