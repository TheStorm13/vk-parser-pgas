class UIStateManager:
    def __init__(self, components):
        self.components = components

    def disable_all(self):
        for component in self.components:
            component.config(state="disabled")

    def enable_all(self):
        for component in self.components:
            component.config(state="normal")
