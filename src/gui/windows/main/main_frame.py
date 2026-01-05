from tkinter import ttk

from src.core.manager.state_manager import StateManager
from src.gui.manager.ui_state_manager import UIStateManager
from src.gui.windows.main.component.button_component import ButtonComponent
from src.gui.windows.main.component.form_component import FormComponent
from src.gui.windows.main.component.progress_bar_component import ProgressBarComponent


class MainFrame:
    """Собирает и управляет главным окном приложения."""

    def __init__(self, root, state_manager: StateManager, button_callbacks):
        """Инициализирует фрейм и основные компоненты.

        Args:
            root: Корневое окно UI.
            state_manager: Менеджер состояния (StateManager).
            button_callbacks: Колбэки кнопок управления.

        Returns:
            None

        """
        self.state_manager = state_manager
        self.button_callbacks = button_callbacks

        self.root = root
        self.style = self.root.style

        self.main_frame = ttk.Frame(self.root, padding=5)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self._init_components()

        self.main_frame.columnconfigure(0, weight=1)
        for i in range(4):
            self.main_frame.rowconfigure(i, weight=0)

        self.ui_state = UIStateManager(
            [
                self.form_component.entry_vk_token,
                self.form_component.entry_vk_group,
                self.form_component.entry_start_date,
                self.form_component.entry_end_date,
                self.form_component.entry_full_name,
                self.buttons_component.button_run_stop,
                self.buttons_component.description_button,
                self.buttons_component.remove_files,
            ],
        )

        self.root.bind("<Button-1>", self._on_root_click)

        self.root.update_idletasks()
        self.root.geometry("")  # Автоматически подгоняет окно под содержимое

    def _init_components(self):
        """Создает и размещает основные компоненты окна.

        Returns:
            None

        """
        self.form_component = FormComponent(self.main_frame, self.state_manager)
        self.form_component.frame.grid(row=0, column=0, sticky="new", pady=5)

        self.progress_component = ProgressBarComponent(
            self.main_frame, self.state_manager,
        )
        self.progress_component.frame.grid(row=1, column=0, pady=5)

        self.buttons_component = ButtonComponent(
            self.main_frame,
            self.button_callbacks["run_program"],
            self.button_callbacks["stop_program"],
            self.button_callbacks["open_description_window"],
            self.state_manager.state_storage.delete_state_storage,
        )
        self.buttons_component.frame.grid(row=2, column=0, pady=5)

    def reset_ui(self):
        """Сбрасывает UI к исходному состоянию.

        Returns:
            None

        """
        self.ui_state.enable_all()
        self.progress_component.hide()
        self.buttons_component.set_run_state()

    def _on_root_click(self, event):
        """Снимает фокус при клике вне поля ввода.

        Args:
            event: Событие Tkinter.

        Returns:
            None

        """
        widget = event.widget
        if not isinstance(widget, ttk.Entry):
            self.root.focus_set()
