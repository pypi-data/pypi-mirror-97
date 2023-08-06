"""This module contains repositories code."""

import abc
from collections import Iterable
from copy import deepcopy
from typing import Any, Dict, List, Union

from pymongo import ASCENDING, DESCENDING
from pymongo.errors import BulkWriteError

from .DomainEventListener import (
    ApplicationDomainEventPublisher,
    DomainEventListener,
)
from .DomainObject import DomainObject


class Repository(metaclass=abc.ABCMeta):
    """Repository is the base interface that all repo must implement."""

    @abc.abstractmethod
    def load(self, object_id: str) -> DomainObject:
        """Load a domain object based on its id.

        Args:
            object_id: the id of the object to be loaded

        Requires:
            object_id is not None and is a valid id

        Returns:
            The loaded domain object

        """
        raise NotImplementedError()

    @abc.abstractmethod
    def exists(self, object_id: str) -> bool:
        """Check if a domain object exist based on its id.

        Args:
            object_id: the identifier for this object

        Requires:
            object_id is not None and is a valid id

        Returns:
            True if the object exists. False otherwise

        """
        raise NotImplementedError()

    @abc.abstractmethod
    def save(self, obj: DomainObject) -> None:
        """Save a domain object.

        Args:
            obj: the received domain object

        Requires:
            obj is not None and is a valid DomainObject

        Effects:
            Modifications made of the domain object are saved

        """
        raise NotImplementedError()

    @abc.abstractmethod
    def remove(self, object_id: str):
        """Remove all events for a domain object identified by its id.

        Args:
            object_id: the id of the object to be removed

        Requires:
            object_id is not None and is a valid id
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_event_stream_for(self, object_id: str) -> List[Dict[str, Any]]:
        """Return the event stream for an object.

        Args:
            object_id: the identifier of this object

        Requires:
            object_id is not None and is a valid object id

        Returns:
            A sorted list of all the events for this domain object

        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_event_stream_since(self, event_id: str) -> List[Dict[str, Any]]:
        """Return all the events that occurs since a event.

        **The event with event_id==event_id is returned too**

        Args:
            event_id: the event id

        Requires:
            event_id is not None and represent an existing event

        Returns:
            A sorted list of all the event that occurs since the specified event
            The specified event is the firt of this list

        """
        raise NotImplementedError()

    @abc.abstractmethod
    def first_event_id(self) -> Union[str, None]:
        """Return the first known event id for sync.

        If there is no event yet, None is returned

        Returns:
            the firdt event id as a string. None if there is
            no events

        """
        raise NotImplementedError()

    @abc.abstractmethod
    def max_version_for_object(self, object_id: str) -> int:
        """Return the max known version for a domain object.

        Args:
            object_id: the object identifier

        Requires:
            object_id is not None and represent an existing domain object

        Returns:
            The last known version of this object

        """
        raise NotImplementedError()

    @abc.abstractmethod
    def create_blank_domain_object(self) -> DomainObject:
        """Create an empty domain event of the appropriate type.

        Returns:
            an empty domain event of the appropriate type

        """
        raise NotImplementedError()

    @staticmethod
    def merge_event_streams(prioritary_event_stream, other_event_stream):
        """Merge two event streams and manage possible conflit.

        Conflicts in event stream are event streams with repeating event number

        If there is a conflit, the first stream is considered prioritary.
        The conflict is then resolved by appending the additional elements of the second stream
        after these from the first. Events numbers are then correctly modified

        Requires:
            The two event streams are for the same object_id

        Returns:
            The merged event stream

        """
        diff1, diff2 = DomainObject.diff_event_streams(
            prioritary_event_stream, other_event_stream
        )

        if len(diff1) == 0 and len(diff2) == 0:
            return prioritary_event_stream
        elif len(diff1) == 0 and len(diff2) != 0:
            return other_event_stream
        elif len(diff1) != 0 and len(diff2) == 0:
            return prioritary_event_stream
        else:
            result_stream = deepcopy(prioritary_event_stream)
            actual_version = result_stream[-1]["version"] + 1
            for event in diff2:
                event["version"] = actual_version
                actual_version += 1
                result_stream.append(event)
            return result_stream


class EventPublisherRepository(Repository, metaclass=abc.ABCMeta):
    """Repository that publishes its saved events to domain event publisher."""

    def __init__(self, publisher: ApplicationDomainEventPublisher):  # noqa: D102
        self.listeners = list()
        self.register_listener(publisher)

    def save(self, obj: DomainObject) -> None:  # noqa: D102
        to_emit = self.append_to_stream(obj)

        assert to_emit is not None
        assert isinstance(to_emit, Iterable)

        for event in to_emit:
            for listener in self.listeners:
                assert isinstance(listener, DomainEventListener)
                listener.domainEventPublished(event)

    def register_listener(self, listener: DomainEventListener) -> None:
        """Register a new listener in this.

        Args:
            listener: the given listener

        Requires:
            listener must not be None and must implemnt DomainEventListener

        Effects:
            The listener is added in self

        """
        assert listener is not None
        assert isinstance(listener, DomainEventListener)

        if listener not in self.listeners:
            self.listeners.append(listener)

    @abc.abstractmethod
    def append_to_stream(self, obj: DomainObject) -> List[Dict[str, Any]]:
        """Save modification made on the domain object.

        Args:
            obj: the domain object to be saved

        Requires:
            obj is not None

        Returns:
            the newly persisted events

        """
        raise NotImplementedError()


class MongoEventSourceRepository(EventPublisherRepository, metaclass=abc.ABCMeta):
    """EventSource repository that persist event in mongodb."""

    def __init__(
        self,
        publisher: ApplicationDomainEventPublisher,
        client,
        database="fenrys",
        collection="event_store",
        memento_collection="domain_object_mementos",
        logger=None,
    ):
        super().__init__(publisher)
        self.__client = client
        self.__db = self.__client[database]
        self.__collection = self.__db[collection]
        self.__memento_collection = self.__db[memento_collection]
        self.__logger = logger
        self.__create_indexes()

    def append_to_stream(self, obj):  # noqa: D102
        assert obj is not None
        assert isinstance(obj, DomainObject)
        added_events = None

        while True:
            try:
                known_event_stream = self.get_event_stream_for(obj.object_id)
                known_event_ids = [event["event_id"] for event in known_event_stream]
                max_known_version = (
                    known_event_stream[-1]["version"]
                    if len(known_event_stream) > 0
                    else 0
                )

                events_to_add = []
                for event in reversed(obj.event_stream):
                    if event["event_id"] not in known_event_ids:
                        events_to_add.append(event)
                    else:
                        break
                events_to_add = list(reversed(events_to_add))

                if added_events is None:
                    added_events = deepcopy(events_to_add)

                if len(events_to_add) > 0:
                    event_version = max_known_version + 1
                    for event in events_to_add:
                        event["version"] = event_version
                        event_version += 1
                    self.__collection.insert_many(deepcopy(events_to_add))
                break
            except BulkWriteError:
                pass

        memento = self.__load_memento(obj.object_id)
        if self.__should_save_memento(memento, obj):
            self.__save_memento(obj)

        return added_events

    def max_version_for_object(self, object_id: str) -> int:
        return 0

    def load(self, object_id):  # noqa: D102
        if self.__have_memento(object_id):
            try:
                return self.load_with_memento(object_id)
            except Exception as e:
                self.__log_error(
                    f"Cannot load memento for {object_id}: {e}. "
                    "Removing memento and loading from stream."
                )
                self.__remove_memento(object_id)
        return self.load_without_memento(object_id)

    def load_without_memento(self, object_id):
        obj = self.create_blank_domain_object()
        assert isinstance(obj, DomainObject)

        stream = self.get_event_stream_for(object_id)
        obj.rehydrate(stream)

        return obj

    def load_with_memento(self, object_id):
        memento = self.__load_memento(object_id)
        obj = self.create_blank_domain_object()
        assert isinstance(obj, DomainObject)

        stream = self.get_event_stream_for(object_id)
        obj.rehydrate(stream, memento=memento)

        return obj

    def remove(self, object_id):  # noqa: D102
        self.__collection.delete_many({"object_id": object_id})

    def exists(self, object_id):  # noqa: D102
        return self.__collection.count_documents({"object_id": object_id}) > 0

    def get_event_stream_for(self, object_id):  # noqa: D102
        event_stream_cursor = self.__collection.find(
            {"object_id": object_id}, {"_id": False}
        )
        event_stream = list(event_stream_cursor)
        event_stream_cursor.close()
        return event_stream

    def get_event_stream_since(self, event_id, limit=None):  # noqa: D102
        assert limit is None or isinstance(limit, int)
        event = self.__collection.find_one({"event_id": event_id})

        if event is None:
            raise ValueError("This event id cannot be found")

        event_timestamp = event["event_timestamp"]
        events_cursor = self.__collection.find(
            {"event_timestamp": {"$gte": event_timestamp}}
        ).sort([("event_timestamp", 1)])
        if limit is not None:
            events_cursor = events_cursor.limit(limit)

        events = list(events_cursor)

        events_cursor.close()

        return events

    def first_event_id(self) -> Union[str, None]:  # noqa: D102
        events_cursor = (
            self.__collection.find({"version": 1})
            .sort([("event_timestamp", 1)])
            .limit(1)
        )
        events = list(events_cursor)
        events_cursor.close()

        if len(events) == 1:
            return events[0]["event_id"]
        else:
            return None

    def __load_memento(self, object_id):
        return self.__memento_collection.find_one({"object_id": object_id})

    @staticmethod
    def __should_save_memento(previous_memento, obj):
        if obj.version_number > 100 and previous_memento is None:
            return True

        if (
            previous_memento is not None
            and (obj.version_number - previous_memento["version_number"]) > 100
        ):
            return True

        return False

    def __save_memento(self, obj):
        try:
            memento_payload = obj.get_memento()
            if not obj.is_json_serializable(memento_payload):
                raise ValueError("Memento should be json serializable")

            memento = {
                "object_id": obj.object_id,
                "version_number": obj.version_number,
                "memento_payload": memento_payload,
            }
            self.__memento_collection.replace_one(
                {"object_id": obj.object_id}, memento, upsert=True
            )
        except NotImplementedError:
            pass
        except Exception as e:
            self.__log_error(f"Cannot save memento : {e}")

    def __remove_memento(self, object_id):
        self.__memento_collection.delete_one({"object_id": object_id})

    def __have_memento(self, object_id):
        return self.__memento_collection.count_documents({"object_id": object_id}) > 0

    def __create_indexes(self):
        self.__collection.create_index(
            [("event_id", ASCENDING)], name="eventid_unique", unique=True
        )
        self.__collection.create_index(
            [("object_id", ASCENDING), ("version", ASCENDING)],
            name="objectid_version_unique",
            unique=True,
        )
        self.__collection.create_index(
            [("event_timestamp", DESCENDING)], name="timestamp_ascending"
        )
        self.__memento_collection.create_index(
            [("object_id", ASCENDING)],
            name="memento_objectid_unique",
            unique=True,
        )

    def __log_error(self, message):
        if self.__logger is not None:
            self.__logger.error(message)


class InMemoryEventSourceRepository(EventPublisherRepository, metaclass=abc.ABCMeta):
    def __init__(self, publisher: ApplicationDomainEventPublisher):
        super().__init__(publisher)
        self.__repo = list()

    def append_to_stream(self, obj):
        assert obj is not None
        assert isinstance(obj, DomainObject)

        max_known_version = self.max_version_for_object(obj.object_id)
        merged_stream = self.merge_event_streams(
            self.get_event_stream_for(obj.object_id), obj.event_stream
        )
        merged_stream_version = merged_stream[-1]["version"]

        events_to_add = list()
        if merged_stream_version > max_known_version:
            for event in merged_stream:
                if event["version"] > max_known_version:
                    events_to_add.append(event)
                    self.__repo.append(event)

        return deepcopy(events_to_add)

    def load(self, object_id):
        obj = self.create_blank_domain_object()
        assert isinstance(obj, DomainObject)

        stream = self.get_event_stream_for(object_id)
        obj.rehydrate(stream)

        return obj

    def remove(self, object_id):
        stream = list()
        for event in self.__repo:
            if event["object_id"] != object_id:
                stream.append(event)
        self.__repo = stream

    def exists(self, object_id):
        return len(self.get_event_stream_for(object_id)) > 0

    def get_event_stream_for(self, object_id):
        stream = list()
        for event in self.__repo:
            if event["object_id"] == object_id:
                stream.append(event)
        return stream

    def get_event_stream_since(self, event_id):
        ignore = True
        for event in sorted(self.__repo, key=lambda x: x["event_timestamp"]):
            if event["event_id"] == event_id:
                ignore = False

            if not ignore:
                yield event

    def max_version_for_object(self, object_id):
        max_known_version = 0
        stream = self.get_event_stream_for(object_id)

        for event in stream:
            if event["version"] > max_known_version:
                max_known_version = event["version"]

        return max_known_version

    def first_event_id(self):
        if len(self.__repo) == 0:
            return None
        else:
            return self.__repo[0]["event_id"]
