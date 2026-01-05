from tkinter import ttk

from src.core.manager.state_manager import StateManager
from src.gui.manager.hotkeys_manager import HotkeysManager
from src.gui.styles import Styles
from src.infrastructure.utils.data_utils import DateUtils


class FormComponent:
    """Управляет формой ввода параметров."""

    def __init__(self, root, state_manager):
        """Инициализирует форму и стили.

        Args:
            root: Корневой контейнер UI.
            state_manager: Менеджер состояния (StateManager).

        Returns:
            None

        """
        self.state_manager: StateManager = state_manager
        self.state_manager.add_observer(self)

        self.root = root
        self.frame = ttk.Frame(self.root, padding=5)

        self.style = Styles.configure_styles(self.root)
        self._init_components()

        self.frame.columnconfigure(1, weight=1, minsize=300)

    def _init_components(self):
        """Создает поля ввода формы.

        Returns:
            None

        """
        end_date, full_name, start_date, vk_group_url, vk_token = (
            self.get_data_from_state()
        )

        self.entry_vk_token = self._create_field("Сервисный ключ VK:", 1, vk_token)
        self.entry_vk_group = self._create_field(
            "Ссылка на сообщество:", 2, vk_group_url,
        )
        self.entry_full_name = self._create_field("ФИО:", 3, full_name)
        self.entry_start_date = self._create_field(
            "Начальная дата (дд.мм.гггг):", 4, start_date,
        )
        self.entry_end_date = self._create_field(
            "Конечная дата (дд.мм.гггг):", 5, end_date,
        )

    def get_data_from_state(self):
        """Читает значения полей из состояния.

        Returns:
            Кортеж значений полей.

        """
        vk_token = self.state_manager.state.vk_token
        vk_group_url = self.state_manager.state.vk_group_url
        full_name = self.state_manager.state.full_name
        start_date = DateUtils.timestamp_to_str(self.state_manager.state.start_date)
        end_date = DateUtils.timestamp_to_str(self.state_manager.state.end_date)
        return end_date, full_name, start_date, vk_group_url, vk_token

    def _create_field(self, label_text, row, placeholder):
        """Создает поле ввода с плейсхолдером.

        Args:
            label_text: Текст метки (str).
            row: Номер строки (int).
            placeholder: Значение по умолчанию.

        Returns:
            Виджет Entry.

        """
        label = ttk.Label(self.frame, text=label_text, style="TLabel")
        label.grid(row=row, column=0, sticky="nsw", pady=5)

        entry = ttk.Entry(self.frame, style="TLabel")
        entry.insert(0, placeholder)
        entry.configure(foreground="gray")

        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, "end")
                entry.configure(foreground="black")

        def on_focus_out(event):
            if entry.get() == "":
                entry.insert(0, placeholder)
                entry.configure(foreground="gray")

        HotkeysManager.setup_entry_bindings(entry)
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        entry.grid(row=row, column=1, sticky="nsew", padx=5, pady=5)

        return entry

    def enter_data(self):
        """Сохраняет введенные данные в состояние.

        Returns:
            None

        """
        start_date = DateUtils.str_to_timestamp(self.entry_start_date.get())
        end_date = DateUtils.str_to_timestamp(
            self.entry_end_date.get(), is_end_of_day=True,
        )
        self.state_manager.update_state("vk_token", self.entry_vk_token.get())
        self.state_manager.update_state("vk_group_url", self.entry_vk_group.get())
        self.state_manager.update_state("full_name", self.entry_full_name.get())
        self.state_manager.update_state("start_date", start_date)
        self.state_manager.update_state("end_date", end_date)

    def update(self, state):
        """Обновляет UI при изменении состояния.

        Args:
            state: Новое состояние приложения.

        Returns:
            None

        """
        # TODO: реализовать обновление UI по состоянию
