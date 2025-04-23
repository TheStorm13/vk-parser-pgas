from tkinter import Menu


class HotkeysManager:
    SELECTION_BG = "#0078D7"  # Цвет фона выделения (синий)
    SELECTION_FG = "white"  # Цвет текста при выделении

    @staticmethod
    def setup_entry_bindings(entry, placeholder):
        """Настраивает горячие клавиши и контекстное меню для поля ввода"""

        # Применяем стиль к entry
        entry.configure(style='Custom.TEntry')

        # Бинды для горячих клавиш
        entry.bind('<Control-c>', lambda e: HotkeysManager._copy(e, entry))
        entry.bind('<Control-v>', lambda e: HotkeysManager._paste(e, entry))
        entry.bind('<Control-x>', lambda e: HotkeysManager._cut(e, entry))

        # Контекстное меню
        entry.bind('<Button-3>', lambda e: HotkeysManager._show_context_menu(e, entry))

    @staticmethod
    def _copy(event, entry):
        """Обработчик копирования"""
        entry.event_generate('<<Copy>>')
        return "break"

    @staticmethod
    def _paste(event, entry):
        """Обработчик вставки"""
        entry.event_generate('<<Paste>>')
        return "break"

    @staticmethod
    def _cut(event, entry):
        """Обработчик вырезания"""
        entry.event_generate('<<Cut>>')
        return "break"

    @staticmethod
    def _show_context_menu(event, entry):
        """Показывает контекстное меню"""
        context_menu = Menu(entry, tearoff=0)

        # Добавляем команды в меню
        context_menu.add_command(label="Копировать (Ctrl+C)",
                                 command=lambda: entry.event_generate('<<Copy>>'))
        context_menu.add_command(label="Вставить (Ctrl+V)",
                                 command=lambda: entry.event_generate('<<Paste>>'))
        context_menu.add_command(label="Вырезать (Ctrl+X)",
                                 command=lambda: entry.event_generate('<<Cut>>'))
        context_menu.add_separator()
        context_menu.add_command(label="Выделить всё",
                                 command=lambda: entry.select_range(0, 'end'))

        # Показываем меню на позиции мыши
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()
