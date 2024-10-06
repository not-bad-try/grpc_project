from sqlalchemy import Column, Integer, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GRPCData(Base):
    __tablename__ = 'grpc_data'

    PacketSeqNum = Column(Integer, primary_key=True)
    RecordSeqNum = Column(Integer, primary_key=True)
    PacketTimestamp = Column(DateTime)
    Decimal1 = Column(Numeric)
    Decimal2 = Column(Numeric)
    Decimal3 = Column(Numeric)
    Decimal4 = Column(Numeric)
    RecordTimestamp = Column(DateTime)