from sqlalchemy import (create_engine, Column, 
                        DateTime, Integer, Float, String, create_engine)
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Prices(Base):

    __tablename__ = "Prices"

    id = Column(Integer, primary_key=True)
    Ticker = Column(String(32))  
    Date = Column(DateTime)
    High = Column(Float(3))
    Low = Column(Float(3))
    Open = Column(Float(3))
    Close = Column(Float(3))
    Volume = Column(Float(3))
    AdjClose = Column(Float(3))
    
    __table_args__ = (
                      UniqueConstraint('Ticker', 'Date', name='Ticker_Date'),
                     )

def create_table():                     
    engine = create_engine('sqlite:///./prices.db', echo=False)
    if not engine.dialect.has_table(engine, 'Prices'):
        Base.metadata.create_all(engine)
    return engine