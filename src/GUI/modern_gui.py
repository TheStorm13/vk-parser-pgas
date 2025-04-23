from tkinter import ttk

from ttkthemes import ThemedTk

from src.GUI.styles import Styles
from src.GUI.windows.main_window.main_window import MainWindow


class ModernGui(ThemedTk):
    def __init__(self):
        super().__init__()
        self.title("Сбор постов для ПГАС")
        self.geometry("1000x800")
        self.center_window()
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

    def center_window(self):
        """
        Центрирует окно на экране.
        """
        self.update_idletasks()  # Обновляем информацию о размерах окна
        width = self.winfo_width()  # Ширина окна
        height = self.winfo_height()  # Высота окна
        screen_width = self.winfo_screenwidth()  # Ширина экрана
        screen_height = self.winfo_screenheight()  # Высота экрана

        # Вычисляем координаты для центрирования окна
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Устанавливаем положение окна
        self.geometry(f"+{x}+{y}")


if __name__ == "__main__":
    app = ModernGui()
    app.mainloop()
