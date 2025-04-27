from src.core.model.state_app import StateApp
from src.infrastructure.storage.state_storage import StateStorage


class StateManager:
    def __init__(self):
        # Хранение текущего состояния приложения
        self.state_storage = StateStorage()
        self.state: StateApp = self.state_storage.load_state()
        self.observers = []

    def add_observer(self, observer):
        """Добавить подписчика для обновлений"""
        self.observers.append(observer)

    def remove_observer(self, observer):
        """Удалить подписчика"""
        self.observers.remove(observer)

    def update_state(self, key, value):
        # todo
        """Обновить состояние по ключу и уведомить подписчиков"""
        if not hasattr(self.state, key):
            raise KeyError(f"Ключ '{key}' отсутствует в состоянии StateApp")

        setattr(self.state, key, value)

        self.state_storage.save_state(self.state)
        self.notify_observers()

    def notify_observers(self):
        """Уведомить всех подписчиков об изменении состояния"""
        for observer in self.observers:
            observer.update(self.state)  # Вызвать метод для обработки новых данных
