"""
Test module
"""

from model import create_person, ClonePerson
from clone_ndb_entity import clone_entity_properties, construct_clone_keys_from_entity_key


import unittest

from google.appengine.ext import testbed
from google.appengine.datastore import datastore_stub_util

class BaseTestCase(unittest.TestCase):

    def setUp(self, probability=0):
        super(BaseTestCase, self).setUp()
        self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(probability=probability)
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub(consistency_policy=self.policy)
        self.testbed.init_memcache_stub()

class TestCreatePerson(BaseTestCase):

    def setUp(self, probability=1):
        super(TestCreatePerson, self).setUp(probability)

    def test_create_person_a_person_was_created(self):
        person = create_person("John", "Smith")
        self.assertEqual(person.first_name, "John")
        self.assertEqual(person.last_name, "Smith")
        self.assertEqual(person.full_name, "John Smith")


class TestConstructCloneKeys(BaseTestCase):
    """
    Test for constructing cloned entity key for an existing entity
    """
    def setUp(self, probability=1):
        super(TestConstructCloneKeys, self).setUp(probability)
        self.person = create_person("John", "Smith")
        self.cloned_person_key = construct_clone_keys_from_entity_key(self.person.key, ClonePerson)

    def test_construct_clone_key_pairs_length_is_same_as_entity_key_length(self):
        self.assertEqual(len(self.cloned_person_key.pairs()), len(self.person.key.pairs()))

    def test_construct_clone_key_kind_is_cloned_kind(self):
        for kind, _ in self.cloned_person_key.pairs():
            self.assertEqual(kind, 'ClonePerson')

    def test_construct_clone_key_id_is_same_as_entity_key_id(self):
        i = 0
        while i < len(self.person.key.pairs()):
            _, cloned_person_key_id = self.cloned_person_key.pairs()[i]
            _, person_key_id = self.person.key.pairs()[i]
            self.assertEqual(cloned_person_key_id, person_key_id)
            i += 1


class TestClonePerson(BaseTestCase):
    """
    Tests for cloning a Person Entity
    """

    def setUp(self, probability=1):
        super(TestClonePerson, self).setUp(probability)
        self.person = create_person("John", "Smith")

    def test_cloning_person_entity_to_clone_person_entity(self):

        cloned_person = clone_entity_properties(self.person, ClonePerson)

        self.assertEqual(cloned_person.first_name, self.person.first_name)
        self.assertEqual(cloned_person.last_name, self.person.last_name)
        self.assertEqual(cloned_person.full_name, self.person.full_name)

    def test_cloning_person_entity_to_clone_person_entity_with_value_override(self):
        override_params = {'first_name': "James"}
        self.assertNotEqual(self.person.first_name, override_params['first_name'])

        cloned_person = clone_entity_properties(self.person, ClonePerson, **override_params)

        #overridden values
        self.assertEqual(cloned_person.first_name, override_params['first_name'])

        #cloned values
        self.assertEqual(cloned_person.last_name, self.person.last_name)
        self.assertEqual(cloned_person.full_name, "James Smith")

    def test_cloning_person_entity_to_clone_person_entity_with_cloned_key(self):
        cloned_person = clone_entity_properties(self.person, ClonePerson, clone_key=True)
        self.assertEqual(len(cloned_person.key.pairs()), len(self.person.key.pairs()))
        i = 0
        while i < len(cloned_person.key.pairs()):
            cloned_person_key_kind, cloned_person_key_id = cloned_person.key.pairs()[i]
            _, person_key_id = self.person.key.pairs()[i]
            self.assertEqual(cloned_person_key_kind, 'ClonePerson')
            self.assertEqual(cloned_person_key_id, person_key_id)
            i += 1

    def test_cloned_person_entity_has_date_cloned_after_put_in_datastore(self):
        cloned_person = clone_entity_properties(self.person, ClonePerson, clone_key=True)
        cloned_person.put()
        cloned_person = cloned_person.key.get()
        self.assertTrue(cloned_person.date_cloned)


if __name__ == '__main__':
    unittest.main()