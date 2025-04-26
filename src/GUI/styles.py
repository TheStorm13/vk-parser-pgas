from tkinter import font as tkfont
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

        # Configure frame styles
        style.configure("TFrame", background="white", borderwidth=0)

        # Configure label styles
        style.configure("TLabel", background="white", font=("Helvetica", 12))

        # Configure button styles
        style.configure("TButton", font=("Helvetica", 12, "bold"))

        # Set focus mapping for custom buttons (e.g., Accent.TButton)
        style.map("Accent.TButton", focus=[("focus", "!focus", "")])

        # Configure custom Entry styling for selection (focus and non-focus states)
        style.map('Custom.TEntry',
                  selectbackground=[('!focus', Styles.SELECTION_BG),
                                    ('focus', Styles.SELECTION_BG)],
                  selectforeground=[('!focus', Styles.SELECTION_FG),
                                    ('focus', Styles.SELECTION_FG)])

        return style

    @staticmethod
    def get_custom_fonts():
        """
        Define and return custom fonts for use in the application.
        :return: A tuple containing (title_font, label_font, button_font).
        """

        title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        label_font = tkfont.Font(family="Helvetica", size=12)
        button_font = tkfont.Font(family="Helvetica", size=12, weight="bold")

        return title_font, label_font, button_font
