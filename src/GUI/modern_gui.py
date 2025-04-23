from tkinter import ttk

from ttkthemes import ThemedTk

from src.GUI.styles import Styles
from src.GUI.windows.main_window.main_window import MainWindow


class ModernGui(ThemedTk):
    def __init__(self):
        super().__init__()
        self.title("Сбор постов для ПГАС")
        self.geometry("500x600")
        # todo: проверить соверменную тему
        self.set_theme("arc")  # Используем современную тему

        # Убираем лишние отступы и границы
        self.configure(bg="white")  # Устанавливаем фон окна
        self.main_frame = ttk.Frame(self, padding=10)  # Убираем лишний паддинг
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)  # Убираем лишние отступы

        # Настройка стилей через класс Styles
        self.style = Styles.configure_styles(self)  # Передаем корневое окно
        self.title_font, self.label_font, self.button_font = Styles.get_custom_fonts()  # Получаем шрифты

        # Создаем и соединяем MainWindow
        self.main_window = MainWindow(self)
        # todo: обработку ошибок и показ окон с ними

        # Отключаем фокусный индикатор для кнопки
        self.style.map("Accent.TButton", focus=[("focus", "!focus", "")])

        # Configure grid weights for resizing
        self.main_frame.columnconfigure(1, weight=1)


if __name__ == "__main__":
    app = ModernGui()
    app.mainloop()
