from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Float

Base = declarative_base()

class RaceResult(Base):

    __tablename__ = 'race_result'

    id =  Column(String(12), primary_key=True)
    name = Column(String(200))
    cource_id = Column(String(3))
    cource_length = Column(String(5))
    date = Column(String(11))
    cource_type = Column(String(5))
    cource_condition = Column(String(10))
    entire_rap = Column(String(200))
    ave_1F = Column(Float)
    first_half_ave_3F = Column(Float)
    last_half_ave_3F = Column(Float)
    RPCI = Column(Float)
    prize = Column(Float)
    hose_all_number = Column(Integer)

    def __repr__(self):
        return "<RaceResult(id='%s', name='%s', cource_id='%s', cource_length='%s', date='%s', cource_type='%s', cource_condition='%s', entire_rap='%s', ave_1F='%f', first_half_ave_3F='%f',last_half_ave_3F='%f',RPCI='%f', prize='%s'>" % (self.id, self.name, self.cource_id, self.cource_length, self.date, self.cource_type, self.cource_condition, self.entire_rap, self.ave_1F, self.first_half_ave_3F, self.last_half_ave_3F, self.RPCI, self.prize) 
