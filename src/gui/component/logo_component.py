from tkinter import ttk

from PIL import Image, ImageTk


class LogoComponent:
    def __init__(self, parent, logo_path, width=100, height=80):
        self.parent = parent
        self.logo_path = logo_path
        self.width = width
        self.height = height
        self.logo_image = None  # Store the processed logo image

        self.frame = ttk.Frame(self.parent, padding=5)

        self._create_logo()

    def _create_logo(self):
        """
        Loads, resizes, and displays the logo on the parent widget.
        """
        # Open the image file
        image = Image.open(self.logo_path)

        # Resize the image to specified dimensions using high-quality resampling
        image = image.resize((self.width, self.height), Image.Resampling.LANCZOS)

        # Convert the image for Tkinter compatibility
        self.logo_image = ImageTk.PhotoImage(image)

        # Create the label and add the image to it
        logo_label = ttk.Label(self.frame, image=self.logo_image)

        # Position the label at the bottom-right corner with padding
        logo_label.grid(row=0, column=0, padx=10, pady=10)

        # Disable resizing of the row and column containing the logo
