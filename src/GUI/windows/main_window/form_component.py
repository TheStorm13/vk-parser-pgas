from tkinter import ttk


class FormComponent:
    def __init__(self, parent_frame, label_font):
        self.frame = parent_frame
        self.label_font = label_font
        self._init_components()

    def _init_components(self):
        self.entry_start_date = self._create_field("Начальная дата (дд.мм.гггг):", 1)
        self.entry_end_date = self._create_field("Конечная дата (дд.мм.гггг):", 2)
        self.entry_full_name = self._create_field("ФИО:", 3)

    def _create_field(self, label_text, row):
        label = ttk.Label(self.frame, text=label_text, font=self.label_font)
        label.grid(row=row, column=0, sticky="w", pady=5)
        entry = ttk.Entry(self.frame, font=self.label_font)
        entry.grid(row=row, column=1, sticky="ew", pady=5)
        return entry
