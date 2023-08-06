"""This module contains DomainEvent listening and publishing logic."""

import abc
from queue import Empty
from threading import Thread
from queue import Queue
from typing import Dict, Any


class DomainEventListener(Thread, metaclass=abc.ABCMeta):
    """DomainEventListener is the interface for domain event listening."""

    is_async = False

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.__queue = Queue()

        if self.is_async:
            self.start()

    def run(self):
        while True:
            try:
                event = self.__queue.get(block=True, timeout=1)
                self.domainEventPublished(event)
            except Empty:
                pass
            except Exception as e:
                if self.is_async:
                    print(f"Exception occured in {self.__class__} : {e}")
                else:
                    raise e

    def onEvent(self, event):
        self.__queue.put(event)

    @abc.abstractmethod
    def domainEventPublished(self, event: Dict[str, Any]) -> None:
        """React to domain event.

        Args:
            event: the event that have been published

        Requires:
            event is not None
        """
        raise NotImplementedError()


class ApplicationDomainEventPublisher(DomainEventListener):
    """Event publisher for an application.

    Listener must be registered with `register_listener` method.
    They can be unregistered with `unregister_listener`.
    All listeners must implement DomainEventListener interface

    """

    def __init__(self):
        self.__listeners = list()

    def domainEventPublished(self, event):
        for listener in self.__listeners:
            assert isinstance(listener, DomainEventListener)
            if listener.is_async:
                listener.onEvent(event)
            else:
                listener.domainEventPublished(event)

    def register_listener(self, obj):
        assert obj is not None
        assert isinstance(obj, DomainEventListener)

        self.__listeners.append(obj)

    def unregister_listener(self, listener):
        assert listener is not None
        assert isinstance(listener, DomainEventListener)

        self.__listeners.remove(listener)

    def contains_listener(self, listener):
        assert listener is not None
        assert isinstance(listener, DomainEventListener)

        return listener in self.__listeners
