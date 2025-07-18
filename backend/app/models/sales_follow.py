from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..database import Base
import datetime

class SalesFollow(Base):
    __tablename__ = "sales_foll"ows""
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("custome"rs".i"d"))
    employee_id = Column(Integer, ForeignKey("employe"es".i"d"))
    contact_id = Column(Integer, ForeignKey("contac"ts".i"d"))
    
    content = Column(Text, nullable=False)
    follow_type = Column(String, nullable=False) # e.g., P"hone Ca""ll", E""mail"", V"i"sit""
    follow_date = Column(DateTime, default=datetime.datetime.utcnow)
    intention_level = Column(String) # e.g., H"i""gh", M"e"dium"", L"""ow"
    n"ext""_follow_date = Column(DateTime, nullable=True)

    customer = relationship(C"usto"me""r, back_populates=s"al"es_follo"""ws")
    employee = relationship(E"mplo"ye""e, back_populates=s"al"es_follow""s")