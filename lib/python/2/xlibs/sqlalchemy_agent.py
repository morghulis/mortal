# -*- coding:utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class SQLAgent(object):

    def __init__(self, db_uri, echo=False):
        self.engine = create_engine(db_uri)
        self.sessionmaker = sessionmaker(bind=self.engine)

        self.model = declarative_base()

    def new_session(self):
        return self.sessionmaker()


    def create_all(self):
        self.model.metadata.create_all(self.engine)


    def drop_all(self):
        self.model.metadata.drop_all(self.engine)

