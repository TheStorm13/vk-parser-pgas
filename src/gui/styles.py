from tkinter import ttk


class Styles:
    # Colors for consistent styling
    SELECTION_BG = "#0078D7"  # Selection background color (blue)
    SELECTION_FG = "white"  # Selection foreground color (text)

    @staticmethod
    def configure_styles(root):
        """
        Configure global styles for ttk widgets in the application.
        :param root: Root Tkinter widget to associate the styles with.
        :return: Configured ttk.Style instance.
        """
        style = ttk.Style(root)

        title_font = ("Helvetica", 16, "bold")
        label_font = ("Helvetica", 12)
        button_font = ("Helvetica", 12, "bold")

        # Configure frame styles
        style.configure("TFrame", background="white", borderwidth=0)

        style.configure("Title.TLabel", background="white", font=title_font)

        # Configure label styles
        style.configure("TLabel", background="white", font=label_font)

        # Configure button styles
        style.configure("TButton", font=button_font)

        # Set focus mapping for custom buttons (e.g., Accent.TButton)
        style.map("Accent.TButton", focus=[("focus", "!focus", "")])

        # Configure custom Entry styling for selection (focus and non-focus states)
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
