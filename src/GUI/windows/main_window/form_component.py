from tkinter import ttk

from src.GUI.manager.hotkeys_manager import HotkeysManager


class FormComponent:
    def __init__(self, parent_frame, label_font):
        self.frame = parent_frame
        self.label_font = label_font
        self._init_components()

    def _init_components(self):
        self.entry_start_date = self._create_field("Начальная дата (дд.мм.гггг):", 1, "01.01.2024")
        self.entry_end_date = self._create_field("Конечная дата (дд.мм.гггг):", 2, "31.12.2024")
        self.entry_full_name = self._create_field("ФИО:", 3, "Иванов Иван Иванович")

    def _create_field(self, label_text, row, placeholder):
        label = ttk.Label(self.frame, text=label_text, font=self.label_font)
        label.grid(row=row, column=0, sticky="w", pady=5)

        entry = ttk.Entry(self.frame, font=self.label_font)
        entry.insert(0, placeholder)
        entry.configure(foreground='gray')

        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, 'end')
                entry.configure(foreground='black')

        def on_focus_out(event):
            if entry.get() == '':
                entry.insert(0, placeholder)
                entry.configure(foreground='gray')

        # Настраиваем горячие клавиши и контекстное меню
        HotkeysManager.setup_entry_bindings(entry, placeholder)

        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
        entry.grid(row=row, column=1, sticky="ew", pady=5)
        return entry
