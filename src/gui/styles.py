from tkinter import ttk


class Styles:
    """Хранит и настраивает стили ttk."""

    SELECTION_BG = "#0078D7"
    SELECTION_FG = "white"

    @staticmethod
    def configure_styles(root):
        """Настраивает глобальные стили ttk.

        Args:
            root: Корневой виджет Tk.

        Returns:
            Экземпляр ttk.Style.

        """
        style = ttk.Style(root)

        title_font = ("Helvetica", 16, "bold")
        label_font = ("Helvetica", 12)
        button_font = ("Helvetica", 12, "bold")

        style.configure("TFrame", background="white", borderwidth=0)
        style.configure("Title.TLabel", background="white", font=title_font)
        style.configure("TLabel", background="white", font=label_font)
        style.configure("TButton", font=button_font)

        style.map("Accent.TButton", focus=[("focus", "!focus", "")])

        style.map(
            "Custom.TEntry",
            selectbackground=[
                ("!focus", Styles.SELECTION_BG),
                ("focus", Styles.SELECTION_BG),
            ],
            selectforeground=[
                ("!focus", Styles.SELECTION_FG),
                ("focus", Styles.SELECTION_FG),
            ],
        )

        return style
