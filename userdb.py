from sqlalchemy import MetaData, Column, Table, ForeignKey
from sqlalchemy import Integer, String, Float, DateTime, PickleType
from sqlalchemy.orm import relationship, backref
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class candidate_table(Base):
    __tablename__ = "candidates"

    cand_id = Column(Integer, primary_key=True)
    user = Column(String, ForeignKey('USERS.user'))
    kic = Column(String)
    period = Column(Float)
    uploadtime = Column(DateTime)
    folded_lc = Column(PickleType)
    label = Column(String)
    offset = Column(Float)
    def __init__(self, user, kic, period, offset, folded_lc, label):
        #self.cand_id = cand_id
        self.user = user
        self.kic = kic
        self.period = period
        self.uploadtime = datetime.now()
        self.folded_lc = folded_lc
        self.label = label
        self.offset = offset
    def __repr__(self):
        return "<candidate no.%s|%s|%s|uploaded by %s on %s>" % (self.cand_id, self.kic, self.period, self.user, self. uploadtime.strftime("%y-%m-%d"))

class user_table(Base):
    __tablename__ = "USERS"

    user = Column(String, primary_key=True)
    password = Column(String(10))
    candidates = relationship("candidate_table", backref="USERS", order_by=candidate_table.cand_id)

    def __init__(self, user, password):
        self.user = user
        self.password = password
    def __repr__(self):
        return "<user:%s>" % (self.user)
#print file_table.__table__


