from tkinter import ttk

from src.core.model.state_app import StateApp


class ProgressBarComponent:
    def __init__(self, parent, state_manager):
        self.state_manager = state_manager
        self.state_manager.add_observer(self)

        self.frame = ttk.Frame(parent, padding=5)

        # Create a horizontal progress bar with an indeterminate mode for continuous progress
        self.progress = ttk.Progressbar(
            self.frame, orient="horizontal", length=300, mode="indeterminate"
        )

        # Create a label for progress description
        self.progress_label = ttk.Label(
            self.frame, text="Опять работать?", style="TLabel"
        )
        self._setup_progress_bar()

    def _setup_progress_bar(self):
        """
        Places the progress bar and label within the parent frame and hides them initially.
        """
        self.progress.grid(row=0, column=0, pady=10)
        self.progress_label.grid(row=1, column=0, pady=5)
        self.hide()  # Initially hide the progress bar

    def show(self):
        """
        Displays the progress bar and label, and starts the progress animation.
        """
        self.frame.grid()
        self.progress.grid()  # Makes progress bar visible
        self.progress_label.grid()  # Makes label visible
        self.progress_label.config(text="Опять работать?")  # Resets the label's text
        self.progress.start(20)  # Starts an indeterminate animation with 20ms interval

    def hide(self):
        """
        Stops the progress animation and hides both the progress bar and label.
        """
        self.progress.stop()  # Stops the indeterminate animation
        self.progress.grid_remove()  # Hides progress bar
        self.progress_label.grid_remove()  # Hides label
        self.frame.grid_remove()

    def update(self, state: StateApp):
        # Updates the label to show progress details
        self.progress_label.config(text=state.progress)
