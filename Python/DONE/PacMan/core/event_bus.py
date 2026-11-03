"""Event Bus module implementing the Observer Pattern."""

from typing import Callable, Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class EventBus:
    """A centralized event bus for decoupled component communication.

    Implements the Observer Design Pattern. Publishers can emit events
    (like 'DOT_EATEN') without needing to know which systems (like ScoreManager
    or AudioSystem) are listening.

    Attributes:
        _subscribers (Dict[str, List[Callable[[Any], None]]]): A dictionary
            mapping event strings to a list of callback functions.
    """

    def __init__(self) -> None:
        """Initialize the EventBus with an empty subscriber dictionary."""
        self._subscribers: Dict[str, List[Callable[[Any], None]]] = {}

    def subscribe(
        self, event_type: str, callback: Callable[[Any], None]
    ) -> None:
        """Subscribe a callback function to a specific event type.

        Args:
            event_type (str): The string identifier of the event
                (e.g., 'DOT_EATEN').
            callback (Callable[[Any], None]): The function to execute
                when the event fires.
        """
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []

        if callback not in self._subscribers[event_type]:
            self._subscribers[event_type].append(callback)
            logger.debug("New subscriber for event: %s", event_type)

    def unsubscribe(
        self, event_type: str, callback: Callable[[Any], None]
    ) -> None:
        """Unsubscribe a callback function from a specific event type.

        Args:
            event_type (str): The string identifier of the event.
            callback (Callable[[Any], None]): The callback function to remove.
        """
        if event_type in self._subscribers:
            try:
                self._subscribers[event_type].remove(callback)
            except ValueError:
                pass

    def clear(self, event_type: Optional[str] = None) -> None:
        """Clear subscribers for a specific event or all events.

        Args:
            event_type (Optional[str]): The event type to clear, or None
                to clear all subscribers. Defaults to None.
        """
        if event_type is None:
            self._subscribers.clear()
        elif event_type in self._subscribers:
            self._subscribers[event_type].clear()

    def publish(self, event_type: str, data: Any = None) -> None:
        """Publish an event, triggering all subscribed callbacks safely.

        Args:
            event_type (str): The string identifier of the event to broadcast.
            data (Any, optional): Optional payload data to pass to the
                callbacks. Defaults to None.
        """
        if event_type in self._subscribers:
            for callback in list(self._subscribers[event_type]):
                try:
                    callback(data)
                except Exception as e:
                    # Strict zero-crash policy: isolate failing subscribers
                    logger.error(
                        "Error in subscriber for %s: %s", event_type, e
                    )
