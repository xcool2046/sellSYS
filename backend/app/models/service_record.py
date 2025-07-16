from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..database import Base
import datetime

class ServiceRecord(Base):
    __tablename__ = "service_records"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    employee_id = Column(Integer, ForeignKey("employees.id")) # Servicing agent
    
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, default="Open") # e.g., Open, In Progress, Closed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)

    customer = relationship("Customer")
    employee = relationship("Employee")