# -*- coding: utf-8 -*-
    
from scrapy.utils.project import get_project_settings

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Text, create_engine

Base = declarative_base()

class Article(Base):
    __tablename__ = 'article'

    title = Column(String(128), primary_key = True)
    author = Column(String(128))
    create_time = Column(String(19))
    content = Column(Text)

class Picture(Base):
    __tablename__ = 'picture'

    title = Column(String(128), primary_key = True)
    author = Column(String(128))
    create_time = Column(String(19))
    paths = Column(Text)

class Offset(Base):
    __tablename__ = 'offset'
    
    type = Column(String(32), primary_key = True)
    href = Column(String(256))



class MysqlHandler(object):
    def __init__(self):
        settings = get_project_settings()
        cmd = 'mysql+mysqldb://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(
            settings.get('MYSQL_USER'),
            settings.get('MYSQL_PASS'),
            settings.get('MYSQL_HOST'),
            settings.get('MYSQL_PORT'),
            settings.get('MYSQL_DB')
        )
        engine = create_engine(cmd)
        self.session = sessionmaker(bind = engine)
        return

    def get_session(self):
        return self.session()

    def get_offset(self, type):
        session = self.session()
        offset = session.query(Offset).filter_by(type = type).first()
        session.close()
        if not offset:
            return None
        else:
            return offset.href

    def set_offset(self, type, href):
        session = self.session()
        offset = session.query(Offset).filter_by(type = type).first()
        if not offset:
            offset = Offset(type = type, href = href)
            session.add(offset)
        else:
            offset.href = href
        session.commit()
        session.close()
        return

