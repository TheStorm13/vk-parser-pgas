from tkinter import ttk

from src.core.manager.state_manager import StateManager
from src.gui.component.button_component import ButtonComponent
from src.gui.component.form_component import FormComponent
from src.gui.component.logo_component import LogoComponent
from src.gui.component.progress_bar_component import ProgressBarComponent
from src.gui.manager.ui_state_manager import UIStateManager


class MainFrame:
    def __init__(self, root, state_manager: StateManager, button_callbacks):
        self.state_manager = state_manager
        self.button_callbacks = button_callbacks

        # Initialize the main components of the UI
        self.root = root
        self.style = self.root.style

        self.main_frame = ttk.Frame(self.root, padding=5)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self._init_components()

        # Настройка колонок и строк для автоматического растяжения
        self.main_frame.columnconfigure(0, weight=1)
        for i in range(4):
            self.main_frame.rowconfigure(i, weight=0)

        # Manage UI controls' manager
        self.ui_state = UIStateManager(
            [
                self.form_component.entry_vk_token,
                self.form_component.entry_vk_group,
                self.form_component.entry_start_date,
                self.form_component.entry_end_date,
                self.form_component.entry_full_name,
                self.buttons_component.button_run_stop,
                self.buttons_component.description_button,
                self.buttons_component.remove_files,
            ]
        )

        # Set window geometry based on current layout
        self.root.update_idletasks()
        self.root.geometry("")  # Automatically resize the window to fit content


    def _init_components(self):
        # Initialize the form component and place it in the layout
        self.form_component = FormComponent(self.main_frame, self.state_manager)
        self.form_component.frame.grid(
            row=0, column=0, sticky="new", pady=5
        )

        # Initialize the progress bar component and place it below the form
        self.progress_component = ProgressBarComponent(
            self.main_frame, self.state_manager
        )
        self.progress_component.frame.grid(
            row=1, column=0, pady=5
        )

        # Initialize the button component, passing callback functions and logic
        self.buttons_component = ButtonComponent(
            self.main_frame,
            self.button_callbacks["run_program"],  # Callback for running the program
            self.button_callbacks["stop_program"],  # Callback for stopping the program
            self.button_callbacks["open_description_window"],  # Callback for opening a description window
            self.state_manager.state_storage.delete_state_storage,  # Callback for deleting state storage
        )

        # Initialize the logo component and place it in the bottom-right corner
        self.logo_component = LogoComponent(self.main_frame, "data/logo.png")
        self.logo_component.frame.grid(
            row=3, column=0, sticky="ne", pady=5
        )

    def reset_ui(self):
        # Reset the UI to its default state
        # Enable all UI elements and hide the progress bar
        self.ui_state.enable_all()
        self.progress_component.hide()  # Hide the progress bar
        self.buttons_component.set_run_state()  # Reset the button to the "Run" state
