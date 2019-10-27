from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData, Table, Column, Integer,ForeignKey, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import desc
import pandas as pd

engine = create_engine('sqlite:///db.sqlite3', echo=True)

Base = declarative_base()

class LineName(Base):
    """
    key と nameのマップ
    """
    __tablename__="linename"
    device=Column(String, primary_key=True)
    name=Column(String)
    aveleavetime = Column(Float)
    lineque = relationship("LineQue", back_populates="linename")

class LineQue(Base):

    # テーブル名
    __tablename__ = 'lineque'
    # 個々のカラムを定義
    id = Column(String, primary_key=True)
    device = Column(String, ForeignKey('linename.device'))
    ob_time = Column(Float)
    count = Column(Integer)
    que_time = Column(Float)
    diff = Column(Integer)
    linename = relationship("LineName", back_populates="lineque") 

meta = Base.metadata
meta.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

df = pd.read_csv("test_data.csv")
for sr in df.iterrows():
    session.add(LineName(device=sr[1]["device"],
                name=sr[1]["name"],
                aveleavetime=sr[1]["aveleavetime"]))
    session.commit()
session.close()