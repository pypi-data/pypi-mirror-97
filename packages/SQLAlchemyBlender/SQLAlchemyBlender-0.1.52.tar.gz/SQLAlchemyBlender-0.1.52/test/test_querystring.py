import unittest
import random
import uuid

from datetime import datetime

from urllib import parse
from sqlalchemy import Column, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy import or_
from sqlalchemy.orm import load_only
from sqlalchemy.orm import sessionmaker
from sqlalchemy_blender import db
from sqlalchemy_blender.types import UUID
from sqlalchemy_blender.processor import QueryString


class TestChild(db.Model):
    __tablename__ = 'child'
    id = Column(db.Integer, primary_key=True)
    uuid = Column(UUID, name='uuid', default=uuid.uuid4())
    name = Column(db.String(256), nullable=False)
    note = Column(db.String(256), nullable=False)
    comment = Column(db.String(256), nullable=False)
    created = Column(db.DateTime(), default=func.now())


class TestModel(db.Model):
    __tablename__ = 'test'
    id = Column(db.Integer, primary_key=True)
    uuid = Column(UUID, name='uuid', default=uuid.uuid4())
    name = Column(db.String(256), nullable=False)
    note = Column(db.String(256), nullable=False)
    comment = Column(db.String(256), nullable=False)
    created = Column(db.DateTime(), default=func.now())
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), nullable=True)
    child = db.relationship('TestChild', backref=db.backref('parent'), uselist=False, lazy='select')


class TestRelated(db.Model):
    __tablename__ = 'related'
    id = Column(db.Integer, primary_key=True)
    uuid = Column(UUID, name='uuid', default=uuid.uuid4())
    name = Column(db.String(256), nullable=False)
    note = Column(db.String(256), nullable=False)
    comment = Column(db.String(256), nullable=False)
    created = Column(db.DateTime(), default=func.now())


class TestQueryString(unittest.TestCase):

    def setUp(self) -> None:
        db_uri = 'sqlite:///:memory:'
        engine = create_engine(db_uri, echo=True)
        session = sessionmaker(bind=engine)
        """:type: sqlalchemy.orm.Session"""
        self.session = session()
        db.metadata.create_all(engine)

        for idx in range(0, 10):
            self.session.add(TestModel(name='test1', note='test`', comment='test`'))
            self.session.add(TestModel(name='test', note='test', comment='test'))
            child = TestChild(name='test', note='test', comment='test')
            self.session.add(TestModel(name='test', note='test', comment='test', child=child))
            self.session.add(TestModel(name='test', note='test', comment='test', created=datetime(2000, random.randint(1, 11), 1)))

    def test_querystring_resolves(self):
        querystring = 'fields=test&fields=bla&order_by=url'

        qs = dict([('content', 'false'), ('order_by', 'url id'), ('fields', 'test2,test3'), ('fields', 'test'), ('test5', '')])

        serialized = parse.parse_qs(querystring)

        # resp = QueryString()

        query: db.session.query = self.session.query(TestModel)
        data = query.all()
        self.assertEqual(len(data), 40)

        query = self.session.query(TestModel)
        data = query.filter(TestModel.name == 'test1').all()
        self.assertEqual(len(data), 10)

        query = self.session.query(TestModel)
        data = query.filter_by(**{TestModel.name.name: 'test'}).all()
        self.assertEqual(len(data), 30)

        data = self.session.query(TestModel).get(10)

        # filtering results less than
        query = self.session.query(TestModel)
        data = query.filter(TestModel.created <= datetime.now()).all()

        # filtering results greater than
        query = self.session.query(TestModel)
        data = query.filter(TestModel.created >= datetime.now()).all()

        # filtering results using IN
        query = self.session.query(TestModel)
        query = query.filter(TestModel.id.in_([1, 2, 3, 4]))

        # filtering results using AND in WHERE clause
        query = self.session.query(TestModel)
        query = query.filter(TestModel.id == 1)
        query = query.filter(TestModel.id == 2)

        # filtering results using OR in WHERE clause
        query = self.session.query(TestModel)
        query = query.filter((TestModel.id == 1) | (TestModel.id == 2))

        query = query.order_by(TestModel.created)
        data = query.all()
        pass
