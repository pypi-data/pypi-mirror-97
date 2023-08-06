"""This module contains DomainEvent listening and publishing logic."""

import abc
from queue import Empty
import time
from threading import Thread
from multiprocessing import Queue
from typing import Dict, Any


class DomainEventListener(metaclass=abc.ABCMeta):
    """DomainEventListener is the interface for domain event listening."""

    @abc.abstractmethod
    def domainEventPublished(self, event: Dict[str, Any]) -> None:
        """React to domain event.

        Args:
            event: the event that have been published

        Requires:
            event is not None
        """
        raise NotImplementedError()


class ApplicationDomainEventPublisher(Thread, DomainEventListener):
    """Event publisher for an application.

    Listener must be registered with `register_listener` method.
    They can be unregistered with `unregister_listener`.
    All listeners must implement DomainEventListener interface

    """

    def __init__(self, is_async=False):
        Thread.__init__(self)

        self.__is_async = is_async
        self.daemon = True
        self.queue = Queue()
        self.__listeners = list()

        if self.__is_async:
            self.start()

    def run(self):  # noqa: D102
        assert self.__is_async
        while True:
            try:
                event = self.queue.get(timeout=5)
                self.__manage_event(event)
            except Empty:
                pass

    def domainEventPublished(self, event):
        if self.__is_async:
            self.queue.put(event)
        else:
            self.__manage_event(event)

    def wait(self):
        assert self.__is_async

        while not self.queue.empty():
            time.sleep(0.1)
        time.sleep(0.5)

    def __manage_event(self, event):
        for listener in self.__listeners:
            assert isinstance(listener, DomainEventListener)
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
