from src.core.model.state_app import StateApp
from src.infrastructure.logger.logger import setup_logger
from src.infrastructure.storage.state_storage import StateStorage

logger = setup_logger(__name__)


class StateManager:
    """Управляет состоянием приложения и наблюдателями.

    Attributes:
        state (StateApp): Текущее состояние.

    """

    def __init__(self):
        """Инициализирует состояние и регистрирует хранилище как наблюдателя."""
        self.state_storage = StateStorage()
        self.state: StateApp = self.state_storage.load_state()
        self.observers = []
        # Хранилище подписывается как наблюдатель для автосохранения
        self.add_observer(self.state_storage)

    def add_observer(self, observer):
        """Добавляет наблюдателя.

        Args:
            observer: Объект с методом update(state).

        """
        self.observers.append(observer)

    def remove_observer(self, observer):
        """Удаляет наблюдателя.

        Args:
            observer: Объект ранее добавленный.

        """
        self.observers.remove(observer)

    def update_state(self, key, value):
        """Обновляет состояние по ключу и уведомляет наблюдателей.

        Args:
            key (str): Имя атрибута StateApp.
            value: Новое значение атрибута.

        Raises:
            KeyError: Ключ отсутствует в StateApp.

        """
        if not hasattr(self.state, key):
            logger.error(f"Key '{key}' is absent in the state of state")
            raise KeyError(f"Ключ '{key}' отсутствует в состоянии StateApp")

        setattr(self.state, key, value)
        self.state_storage.save_state(self.state)
        self.notify_observers()

    def notify_observers(self):
        """Уведомляет всех наблюдателей об обновлении состояния."""
        for observer in self.observers:
            # Каждый наблюдатель получает актуальное состояние
            observer.update(self.state)
