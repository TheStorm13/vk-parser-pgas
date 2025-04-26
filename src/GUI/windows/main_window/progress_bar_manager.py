from tkinter import ttk


class ProgressBarManager:
    def __init__(self, parent_frame, label_font):
        self.frame = parent_frame
        # Create a horizontal progress bar with an indeterminate mode for continuous progress
        self.progress = ttk.Progressbar(parent_frame,
                                        orient="horizontal",
                                        length=300,
                                        mode="indeterminate")

        # Create a label for progress description
        self.progress_label = ttk.Label(parent_frame,
                                        text="Запускается",
                                        font=label_font)
        self._setup_progress_bar()

    def _setup_progress_bar(self):
        """
        Places the progress bar and label within the parent frame and hides them initially.
        """
        self.progress.grid(row=7, column=0, columnspan=2, pady=10)
        self.progress_label.grid(row=8, column=0, columnspan=2, pady=5)
        self.hide()  # Initially hide the progress bar

    def show(self):
        """
        Displays the progress bar and label, and starts the progress animation.
        """
        self.progress.grid()  # Makes progress bar visible
        self.progress_label.grid()  # Makes label visible
        self.progress.start(20)  # Starts an indeterminate animation with 20ms interval

    def hide(self):
        """
        Stops the progress animation and hides both the progress bar and label.
        """
        self.progress.stop()  # Stops the indeterminate animation
        self.progress.grid_remove()  # Hides progress bar
        self.progress_label.config(text="Запускается")  # Resets the label's text
        self.progress_label.grid_remove()  # Hides label

    def update(self, progress: int, total_progress: int):
        # Updates the label to show progress details
        self.progress_label.config(text=f"Обработано: {int(progress)} постов")
