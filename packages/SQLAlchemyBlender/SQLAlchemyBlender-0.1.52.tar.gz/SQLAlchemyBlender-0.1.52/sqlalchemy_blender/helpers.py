from typing import Optional
from typing import Union
from datetime import datetime
from datetime import date

from collections.abc import Iterable
from sqlalchemy.orm.collections import InstrumentedList

from .database import db

CIRCREF_CHECK = set()


class Config:
    collection = False


def get_primary_key_value(elem: db.Model):
    pk = primarykey(elem)
    return getattr(elem, pk, None)


def extract_special_members(data, *args, **kwargs):
    resp = {}
    # first extract any special properties or hybrid properties
    for prop in getattr(data, '__properties__', set()):
        if not getattr(prop, '__name__', None):
            resp[prop.__name__] = prop.fget(data)
        property = serializer(getattr(data, prop.__name__), *args, **kwargs)
        resp[prop.__name__] = property

    # then get the counts we have defined as special len(relation)
    if getattr(data, '__counts__', None):
        resp['__counts__'] = getattr(data, '__counts__')

    # if a Model has some relationships that should be exposed by default, extract them here
    if getattr(data, '__expose__', None):
        for entity in getattr(data, '__expose__'):
            if entity.key in kwargs.get('exclusions', set()):
                continue
            if entity.uselist:
                resp[entity.key] = []
                for child in getattr(data, entity.key):
                    resp[entity.key].append(serializer(child, *args, **kwargs))
            else:
                resp[entity.key] = serializer(getattr(data, entity.key, None), *args, **kwargs)
    return resp


def extract_relationships(data, **kwargs):
    if kwargs.get('rels', None) is None:
        return set()
    rels = kwargs.get('rels', set())
    if '*' in rels:
        rels = relationships(data, fmt=True)
    resp: dict = {}
    for rel in set(relationships(data, fmt=True)).intersection(rels):
        resp[rel] = serializer(getattr(data, rel, None), **kwargs)
    # CIRCREF_CHECK.clear()
    return resp


def serializer(*args, **kwargs):
    return _tojson(*args, **kwargs)


def tojson(*args, **kwargs):
    CIRCREF_CHECK.clear()
    return _tojson(*args, **kwargs)


def _tojson(data: Union[list, db.Model, dict], *args, **kwargs):
    exclude = kwargs.get('exclusions', set())
    resp: dict = None
    if isinstance(data, Iterable) and not isinstance(data, (dict, str, tuple)):
        Config.collection = True
        transformed = []
        for (idx, elem) in enumerate(data):
            if idx == 0:
                deny_func = getattr(elem, '__denials__', None)
                if deny_func:
                    kwargs.get('exclusions').extend(deny_func('__collection__'))
            transformed.append(_tojson(elem, *args, **kwargs))
        return transformed
    elif isinstance(data, db.Model):
        resp = {}
        final = set(columns(data, True)).difference(set(exclude))
        hidden = getattr(data, '__hidden__', set())
        final = final.difference(hidden)
        for column in final:
            resp[column] = getattr(data, column, None)

        if not getattr(data, primarykey(data)) in CIRCREF_CHECK:
            CIRCREF_CHECK.add(getattr(data, primarykey(data)))
            resp.update(extract_special_members(data, *args, **kwargs))
            resp.update(extract_relationships(data, **kwargs))

    elif isinstance(data, tuple):
        resp = {}
        # this will cover the cases where you select fields explicitly
        # and SQLAlchemy returns a results tuple rather than a full db.Model
        final = set(columns(data, True)).difference(exclude)
        for column in final:
            resp[column] = getattr(data, column, None)
        resp.update(extract_special_members(data, *args, **kwargs))
    elif isinstance(data, (dict, str, int)):
        return data
    # CIRCREF_CHECK.clear()
    return resp


def _serializer(data, exclude=set(), **kwargs):
    """
    Takes a SQLAlchemy Model (db.Model) and converts it into a response ready JSON format.

    :param data: list of db.Model types or single instance of db.Model types
    :param exclude:
    :return:
    """

    if not exclude:
        exclude = kwargs.get('exclusions', set())

    if isinstance(data, db.Model):
        resp = {}
        final = set(columns(data, True)).difference(exclude)
        for column in final:
            resp[column] = getattr(data, column, None)
        return resp
    elif isinstance(data, list):
        resp = []
        for elem in data:
            resp.append(serializer(elem, exclude))
        return resp


def save(session):
    session.save()


def primarykey(model):
    return model.__mapper__.primary_key[0].name


def get_primary_key(model):
    return model.__mapper__.primary_key[0].name


def get_primary_key_field(model):
    return model.__mapper__.primary_key[0]


def hidden_fields(element):
    return set([getattr(col, 'name', col) for col in getattr(element, '__hidden__', set())])


def update(self, commit=True, **kwargs):
    for attr, value in kwargs.items():
        if attr != 'id' and attr in self.fields():
            setattr(self, attr, value)

    for mtm in set(self.relationattrs()).intersection(set(kwargs.keys())):
        model = getattr(self, mtm)
        current = set(map(lambda rel: getattr(rel, rel.identify_primary_key()), model))
        candidates = set(map(lambda item: list(item.values()).pop(), kwargs[mtm]))
        for addition in candidates.difference(current):
            association = db.session.query(self.__mapper__.relationships.classgroups.entity).get(addition)
            getattr(self, mtm).append(association)

        for removal in current.difference(candidates):
            association = db.session.query(self.__mapper__.relationships.classgroups.entity).get(removal)
            getattr(self, mtm).remove(association)
    self.save()
    return self


def related(model, lookup=None):
    if isinstance(model, tuple):
        return list()

    if lookup:
        return getattr(model, lookup).entity.entity

    related_models = list()
    for i in model.__mapper__.relationships:
        related_models.append(i.entity.entity)
    return related_models


def get_relationships(model):
    return list(model.__mapper__.relationships)


def get_model_from_relationship(model, rel):
    return getattr(model, rel).property.entity.entity


def relationships(model, fmt=False):
    rels = model.__mapper__.relationships
    if fmt:
        return set(map(lambda x: x.key, rels))
    return rels


def columns(model, strformat=False, relations=None):
    if isinstance(model, tuple):
        return model._fields
    if not model:
        return None
    bound_columns = set(model.__mapper__.columns)
    if relations:
        return bound_columns.union(set([i.class_attribute for i in model.__mapper__.relationships]))
    if strformat:
        return [i.name for i in bound_columns]
    return bound_columns


def getschema(model):
    cols = set([i.name for i in columns(model)])
    cols = cols.difference([i.name for i in getattr(model, 'hidden', [])])
    schemamap = {
        'model': model.__tablename__,
        'fields': []
    }

    for item in cols:
        column = getattr(model, item)
        schemamap['fields'].append(dict(name=column.name, type=str(column.type)))

    return schemamap


def extract(element, fields=None, exclude: Optional[set] = None, **kwargs) -> Optional[dict]:
    resp = dict()
    if element is None:
        return None
    if exclude is None:
        exclude = set()

    if fields is None:
        fields = columns(element, strformat=True)

    for column in set(fields or []).difference(set(exclude)).difference(hidden_fields(element)):
        if isinstance(getattr(element, column), datetime) or isinstance(getattr(element, column), date):
            resp[column] = str(getattr(element, column))
        else:
            resp[column] = getattr(element, column)

    for prop in getattr(element, '__properties__', set()):
        property = serializer(getattr(element, prop.__name__), exclude)
        resp[prop.__name__] = property

    if getattr(element, '__counts__', None):
        resp['__counts__'] = getattr(element, '__counts__')

    if getattr(element, '__expose__', None):
        for entity in getattr(element, '__expose__'):
            if entity.key in exclude:
                continue
            if entity.uselist:
                resp[entity.key] = []
                for child in getattr(element, entity.key):
                    resp[entity.key].append(extract(child))
            else:
                resp[entity.key] = extract(getattr(element, entity.key, None))
    return resp


def process_relationship(data, exclude):
    resp = None
    if isinstance(data, list):
        resp = []
        for item in data:
            resp.append(extract(item, columns(item, strformat=True), exclude))
        return resp
    else:
        resp = extract(data, columns(data, strformat=True), exclude)
    return resp


def transform(data, fields=None, relations=None, **kwargs):
    if isinstance(data, list):
        resp = []
        for item in data:
            resp.append(extract(item))
        return resp
    elif isinstance(data, dict):
        return extract(data)
    return data


def iserialize(data, fields=None, rels=None, root=None, exclusions=None, functions=None,
               **kwargs):
    """
    This utility function dynamically converts Alchemy model classes into a
    dict using introspective lookups. This saves on manually mapping each
    model and all the fields. However, exclusions should be noted. Such as
    passwords and protected properties.

    :param model: SQLAlchemy model
    :param data: query data
    :param functions:
    :param fields: More of a whitelist of fields to include (preferred way)
    :param rels: Whether or not to introspect to relationships
    :param exc: Fields to exclude from query result set
    :param root: Root model for processing relationships. This acts as a
    recursive sentinel to prevent infinite recursion due to selecting oneself
    as a related model, and then infinitely trying to traverse the roots
    own relationships, from itself over and over.
    :param exclude: Exclusion in set form. Currently in favour of exc param.

    Only remedy to this is also to use one way relationships. Avoiding any
    back referencing of models.

    :return: json data structure of model
    :rtype: dict
    """

    if functions is None:
        functions = {}
    if exclusions is None:
        exclude = set()
    else:
        exclude = set(exclusions)

    model = data
    if isinstance(data, list) and len(data):
        model = data[0]

    exclude = exclude.union(set(kwargs.get('exclusions', set())))
    exclude.update(map(lambda col: getattr(col, 'name', col), getattr(model, 'hidden', set())))
    exclude.update(map(lambda col: getattr(col, 'name', col), getattr(model, '__hidden__', set())))

    if not data:
        return []

    if rels is True:
        rels = relationships(model, True)

    if not fields:
        fields = set(columns(model, strformat=True))

    fields = fields.difference(exclude)

    def process(element):
        if getattr(element, '_fields', None):
            transformed = {}
            for idx, field in enumerate(element._fields):
                transformed[field] = element[idx]
            return transformed

        transformed = extract(element, fields, exclude, **kwargs)
        if functions:
            for key, value in functions.items():
                transformed[f'_{key}'] = value(getattr(element, key))
        # rels = set([i.key for i in element.__mapper__.relationships]).intersection(fields)

        for item in rels or []:
            if '.' in item:
                left, right = item.split('.')
                _ = process_relationship(getattr(element, left), exclude)

                for idx, i in enumerate(getattr(element, left)):
                    _[idx][right] = extract(getattr(i, right))
                transformed[left] = _
                continue

            rel = None
            if getattr(element, item, None):
                rel = process_relationship(getattr(element, item), exclude)
                transformed[item] = rel
        return transformed

    if root is None:
        root = model.__tablename__

    # Define our model properties here. Columns and Schema relationships
    if not isinstance(data, list):
        return process(data)
    resp = []
    for element in data:
        resp.append(process(element))
    return resp


def serialize(model, data, fields=None, exc: Optional[set] = None, rels=None, root=None, exclude=None, functions=None,
              **kwargs):
    """
    This utility function dynamically converts Alchemy model classes into a
    dict using introspective lookups. This saves on manually mapping each
    model and all the fields. However, exclusions should be noted. Such as
    passwords and protected properties.

    :param model: SQLAlchemy model
    :param data: query data
    :param functions:
    :param fields: More of a whitelist of fields to include (preferred way)
    :param rels: Whether or not to introspect to relationships
    :param exc: Fields to exclude from query result set
    :param root: Root model for processing relationships. This acts as a
    recursive sentinel to prevent infinite recursion due to selecting oneself
    as a related model, and then infinitely trying to traverse the roots
    own relationships, from itself over and over.
    :param exclude: Exclusion in set form. Currently in favour of exc param.

    Only remedy to this is also to use one way relationships. Avoiding any
    back referencing of models.

    :return: json data structure of model
    :rtype: dict
    """

    if functions is None:
        functions = {}
    if exclude is None:
        exclude = set()
    else:
        exclude = set(exclude)

    exclude = exclude.union(set(kwargs.get('exclusions', set())))

    if rels is True:
        rels = relationships(model, True)

    exclude.update(map(lambda col: getattr(col, 'name', col), getattr(model, 'hidden', set())))
    exclude.update(map(lambda col: getattr(col, 'name', col), getattr(model, '__hidden__', set())))

    if not fields:
        fields = set(columns(model, strformat=True))

    fields = fields.difference(exclude)

    def process(element):
        if getattr(element, '_fields', None):
            transformed = {}
            for idx, field in enumerate(element._fields):
                transformed[field] = element[idx]
            return transformed

        transformed = extract(element, fields, set(), **kwargs)
        if functions:
            for key, value in functions.items():
                transformed[f'_{key}'] = value(getattr(element, key))
        # rels = set([i.key for i in element.__mapper__.relationships]).intersection(fields)

        for item in rels or []:
            if '.' in item:
                left, right = item.split('.')
                _ = process_relationship(getattr(element, left), exclude)

                for idx, i in enumerate(getattr(element, left)):
                    _[idx][right] = extract(getattr(i, right))
                transformed[left] = _
                continue

            rel = None
            if getattr(element, item, None):
                rel = process_relationship(getattr(element, item), exclude)
            transformed[item] = rel
        return transformed

    if root is None:
        root = model.__tablename__

    # Define our model properties here. Columns and Schema relationships
    if not isinstance(data, list):
        return process(data)
    resp = []
    for element in data:
        resp.append(process(element))
    return resp


def json(data):
    resp = None

    if isinstance(data, list):
        resp = []
    for item in data:
        resp.append(extract(item))
    return resp
