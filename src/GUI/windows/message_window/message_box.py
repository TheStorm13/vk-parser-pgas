import tkinter as tk
from tkinter import ttk


class CustomMessageBox(tk.Toplevel):
    def __init__(self, parent, title, message, button_text="OK"):
        super().__init__(parent)  # Initialize the Toplevel window
        self.title(title)  # Set window title
        self.configure(bg="white")
        self.resizable(False, False)  # Disable resizing

        # Configure custom styles for labels and buttons
        self.style = ttk.Style()
        self.style.configure("Custom.TLabel", background="white", font=("Helvetica", 12))
        self.style.configure("Custom.TButton", font=("Helvetica", 12, "bold"), background="white")

        # Create the message label with wrapping for long texts
        self.label_message = ttk.Label(self, text=message, style="Custom.TLabel", wraplength=350)
        self.label_message.pack(pady=20, padx=20)

        # Create the OK button that closes the message box
        self.button_ok = ttk.Button(self, text=button_text, style="Custom.TButton", command=self.destroy)
        self.button_ok.pack(pady=10)

        self.update_idletasks()  # Ensure all widgets are rendered before adjusting window size
        self.adjust_window_height()  # Adjust height dynamically based on text content

    def adjust_window_height(self):
        """
        Dynamically adjust the window height based on the text content.
        """
        text_height = self.label_message.winfo_reqheight()  # Measure required height for the message
        window_height = text_height + 100  # Add a margin for padding
        self.geometry(f"400x{window_height}")  # Set window size
