from tkinter import ttk

from src.GUI.manager.hotkeys_manager import HotkeysManager
from src.utils.data_utils import DateUtils


class FormComponent:
    def __init__(self, parent_frame, label_font, state):
        self.state = state
        self.frame = parent_frame
        self.label_font = label_font
        self._init_components()

    def _init_components(self):
        """
        Initialize input fields for the form.
        Each field has a label, an entry, and placeholder text.
        """
        start_date = DateUtils.timestamp_to_str(self.state.start_date)
        end_date = DateUtils.timestamp_to_str(self.state.end_date)

        self.entry_vk_token = self._create_field(
            "Токен VK:", 1, self.state.vk_token)
        self.entry_vk_group = self._create_field(
            "Ссылка на сообщество:", 2, self.state.vk_group_url)
        self.entry_full_name = self._create_field(
            "ФИО:", 3, self.state.full_name)
        self.entry_start_date = self._create_field(
            "Начальная дата (дд.мм.гггг):", 4, start_date)
        self.entry_end_date = self._create_field(
            "Конечная дата (дд.мм.гггг):", 5, end_date)

    def _create_field(self, label_text, row, placeholder):
        # Create and position the label
        label = ttk.Label(self.frame, text=label_text, font=self.label_font)
        label.grid(row=row, column=0, sticky="w", pady=5)

        # Create entry field with placeholder text
        entry = ttk.Entry(self.frame, font=self.label_font)
        entry.insert(0, placeholder)  # Add placeholder text
        entry.configure(foreground='gray')  # Make placeholder gray

        # Event: Clear placeholder on focus
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, 'end')  # Clear text
                entry.configure(foreground='black')  # Restore default text color

        # Event: Restore placeholder if field is empty
        def on_focus_out(event):
            if entry.get() == '':
                entry.insert(0, placeholder)  # Reinsert placeholder text
                entry.configure(foreground='gray')  # Set placeholder color

        # Register hotkey bindings for the entry field
        HotkeysManager.setup_entry_bindings(entry)

        # Bind focus events to the entry field
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)

        # Position the entry field in the grid
        entry.grid(row=row, column=1, sticky="ew", pady=5)
        return entry
