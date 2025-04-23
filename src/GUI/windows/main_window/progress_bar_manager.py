from tkinter import ttk


class ProgressBarManager:
    def __init__(self, parent_frame, label_font):
        self.frame = parent_frame
        self.progress = ttk.Progressbar(parent_frame, orient="horizontal",
                                        length=300, mode="indeterminate")
        self.progress_label = ttk.Label(parent_frame, text="Запускается", font=label_font)
        self._setup_progress_bar()

    def _setup_progress_bar(self):
        self.progress.grid(row=5, column=0, columnspan=2, pady=10)
        self.progress_label.grid(row=6, column=0, columnspan=2, pady=5)
        self.hide()

    def show(self):
        self.progress.grid()
        self.progress_label.grid()
        # Запускаем анимацию при показе
        self.progress.start(20)

    def hide(self):
        # Останавливаем анимацию при скрытии
        self.progress.stop()
        self.progress.grid_remove()
        self.progress_label.grid_remove()

    def update(self, progress: int, total_progress: int):
        self.progress_label.config(text=f"Обработано: {int(progress)} постов")
