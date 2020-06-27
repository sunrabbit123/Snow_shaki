from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Table, Column, Integer, String

Base = declarative_base()

class made_command(Base):
    __tablename__ = 'made_command'

    id = Column(Integer,primary_key = True)
    server_nickname= Column(String(50))
    server_id = Column(String(50))
    author = Column(String(50))
    keycommand = Column(String(255))
    valuecommand = Column(String(255))

    def __init__(self,server_nickname,server_id,author,keycommand,valuecommand):
        self.server_id = server_id
        self.server_nickname = server_nickname
        self.author = author
        self.keycommand = keycommand
        self.valuecommand = valuecommand

    def __repr__(self):
        return '<made_command %s %s %s>' %\
            (self.server_id,self.keycommand,self.valuecommand)