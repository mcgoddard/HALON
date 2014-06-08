from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
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
    health = Column(Integer, unique=False)
    moving = Column(Boolean)
    character_id = Column(Integer, ForeignKey('characters.id'))
    character = relationship('Character', backref=backref('users', lazy='dynamic'))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.username)

class Character(Base):
	__tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    description = Column(String(50))
    max_health = Column(Integer)
    speed = Column(Integer)
    decode_time = Column(Integer)
    regen_speed = Column(Integer)

    def __init__(self, name, description, max_health, speed, decode_time, regen_speed):
        self.name = name
        self.description = description
        self.max_health = max_health
        self.speed = speed
        self.decode_time = decode_time
        self.regen_speed = regen_speed

    def __repr__(self):
        return '<Character %r>' % (self.name)

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
