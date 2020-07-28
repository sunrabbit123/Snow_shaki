import configparser
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker,scoped_session
from sqlalchemy.ext.declarative import declarative_base
from os.path import join, exists

from models import made_command, Base
from data import databa


class dbmanger:
    def __init__(self):
        address = create_engine(databa.local)
        Base.metadata.create_all(address)

        self.session = sessionmaker()
        self.session.configure(bind = address)
        self.session = self.session()
    
    def insert_row(self,data):
        self.session.add(data)
        self.session.commit()
    
    def search_data(self,table,column,data):
        try:
            keyword = getattr(table,column)
            query = self.session.query(table).filter(keyword == (data))
            return query.all()
        except(AttributeError):
            pass
    def delete_data(self,data):
        self.session.delete(data)
        self.session.commit()

if __name__ == '__main__':
    pass

    
