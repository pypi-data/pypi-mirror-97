import os
import json
import uuid
import threading

from ..errors.entity_not_found import EntityNotFound
from ..errors.more_than_one_result import MoreThanOneResult

class JsonContext(object):
    def __init__(
            self,
            entity_class,
            filepath="./",
            key_field="id",
            key_generate_func=lambda: str(uuid.uuid4())):
        """

        Args:
            entity_class (class): Class that will be the json elements template
            filepath (str, optional): collection file path. Defaults to "./".
            key_field (str, optional): keyfield name. Defaults to "id".
            key_generate_func ([type], optional): Collection key generation func. Defaults to lambda:str(uuid.uuid4()).
        """
        self.entity_class = entity_class
        entity_name = entity_class.__name__.lower()
        self.file_path = os.path.join(filepath, "{0}s.json".format(entity_name))
        self.entity_name = entity_name
        self.session_values = []
        if not os.path.exists(self.file_path):
            self.commit()
        self.key_field = key_field
        self.key_generate_func = key_generate_func
        self.lock = threading.Lock()

    def __map(self, data):
        entity = self.entity_class()
        for attr, value in data.items():
            setattr(entity, attr, value)
        return entity

    def open(self):
        """Open and load values on session (locks context)
        """
        self.lock.acquire()
        with open(self.file_path) as fh:
            data = json.load(fh)
            self.session_values = list(map(self.__map, data["values"]))

    def close(self):
        """Unlock context
        """
        self.lock.release()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def exists(self, identifier):
        """Check if exists a document with the identifier provided

        Args:
            identifier (any type): identifier value

        Returns:
            bool: True if  document exists False if not
        """
        matches = list(
            filter(
                lambda x: getattr(x, self.key_field) == identifier,
                self.session_values))
        return len(matches) > 0

    def add(self, entity):
        """Inserts a document in the collection

        Args:
            entity (Collection´s entity): document

        Returns:
            Collection´s entity: Entity with updated fields
        """
        identifier = getattr(entity, self.key_field)
        if (identifier is not None and self.exists(identifier)):
            self.delete(entity)
        else:
            setattr(entity, self.key_field, self.key_generate_func())
        self.session_values.append(entity)
        return entity

    def delete(self, entity):
        """Remove from the collection the provided entity

        Args:
            entity (Collection´s entity): Entity that will be deleted
        """
        self.session_values = list(
            filter(
                lambda x: getattr(x, self.key_field) != getattr(entity, self.key_field),
            self.session_values))

    def commit(self):
        """Writes on disk session collection
        """
        with open(self.file_path, 'w+') as fh:
            fh.write(
                json.dumps(
                    {
                        "name": self.entity_name,
                        "values": list(map(lambda x: x.__dict__, self.session_values))
                    }))

    def find(self, query_function=None):
        """Finds a document that maches the query provied

        Args:
            query_function (function entity -> bool, optional): Function that will be applied to the collection. Defaults to None.

        Returns:
            list[Collection´s entity]: Collection filtered
        """
        if query_function is None:
            return self.session_values
        return list(
            filter(
                query_function,
                self.session_values))

    def first(self, query_function):
        """Returns the first element that matches the specified function

        Args:
            query_function (function entity->bool): Funtion that will be applied to the collection.

        Returns:
            Collection´s entity: First element that matches query provided
        """
        values = self.find(query_function=query_function)
        return  None if len(values) == 0 else values[0]

    def single( self, query_function):
        """Returns the single element that matches the specified function if there are more than 1 raises exception

        Args:
            query_function (function entity->bool): Funtion that will be applied to the collection.
        
        Raises:
            EntityNotFound: If there is not an element that matches the query provided raises error
            MoreThanOneResult: I there is more than one eelemtn that matches the query raises error

        Returns:
            Collection´s entity: Element that matches the query provied
        """
        values = self.find(query_function=query_function)

        if len(values) is 0:
            raise EntityNotFound()

        if len(values) is not 1:
            raise MoreThanOneResult()

        return values[0]

    def get(self, identifier):
        """

        Args:
            identifier (Collection´s entity key): collections key field

        Raises:
            EntityNotFound: If there is not an element that matches the identifier provided raises error

        Returns:
            Collection´s entity: Element that has a key matching the identifier provided
        """
        if not self.exists(identifier):
            raise EntityNotFound("identifier not found")
        return self.find(lambda x: getattr(x, self.key_field) == identifier)[0]

    def get_all(self):
        """Returns all elements

        Returns:
            list[Collection´s entity]: all session elements
        """
        return self.session_values
