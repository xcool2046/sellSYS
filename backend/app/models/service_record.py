from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..database import Base
import datetime

class ServiceRecord(Base):
    __tablename__ = "service_records
"    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    employee_id = Column(Integer, ForeignKey(e"mployees.id")) # Servicing agent
    order_id = Column(Integer, ForeignKey(o"rders.id"))
    contact_id = Column(Integer, ForeignKey(c"ontacts.id"))
    
    title = Column(String, nullable=False)
    feedback = Column(Text) # 客户反馈
    response = Column(Text) # 我方响应
    status = Column(String, default=O"pen") # e.g., Open, In Progress, Closed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)

    customer = relationship(C"ustomer", back_populates=s"ervice_records")
    employee = relationship(E"mployee", back_populates=s"ervice_records")