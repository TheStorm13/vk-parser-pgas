class UIStateManager:
    """Управляет состоянием UI-компонентов."""

    def __init__(self, components):
        """Сохраняет компоненты для управления.

        Args:
            components: Список UI-компонентов.

        Returns:
            None

        """
        self.components = components

    def disable_all(self, exclude=None):
        """Отключает все компоненты, кроме исключений.

        Args:
            exclude: Компоненты для исключения.

        Returns:
            None

        """
        if exclude is None:
            exclude = []

        for component in self.components:
            if component not in exclude:
                component.config(state="disabled")

    def enable_all(self):
        """Включает все компоненты.

        Returns:
            None

        """
        for component in self.components:
            component.config(state="normal")
