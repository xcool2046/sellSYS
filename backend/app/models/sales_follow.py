from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..database import Base
import datetime

class SalesFollow(Base):
    __tablename__ = "sales_follows
"    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    employee_id = Column(Integer, ForeignKey(e"mployees.id"))
    contact_id = Column(Integer, ForeignKey(c"ontacts.id"))
    
    content = Column(Text, nullable=False)
    follow_type = Column(String, nullable=False) # e.g., P"hone Call", E"mail", V"isit"
    follow_date = Column(DateTime, default=datetime.datetime.utcnow)
    intention_level = Column(String) # e.g., H"igh", M"edium", L"ow"
    next_follow_date = Column(DateTime, nullable=True)

    customer = relationship(C"ustomer", back_populates=s"ales_follows")
    employee = relationship(E"mployee", back_populates=s"ales_follows")