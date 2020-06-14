from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey

Base = declarative_base()
 
class Hose(Base):

    __tablename__ = 'hose'

    hose_id = Column(String(10), primary_key=True)
    name = Column(String(20))

    def __repr__(self):
        return "<RaceResult(hose_id='%s', name='%s')>" % (self.hose_id, self.name)