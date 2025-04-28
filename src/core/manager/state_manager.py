from src.core.model.state_app import StateApp
from src.infrastructure.logger.logger import setup_logger
from src.infrastructure.storage.state_storage import StateStorage

logger = setup_logger(__name__)


class StateManager:
    def __init__(self):
        # Initialize the storage for application state
        self.state_storage = StateStorage()

        # Load the initial application state from storage
        self.state: StateApp = self.state_storage.load_state()

        # List of observers to notify about state changes
        self.observers = []

        # Add the storage itself as an observer to handle automatic updates
        self.add_observer(self.state_storage)

    def add_observer(self, observer):
        """
        Add an observer to the list of observers.
        Observers will be notified when the state is updated.
        """

        self.observers.append(observer)

    def remove_observer(self, observer):
        """
        Remove an observer from the list of observers.
        """

        self.observers.remove(observer)

    def update_state(self, key, value):
        """
        Update the application state for a given key and notify all observers.

        Args:
            key (str): The attribute of StateApp to be updated.
            value: The new value to set for the key.

        Raises:
            KeyError: If the key does not exist in the StateApp class.
        """

        if not hasattr(self.state, key):
            logger.error(f"Key '{key}' is absent in the state of state")
            raise KeyError(f"Ключ '{key}' отсутствует в состоянии StateApp")

        # Update the state attribute with the new value
        setattr(self.state, key, value)

        # Save the updated state to persistent storage
        self.state_storage.save_state(self.state)

        # Notify all observers about the state change
        self.notify_observers()

    def notify_observers(self):
        """
       Notify all registered observers about the state update.
       Each observer's `update` method will be called with the current state.
       """

        for observer in self.observers:
            observer.update(self.state)  # Call the observer's update method with the new state
