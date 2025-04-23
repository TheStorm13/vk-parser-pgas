from tkinter import ttk


class ProgressBarManager:
    def __init__(self, parent_frame, label_font):
        self.frame = parent_frame
        self.progress = ttk.Progressbar(parent_frame, orient="horizontal", length=400, mode="determinate")
        self.progress_label = ttk.Label(parent_frame, text="0", font=label_font)
        self._setup_progress_bar()

    def _setup_progress_bar(self):
        self.progress.grid(row=5, column=0, columnspan=2, pady=10)
        self.progress_label.grid(row=6, column=0, columnspan=2, pady=5)
        self.hide()

    def show(self):
        self.progress.grid()
        self.progress_label.grid()

    def hide(self):
        self.progress.grid_remove()
        self.progress_label.grid_remove()

    def update(self, progress: int, total_progress: int):
        percentage = min(100, (progress / total_progress) * 100)
        self.progress['value'] = percentage
        self.progress_label.config(text=f"{int(progress)}/???")
