from tkinter import ttk


class ButtonComponent:
    def __init__(self, root, on_run, on_stop, on_description, on_remove_files):
        self.root = root
        self.on_run = on_run
        self.on_stop = on_stop
        self.on_description = on_description
        self.on_remove_files = on_remove_files

        self.frame = ttk.Frame(self.root, padding=5)
        # self.frame.columnconfigure(0, weight=1)

        self._init_components()

    def _init_components(self):
        # Добавляем контейнер для кнопок (если их несколько)

        self.button_run_stop = ttk.Button(
            self.frame,
            text="Запустить",
            command=self.toggle_run_stop,
            style="Accent.TButton",
            takefocus=False
        )
        self.button_run_stop.grid(row=0, column=0, sticky="nsew", pady=5)  # Расположим с отступами

        self.description_button = ttk.Button(
            self.frame,
            text="Описание",
            command=self.on_description,
            style="Accent.TButton"
        )
        self.description_button.grid(row=1, column=0, sticky="nsew", pady=5)  # Рядом с предыдущей

        self.remove_files = ttk.Button(
            self.frame,
            text="Удалить временные файлы",
            command=self.on_remove_files,
            style="Accent.TButton"
        )
        self.remove_files.grid(row=2, column=0, sticky="nsew", pady=5)

    def toggle_run_stop(self):
        # Toggle the button between "Run" and "Stop"
        if self.button_run_stop["text"] == "Запустить":
            self.button_run_stop.config(text="Остановить", style="Accent.TButton")
            self.on_run()
        else:
            self.button_run_stop.config(text="Запустить", style="Accent.TButton")
            self.on_stop()

    def set_run_state(self):
        self.button_run_stop.config(text="Запустить", style="Accent.TButton")
