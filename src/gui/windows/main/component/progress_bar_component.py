from tkinter import ttk

from src.core.model.state_app import StateApp


class ProgressBarComponent:
    """Управляет индикатором прогресса и подписью."""

    def __init__(self, parent, state_manager):
        """Инициализирует индикатор и подписку на состояние.

        Args:
            parent: Родительский контейнер.
            state_manager: Менеджер состояния приложения.

        Returns:
            None

        """
        self.state_manager = state_manager
        self.state_manager.add_observer(self)

        self.frame = ttk.Frame(parent, padding=5)

        self.progress = ttk.Progressbar(
            self.frame, orient="horizontal", length=300, mode="indeterminate",
        )

        self.progress_label = ttk.Label(
            self.frame, text="Опять работать?", style="TLabel",
        )
        self._setup_progress_bar()

    def _setup_progress_bar(self):
        """Размещает элементы и скрывает их.

        Returns:
            None

        """
        self.progress.grid(row=0, column=0, pady=10)
        self.progress_label.grid(row=1, column=0, pady=5)
        self.hide()

    def show(self):
        """Показывает индикатор и запускает анимацию.

        Returns:
            None

        """
        self.frame.grid()
        self.progress.grid()
        self.progress_label.grid()
        self.progress_label.config(text="Опять работать?")
        self.progress.start(20)

    def hide(self):
        """Останавливает анимацию и скрывает элементы.

        Returns:
            None

        """
        self.progress.stop()
        self.progress.grid_remove()
        self.progress_label.grid_remove()
        self.frame.grid_remove()

    def update(self, state: StateApp):
        """Обновляет текст подписи по состоянию.

        Args:
            state: Состояние приложения (StateApp).

        Returns:
            None

        """
        self.progress_label.config(text=state.progress)
