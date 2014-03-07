"""
clone an ndb entity
"""

from google.appengine.ext import ndb


def construct_clone_keys_from_entity_key(entity_key, clone_kind):
    """
    :param entity_key: the entity key (ndb.Key)
    :param clone_kind: the kind of the clone model
    :return: the key for the entity clone model
    """
    keys = [(clone_kind, key_id) for _, key_id in entity_key.pairs()]
    return ndb.Key(pairs=keys)

def clone_entity_properties(entity_to_clone, to_class, clone_key=False, **extra_args):
    """Clones the properties of an entity into another entity, adding or overriding constructor attributes.

    The cloned entity will have exactly the same property values as the original
    entity, except where overridden. By default it will have no parent entity or key name, unless supplied.

    Args:
    :param entity_to_clone: The entity to clone
    :param to_class: the new Entity type
    :param clone_key: whether to clone the entity key or not
    :param extra_args: Keyword arguments to override from the cloned entity and pass
      to the constructor.
    :returns:
        A cloned, possibly modified, copy of entity e that has the same properties as e
    """
    entity_dict = entity_to_clone.to_dict()
    new_props = {}
    for k, v in entity_to_clone.__class__.__dict__.iteritems():
        if isinstance(v, ndb.Property) and not isinstance(v, ndb.ComputedProperty):  # can't clone ComputedProperty
            new_props[k] = entity_dict[k]
    new_props.update(extra_args)
    new_entity = to_class(**new_props)
    if clone_key:
        key = construct_clone_keys_from_entity_key(entity_to_clone.key, to_class)
        new_entity.key = key
    return new_entity



