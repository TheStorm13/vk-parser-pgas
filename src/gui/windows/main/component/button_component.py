from tkinter import ttk


class ButtonComponent:
    def __init__(self, root, on_run, on_stop, on_description, on_remove_files):
        self.root = root
        self.on_run = on_run
        self.on_stop = on_stop
        self.on_description = on_description
        self.on_remove_files = on_remove_files

        # Create a frame to hold the buttons
        self.frame = ttk.Frame(self.root, padding=5)

        # Initialize the components (buttons)
        self._init_components()

    def _init_components(self):
        """
        Create and configure the buttons for the component.
        """
        # Create the "Run/Stop" toggle button
        self.button_run_stop = ttk.Button(
            self.frame,
            text="Запустить",  # Default button label is "Run"
            command=self.toggle_run_stop,  # Toggle between "Run" and "Stop"
            style="Accent.TButton",
            takefocus=False,
        )
        self.button_run_stop.grid(
            row=0, column=0, sticky="nsew", pady=5  # Add padding for the layout
        )

        # Create the "Description" button
        self.description_button = ttk.Button(
            self.frame,
            text="Описание",  # "Description" button label
            command=self.on_description,  # Call the description callback when pressed
            style="Accent.TButton",
        )
        self.description_button.grid(row=1, column=0, sticky="nsew", pady=5)

        # Create the "Remove Temporary Files" button
        self.remove_files = ttk.Button(
            self.frame,
            text="Удалить временные файлы",  # "Remove Files" button label
            command=self.on_remove_files,  # Call the remove files callback when pressed
            style="Accent.TButton",
        )
        self.remove_files.grid(
            row=2, column=0, sticky="nsew", pady=5  # Align below "Description" button
        )

    def toggle_run_stop(self):
        """
        Toggle the state of the "Run/Stop" button.

        - Switch between "Run" and "Stop" labels.
        - Trigger the corresponding callback for each state.
        """
        if self.button_run_stop["text"] == "Запустить":  # Current state is "Run"
            self.button_run_stop.config(
                text="Остановить",  # Change to "Stop"
                style="Accent.TButton",
            )
            self.on_run()  # Call the "on_run" callback
        else:
            self.button_run_stop.config(
                text="Запустить",  # Change back to "Run"
                style="Accent.TButton",
            )
            self.on_stop()  # Call the "on_stop" callback

    def set_run_state(self):
        """
        Reset the "Run/Stop" button to "Run" state.

        This method can be used to explicitly set the button text to "Run".
        """
        self.button_run_stop.config(
            text="Запустить",  # Reset text to "Run"
            style="Accent.TButton",
        )
