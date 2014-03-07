"""
Models
"""

from google.appengine.ext import ndb


class Person(ndb.Model):
    """
    Represents a person
    """
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    full_name = ndb.ComputedProperty(lambda self: "%s %s" % (self.first_name, self.last_name))


class ClonePerson(ndb.Model):
    """ A Person entity that has been cloned
    """
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    full_name = ndb.ComputedProperty(lambda self: "%s %s" % (self.first_name, self.last_name))
    date_cloned = ndb.DateTimeProperty(auto_now_add=True)


def create_person(first_name, last_name, **kwargs):
    """
    :param first_name: the first name of the person
    :param last_name: the last name of the person
    :param kwargs: additional person properties
    :return: the person that was created
    """
    person = Person(first_name=first_name, last_name=last_name, **kwargs)
    person.put()
    return person