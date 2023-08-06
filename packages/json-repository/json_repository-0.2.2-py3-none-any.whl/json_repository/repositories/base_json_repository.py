from ..context.json_context import JsonContext


class BaseJsonRepository(object):
    def __init__(self, entity_name, filepath="./"):
        self.context = JsonContext(entity_name, filepath=filepath)

    def __enter__(self):
        """Open context
        """        
        self.context.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Unlock context
        """
        self.context.close()

    def insert(self, entity):
        """Inserts a document in the collection

        Args:
            entity (Collection´s entity): document

        Returns:
            Collection´s entity: Entity with updated fields
        """
        return self.context.add(entity)

    def update(self, entity):
        """updates a document in the collection

        Args:
            entity (Collection´s entity): document

        Returns:
            Collection´s entity: Entity with updated fields
        """
        return self.context.add(entity)

    def delete(self, entity):
        """Remove from the collection the provided entity

        Args:
            entity (Collection´s entity): Entity that will be deleted
        """
        self.context.delete(entity)

    def get_all(self):
        """Returns all elements

        Returns:
            list[Collection´s entity]: all session elements
        """
        return self.context.get_all()

    def get(self, identifier):
        """

        Args:
            identifier (Collection´s entity key): collections key field

        Raises:
            EntityNotFound: If there is not an element that matches the identifier provided raises error

        Returns:
            Collection´s entity: Element that has a key matching the identifier provided
        """
        return self.context.get(identifier)

    def find(self, function):
        """Finds a document that maches the query provied

        Args:
            query_function (function entity -> bool, optional): Function that will be applied to the collection. Defaults to None.

        Returns:
            list[Collection´s entity]: Collection filtered
        """
        return self.context.find(function)

    def first(self, function=None):
        """Returns the first element that matches the specified function

        Args:
            query_function (function entity->bool): Funtion that will be applied to the collection.

        Returns:
            Collection´s entity: First element that matches query provided
        """
        return self.context.first(function)

    def single(self, function=None):
        """Returns the single element that matches the specified function if there are more than 1 raises exception

        Args:
            query_function (function entity->bool): Funtion that will be applied to the collection.
        
        Raises:
            EntityNotFound: If there is not an element that matches the query provided raises error
            MoreThanOneResult: I there is more than one eelemtn that matches the query raises error

        Returns:
            Collection´s entity: Element that matches the query provied
        """
        return self.context.single(function)
    
    def exists(self, identifier):
        """Check if exists a document with the identifier provided

        Args:
            identifier (any type): identifier value

        Returns:
            bool: True if  document exists False if not
        """
        return self.context.exists(identifier)
