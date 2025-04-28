class HotkeysManager:
    # Constants for selection colors
    SELECTION_BG = "#0078D7"  # Background color for selection
    SELECTION_FG = "white"  # Foreground color for selection

    @staticmethod
    def setup_entry_bindings(entry):
        # Configure the entry widget style
        entry.configure(style="Custom.TEntry")

        # Bind keyboard shortcuts to copy, paste, and cut actions
        entry.bind("<Control-c>", lambda e: HotkeysManager._copy(entry))
        entry.bind("<Control-v>", lambda e: HotkeysManager._paste(entry))
        entry.bind("<Control-x>", lambda e: HotkeysManager._cut(entry))

    @staticmethod
    def _copy(entry):
        entry.event_generate("<<Copy>>")
        return "break"

    @staticmethod
    def _paste(entry):
        entry.event_generate("<<Paste>>")
        return "break"

    @staticmethod
    def _cut(entry):
        entry.event_generate("<<Cut>>")
        return "break"
