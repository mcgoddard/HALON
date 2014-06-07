from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base
import datetime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(128), unique=False)
    active_until = Column(DateTime, unique=False, default=(datetime.datetime.now))
    x = Column(Integer, unique=False)
    y = Column(Integer, unique=False)
    direction = Column(Integer, unique=False)
    character = Column(Integer, unique=False)
    health = Column(Integer, unique=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.username)

class Tile(Base):
    __tablename__ = 'tiles'
    id = Column(Integer, primary_key=True)
    x = Column(Integer)
    y = Column(Integer)
    tile_type = Column(Integer)
    status = Column(Integer)

    def __init__(self, x, y, tile_type, status):
        self.x = x
        self.y = y
        self.tile_type = tile_type
        self.status = status

    def __repr__(self):
        return '<Tile %r>' % (self.id)

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    text = Column(String(144), unique=False)
    created_at = Column(DateTime, unique=False, default=datetime.datetime.now)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref=backref('messages', lazy='dynamic'))
    x = Column(Integer)
    y = Column(Integer)

    def __init__(self, text, user):
        self.text = text
        self.user = user

    def __repr__(self):
        return '<Message %r>' % (self.text)