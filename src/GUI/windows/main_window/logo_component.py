from tkinter import ttk

from PIL import Image, ImageTk


class LogoComponent:
    def __init__(self, parent, logo_path, width=100, height=80):
        """
        Логика для отображения логотипа.

        :param parent: родительский контейнер, в котором будет отображаться логотип.
        :param logo_path: путь к файлу логотипа.
        :param width: ширина логотипа.
        :param height: высота логотипа.
        """
        self.parent = parent
        self.logo_path = logo_path
        self.width = width
        self.height = height
        self.logo_image = None
        self._create_logo()

    def _create_logo(self):
        """Создает виджет логотипа."""
        # Загрузка изображения
        image = Image.open(self.logo_path)
        image = image.resize((self.width, self.height), Image.Resampling.LANCZOS)
        self.logo_image = ImageTk.PhotoImage(image)

        # Создание виджета с логотипом
        logo_label = ttk.Label(self.parent, image=self.logo_image)
        logo_label.grid(row=99, column=1, sticky="se", padx=10, pady=10)

        # Настройка сетки (гарантирует, что строка не будет сжиматься)
        self.parent.grid_rowconfigure(1, weight=0)  # Строка для логотипа имеет вес 0
        self.parent.grid_columnconfigure(1, weight=0)  # Колонка для логотипа имеет вес 0
