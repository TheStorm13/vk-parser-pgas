from tkinter import ttk


class ButtonComponent:
    """Управляет кнопками запуска, описания и очистки."""

    def __init__(self, root, on_run, on_stop, on_description, on_remove_files):
        """Инициализирует компонент кнопок.

        Args:
            root: Родительский контейнер.
            on_run: Колбэк запуска.
            on_stop: Колбэк остановки.
            on_description: Колбэк описания.
            on_remove_files: Колбэк удаления файлов.

        Returns:
            None

        """
        self.root = root
        self.on_run = on_run
        self.on_stop = on_stop
        self.on_description = on_description
        self.on_remove_files = on_remove_files

        self.frame = ttk.Frame(self.root, padding=5)

        self._init_components()

    def _init_components(self):
        """Создает и размещает кнопки.

        Returns:
            None

        """
        self.button_run_stop = ttk.Button(
            self.frame,
            text="Запустить",
            command=self.toggle_run_stop,
            style="Accent.TButton",
            takefocus=False,
        )
        self.button_run_stop.grid(row=0, column=0, sticky="nsew", pady=5)

        self.description_button = ttk.Button(
            self.frame,
            text="Описание",
            command=self.on_description,
            style="Accent.TButton",
        )
        self.description_button.grid(row=1, column=0, sticky="nsew", pady=5)

        self.remove_files = ttk.Button(
            self.frame,
            text="Удалить временные файлы",
            command=self.on_remove_files,
            style="Accent.TButton",
        )
        self.remove_files.grid(row=2, column=0, sticky="nsew", pady=5)

    def toggle_run_stop(self):
        """Переключает состояние кнопки запуска.

        Returns:
            None

        """
        if self.button_run_stop["text"] == "Запустить":
            self.button_run_stop.config(text="Остановить", style="Accent.TButton")
            self.on_run()
        else:
            self.button_run_stop.config(text="Запустить", style="Accent.TButton")
            self.on_stop()

    def set_run_state(self):
        """Сбрасывает кнопку в состояние "Запустить".

        Returns:
            None

        """
        self.button_run_stop.config(text="Запустить", style="Accent.TButton")
