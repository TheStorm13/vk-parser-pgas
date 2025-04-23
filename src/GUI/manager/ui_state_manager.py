class UIStateManager:
    def __init__(self, components):
        self.components = components

    def disable_all(self, exclude=None):
        """
        Отключает все компоненты, кроме тех, которые находятся в списке exclude.
        :param exclude: Список компонентов, которые нужно исключить из отключения.
        """
        if exclude is None:
            exclude = []

        for component in self.components:
            if component not in exclude:  # Не отключать компоненты из exclude
                component.config(state="disabled")

    def enable_all(self):
        for component in self.components:
            component.config(state="normal")
