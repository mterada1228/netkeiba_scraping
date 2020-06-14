from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey

Base = declarative_base()
 
class HoseRaceResult(Base):

    __tablename__ = 'hose_race_result'

    hose_id = Column(String(10), primary_key=True)
    race_id = Column(String(12), primary_key=True)
    gate_num = Column(String(2))
    hose_num = Column(String(2))
    odds = Column(String(6))
    popularity = Column(String(2))
    rank = Column(String(2))
    jockey = Column(String(10))
    burden_weight = Column(String(4))
    time = Column(String(8))
    time_diff = Column(String(5))
    passing_order = Column(String(10))
    last_3f = Column(String(5))
    hose_weight = Column(String(4))
    hose_weight_diff = Column(String(4))
    get_prize = Column(String(20))

    def __repr__(self):
        return "<HoseRaceResult(hose_id='%s',race_id='%s',gate_num='%s',hose_num='%s',odds='%s',popularity='%s',rank='%s',jockey='%s',burden_weight='%s',time='%s',time_diff='%s',passing_order='%s',last_3f='%s',hose_weight='%s',hose_weight_diff='%s',get_prize='%s')>" % (self.hose_id, self.race_id, self.gate_num, self.hose_num, self.odds, self.popularity, self.rank, self.jockey, self.burden_weight, self.time, self.time_diff, self.passing_order, self.last_3f, self.hose_weight, self.hose_weight_diff, self.get_prize)