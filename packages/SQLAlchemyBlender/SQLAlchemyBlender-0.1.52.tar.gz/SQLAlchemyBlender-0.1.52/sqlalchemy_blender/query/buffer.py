from copy import deepcopy

from flask import request
from flask import current_app
from flask_sqlalchemy import BaseQuery
from sqlalchemy.ext.declarative import DeclarativeMeta

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import load_only
from sqlalchemy import desc
from sqlalchemy import func

from sqlalchemy_blender import serialize
from sqlalchemy_blender import relationships
from sqlalchemy_blender import columns
from sqlalchemy_blender import serialize
from sqlalchemy_blender.helpers import get_primary_key_field
from sqlalchemy_blender.helpers import get_relationships
from sqlalchemy_blender.query.processor import QueryStringProcessor

from handyhttp import HTTPNotFound
from handyhttp import HTTPBadRequest


class QueryBuffer:
    ACCEPTED_CALLS = ['all', 'count']

    def __init__(self, model, queryargs=None, auto=True):
        self.session = current_app.extensions['sqlalchemy'].db.session
        if not queryargs:
            queryargs = QueryStringProcessor(dict(request.args)).validate(request.query_string)

        if isinstance(model, DeclarativeMeta):
            query = self.session.query(model)
            self.basequery: BaseQuery = query
            self._basequery: BaseQuery = query
        else:
            self.basequery: BaseQuery = model.query
            self._basequery: BaseQuery = model.query

        self.pagedquery = None
        self.queryargs: QueryStringProcessor = queryargs
        self.data = list()
        self.fields: set = set()
        self.count: int = 0
        self.flags = ['Y', 'N', 'P']
        self.paginated = False
        self.model = model
        self.active()
        self.errors = []

        if auto:
            self.apply()

    def __getattr__(self, f, *args, **kwargs):
        def _query_function(operation, *args, **kwargs):
            if hasattr(self.query, operation):
                return getattr(self.query, operation)
            raise NotImplementedError('This function is not available on the BaseQuery object.')
        return _query_function(f, *args, **kwargs)

    @staticmethod
    def querystring():
        return QueryStringProcessor(dict(request.args))

    def active(self):
        if getattr(self.model, 'active', None):
            self.basequery = self.basequery.filter(self.model.active != 'D')
            self.basequery = self.basequery.filter(self.model.active != 'X')
        return self

    @property
    def query(self):
        return self.basequery

    def check_key(self, key: str) -> bool:
        _key = key.split('.')
        for item in relationships(self.model):
            try:
                if _key[0] in [i.name for i in getattr(self.model, item).prop.target.columns]:
                    return True
            except Exception:
                continue
        return _key[0] in relationships(self.model)

    def prepare_query(self, fields):
        if not fields:
            self.basequery = self.session.query(self.model)
            return self.basequery
        select = [getattr(self.model, _field) for _field in fields]
        query = self.session.query(*select)
        self.basequery = query
        return self.basequery

    def build(self, query, queryargs, entity=None):
        entity = entity or query._entity_zero().entity
        base_fields = set(map(lambda x: x.key, entity.__mapper__.columns))
        _relationships = set(map(lambda x: x.key, entity.__mapper__.relationships))
        keys = columns(entity, strformat=True)
        fields = base_fields.difference(set(queryargs.exclusions))

        if queryargs.include:
            fields = set()
            for item in queryargs.include:
                if not {item}.issubset(base_fields):
                    raise HTTPBadRequest('{} is not a recognised attribute of this resource'.format(item))
                fields.add(item)
            self.fields = fields

        if queryargs.rels:
            if type(queryargs.rels) in [list, set]:
                fields.union(set(relationships(entity)).difference(queryargs.rels))
            elif queryargs.rels:
                fields.union(_relationships)
                queryargs.rels = _relationships

        updated_rels = set()

        if type(queryargs.rels) in [list, set]:
            for item in queryargs.rels:
                if self.check_key(item):
                    pass
                updated_rels.add(item)
            queryargs.rels = updated_rels

        if not queryargs.sortkey or queryargs.sortkey == '':
            queryargs.sortkey = get_primary_key_field(entity).name

        self.prepare_query(queryargs.include)

        if queryargs.sortkey in keys:
            column = getattr(entity, queryargs.sortkey, get_primary_key_field(entity))
            if queryargs.descending and queryargs.sortkey in columns(entity, strformat=True):
                query = query.order_by(desc(column))
            else:
                query = query.order_by(column)

        filters = queryargs.filters
        query, filters = self.check_relationship_filtering(query, filters)

        setfilters = []

        if getattr(queryargs, 'filterin', None):
            for key, search in getattr(queryargs, 'filterin').items():
                setfilters.append(getattr(entity, key).in_(search))
                del filters[key]

        query = query.filter(*setfilters)

        try:
            query = query.filter_by(**filters)
        except InvalidRequestError as exc:
            self.errors.append(str(exc))
            # raise HTTPBadRequest(str(exc))

        for key, value in queryargs.max:
            query = query.filter(getattr(self.model, key) <= value)

        for key, value in queryargs.min:
            query = query.filter(getattr(self.model, key) >= value)

        if queryargs.page:
            query = query.paginate(queryargs.page, queryargs.pagesize or 50, False)
            self.paginated = True
            return query

        default_field = getattr(self.model, self.model.__mapper__.primary_key[0].name)
        query = query.group_by(default_field)
        query = query.limit(self.queryargs.limit)
        # self.basequery = self.basequery.options(load_only(*self.fields))
        return query

    def apply(self, pending=False, inactive=False, query=None, entity=None):
        entity = entity or self.basequery._entity_zero()
        base_fields = set(map(lambda x: x.key, entity.column_attrs))
        _relationships = set(map(lambda x: x.key, entity.relationships))
        keys = columns(self.model, strformat=True)

        self.fields = base_fields.difference(set(self.queryargs.exclusions))
        # Now detect whether we want relationships

        # session.query(arti).join(arti, self.model.articles).filter(arti.active=='Y').order_by(desc(arti.created)).all()

        if self.queryargs.include:
            fields = set()
            for item in self.queryargs.include:
                if not {item}.issubset(base_fields):
                    raise HTTPBadRequest('{} is not a recognised attribute of this resource'.format(item))
                fields.add(item)
            self.fields = fields

        if self.queryargs.rels:
            if type(self.queryargs.rels) in [list, set]:
                self.fields.union(set(relationships(self.model)).difference(self.queryargs.rels))
            elif self.queryargs.rels:
                self.fields.union(_relationships)
                self.queryargs.rels = _relationships

        updated_rels = set()

        if type(self.queryargs.rels) in [list, set]:
            for item in self.queryargs.rels:
                if self.check_key(item):
                    pass
                updated_rels.add(item)
            self.queryargs.rels = updated_rels

        if not self.queryargs.sortkey or self.queryargs.sortkey == '':
            self.queryargs.sortkey = entity.primary_key[0].name

        self.prepare_query(self.queryargs.include)

        if self.queryargs.sortkey in keys:
            column = getattr(self.basequery._entity_zero().attrs, self.queryargs.sortkey)
            if self.queryargs.descending and self.queryargs.sortkey in columns(self.model, strformat=True):
                self.basequery = self.basequery.order_by(desc(column))
            else:
                self.basequery = self.basequery.order_by(column)

        filters = self.queryargs.filters
        self.basequery, filters = self.check_relationship_filtering(self.basequery, filters)

        setfilters = []

        if getattr(self.queryargs, 'filterin', None):
            for key, search in getattr(self.queryargs, 'filterin').items():
                setfilters.append(getattr(self.model, key).in_(search))
                del filters[key]
                # self.basequery = self.basequery.filter(getattr(self.model, key).in_(search))

        # filters = tuple(filter(lambda k: '.' not in k, filters.keys()))

        if 'active' in keys:
            if pending:
                self.flags.append('P')
                self.flags.append('C')
            if inactive:
                self.flags.append('N')
            self.flags.append('C')
            setfilters.append(getattr(self.model, 'active').in_(self.flags))
            # self.basequery = self.set_active_filter(self.basequery, self.flags)

        self.basequery = self.basequery.filter(*setfilters)

        try:
            self.basequery = self.basequery.filter_by(**filters)
        except InvalidRequestError as exc:
            self.errors.append(str(exc))
            # raise HTTPBadRequest(str(exc))

        for key, value in self.queryargs.max:
            self.basequery = self.basequery.filter(getattr(self.model, key) <= value)

        for key, value in self.queryargs.min:
            self.basequery = self.basequery.filter(getattr(self.model, key) >= value)

        if self.queryargs.page:
            self.pagedquery = self.basequery.paginate(self.queryargs.page, self.queryargs.pagesize or 50, False)
            self.paginated = True
            return self

        default_field = getattr(self.model, self.model.__mapper__.primary_key[0].name)
        self.basequery = self.basequery.group_by(default_field)
        self.basequery = self.basequery.limit(self.queryargs.limit)
        # self.basequery = self.basequery.options(load_only(*self.fields))
        return self

    def set_active_filter(self, query, flags):
        new_query = query
        if 'active' in columns(self.model, strformat=True) and self.model.active:
            new_query = query.filter(self.model.active.in_(flags))
        return new_query

    def check_relationship_filtering(self, query, filters):
        _filters = filters.copy()
        for item in filters.keys():
            splitter = item.split('.')
            if len(splitter) == 2:
                attribute = getattr(self.model, splitter[0]).comparator.entity.class_
                query = query.join(attribute).filter(getattr(attribute, splitter[1]) == filters[item])
                del _filters[item]
        return query, _filters

    def all(self, counts=True):
        if self.paginated:
            self.data = self.pagedquery.items
            self.count = getattr(self.basequery, 'count')()
            return self

        if counts:
            rels = get_relationships(self.model)
            primary_key = get_primary_key_field(self.model)
            query = self.session.query(self.model)
            count_queries = []
            for rel in rels:
                count = func.count(getattr(self.model, rel.key))
                count_queries.append(count)
                # self.basequery = self.basequery.with_entities(count)
                # query = query.with_entities(self.model, count)
            query = query.with_entities(self.model, *count_queries)
            query = query.group_by(primary_key)
        self.data = self.basequery.all()
        self.count = len(self.data)
        return self

    def get(self, lookup, field=None):
        if field:
            if isinstance(field, str):
                field = getattr(self.model, field)
            return self._basequery.filter(field == lookup).first()
        primary_key = self.model.__mapper__.primary_key
        if isinstance(primary_key, tuple):
            primary_key = primary_key[0]
        return self._basequery.filter(primary_key == lookup).first()

    def one(self, field, value):
        filter_expression = {field: value}
        self.prepare_query(self.queryargs.include)
        query = self.basequery.filter_by(**filter_expression)
        self.data = query.first()
        if not self.data:
            pass
            # raise HTTPNotFound(f'{str(self.model.__dict__.get("__tablename__")).capitalize()} not found!')
        for item in set([str(i.key) for i in relationships(self.model)]).intersection(self.queryargs.include):
            _item = item
            if not isinstance(_item, str):
                _item = str(item).split('.').pop()
            if isinstance(getattr(self.data, _item), BaseQuery):
                query = getattr(self.data, _item)
                related = QueryBuffer(query, deepcopy(self.queryargs), query._entity_zero().class_)
                related.basequery = related.set_active_filter(related.basequery, self.flags)
                related.fields = related.model.keys().difference(set(self.queryargs.exclusions))
                related_query_data = related.apply().all()
                setattr(self.data, '__i__' + item, related_query_data.json(autodata=False))
        return self

