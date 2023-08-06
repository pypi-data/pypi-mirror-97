import unittest
import os
from json_repository.repositories.base_json_repository\
    import BaseJsonRepository
from json_repository.errors.entity_not_found import EntityNotFound
from json_repository.errors.more_than_one_result import MoreThanOneResult

class Foo(object):
    foo = None
    bar = None
    id = None

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        return self.id == other.id and self.bar == other.bar and self.foo == other.foo

class FoobarRepository(BaseJsonRepository):
    def __init__(self):
        super(FoobarRepository, self).__init__(Foo)


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        """
            ensure db is empty at the end.
        """
        with FoobarRepository() as repo:
            for entity in repo.get_all():
                repo.delete(entity)
            repo.context.commit()

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        os.remove("foos.json")

    def get_foo(self):
        entity = Foo()
        entity.foo = "a foo value"
        entity.bar = "a bar value"
        return entity

    def test_insert(self):
        value = None
        with FoobarRepository() as repo:
            value = repo.insert(self.get_foo())
            repo.context.commit()
        val2 = None
        with FoobarRepository() as repo:
            val2 = repo.get(value.id)

        self.assertEqual(value, val2)

    def test_update(self):
        value = None
        with FoobarRepository() as repo:
            value = repo.insert(self.get_foo())
            repo.context.commit()
        value.foo = " a new foo value"

        with FoobarRepository() as repo:
            repo.update(value)
            repo.context.commit()

        with FoobarRepository() as repo:
            val2 = repo.get(value.id)

        self.assertEqual(value.foo, val2.foo)

    def test_delete(self):
        value = None
        with FoobarRepository() as repo:
            value = repo.insert(self.get_foo())
            repo.context.commit()
        with FoobarRepository() as repo:
            repo.delete(value)
            repo.context.commit()

        with self.assertRaises(EntityNotFound):
            with FoobarRepository() as repo:
                repo.get(value.id)

    def test_get_all(self):
        value = None
        value2 = None
        with FoobarRepository() as repo:
            value = repo.insert(self.get_foo())
            value2 = repo.insert(self.get_foo())
            repo.context.commit()
        values = [value, value2]
        with FoobarRepository() as repo:
            for value in repo.get_all():
                self.assertIn(value, values)

    def test_get(self):
        value = None
        with FoobarRepository() as repo:
            value = repo.insert(self.get_foo())
            repo.context.commit()
        with FoobarRepository() as repo:
            self.assertEqual(value, repo.get(value.id))

    def test_find(self):
        value = None
        with FoobarRepository() as repo:
            value = repo.insert(self.get_foo())
            repo.context.commit()
        with FoobarRepository() as repo:
            self.assertEqual(
                value,
                repo.find(lambda x: x.foo == value.foo)[0])


    def test_single(self):
        with FoobarRepository() as repo:
            value = repo.insert(self.get_foo())
            repo.context.commit()

        with FoobarRepository() as repo:
            self.assertEqual(
                value,
                repo.single(lambda x: x.foo == value.foo))

    def test_single_not_found(self):
        with FoobarRepository() as repo:
            value = repo.insert(self.get_foo())
            repo.context.commit()
        with self.assertRaises(EntityNotFound):
            with FoobarRepository() as repo:
                self.assertEqual(
                    value,
                    repo.single(lambda x: x.foo == "myvaluenotexists"))

    def test_single_morethanoneresult(self):
        with FoobarRepository() as repo:
            value = repo.insert(self.get_foo())
            value = repo.insert(self.get_foo())
            repo.context.commit()
        with self.assertRaises(MoreThanOneResult):
            with FoobarRepository() as repo:
                self.assertEqual(
                    value,
                    repo.single(lambda x: x.foo == value.foo))

    def test_first_not_exists(self):
        with FoobarRepository() as repo:
            self.assertEqual(
                None,
                repo.first(lambda x: x.foo == "randomvalue"))

    def test_first_with_fun(self):
        with FoobarRepository() as repo:
            value = repo.insert(self.get_foo())
            va = self.get_foo()
            va.bar = "22"
            repo.insert(va)
            repo.context.commit()

        with FoobarRepository() as repo:
            self.assertEqual(
                value,
                repo.first(lambda x: x.foo == value.foo))

    def test_first(self):
        with FoobarRepository() as repo:
            value = repo.insert(self.get_foo())
            va = self.get_foo()
            va.bar = "22"
            repo.insert(va)
            repo.context.commit()

        with FoobarRepository() as repo:
            self.assertEqual(
                value,
                repo.first())

    def test_exists(self):
        with FoobarRepository() as repo:
            value = repo.insert(self.get_foo())
            va = self.get_foo()
            va.bar = "22"
            repo.insert(va)
            repo.context.commit()

        with FoobarRepository() as repo:
            self.assertTrue(
                repo.exists(va.id))
            self.assertFalse(
                repo.exists(234))
