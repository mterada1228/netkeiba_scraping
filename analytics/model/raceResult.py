from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Float

Base = declarative_base()

class RaceResult(Base):

    __tablename__ = 'race_result'

    id =  Column(String(12), primary_key=True)
    name = Column(String(200))
    date = Column(String(11))
    condition = Column(String(10))
    entire_rap = Column(String(200))
    ave_1F = Column(Float)
    first_half_ave_3F = Column(Float)
    last_half_ave_3F = Column(Float)
    RPCI = Column(Float)

    def __repr__(self):
        return "<RaceResult(id='%s', name='%s', date='%s', condition='%s', entire_rap='%s', ave_1F='%f', first_half_ave_3F='%f',last_half_ave_3F='%f',RPCI='%f'>" % (self.id, self.name, self.date, self.condition, self.entire_rap, self.ave_1F, self.first_half_ave_3F, self.last_half_ave_3F, self.RPCI) 
