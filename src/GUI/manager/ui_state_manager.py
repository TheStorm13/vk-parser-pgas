class UIStateManager:
    def __init__(self, components):
        self.components = components

    def disable_all(self, exclude=None):
        # Disables all components except those in the 'exclude' list
        if exclude is None:
            exclude = []

        for component in self.components:
            # Do not turn off the components from exclude
            if component not in exclude:
                component.config(state="disabled")

    def enable_all(self):
        # Enables all components
        for component in self.components:
            component.config(state="normal")
