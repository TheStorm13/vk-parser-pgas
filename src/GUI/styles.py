from tkinter import font as tkfont
from tkinter import ttk


class Styles:
    @staticmethod
    def configure_styles(root):
        """
        Настройка стилей ttk-компонентов.
        :param root: объект Tk (корневое окно или ThemedTk)
        :return: объект Style для дальнейшего использования.
        """
        style = ttk.Style(root)

        # Стили ttk-компонентов
        style.configure("TFrame", background="white", borderwidth=0)
        style.configure("TLabel", background="white", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12, "bold"))
        style.map("Accent.TButton", focus=[("focus", "!focus", "")])

        return style

    @staticmethod
    def get_custom_fonts():
        """
        Создание и возврат пользовательских шрифтов.
        :return: шрифты для заголовков, меток и кнопок.
        """
        title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        label_font = tkfont.Font(family="Helvetica", size=12)
        button_font = tkfont.Font(family="Helvetica", size=12, weight="bold")

        return title_font, label_font, button_font
