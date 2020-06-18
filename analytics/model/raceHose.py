from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey

Base = declarative_base()
 
class RaceHose(Base):

    __tablename__ = 'race_hose'

    race_id = Column(String(12), primary_key=True)
    hose_id = Column(String(10), primary_key=True)
    gate_num = Column(String(2))
    hose_num = Column(String(2))

    def __repr__(self):
        return "<RaceResult(hose_id='%s', name='%s')>" % (self.hose_id, self.name)