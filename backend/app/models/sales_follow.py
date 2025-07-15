from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..database import Base
import datetime

class SalesFollow(Base):
    __tablename__ = "sales_follows"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    employee_id = Column(Integer, ForeignKey("employees.id"))
    
    content = Column(Text, nullable=False)
    follow_type = Column(String, nullable=False) # e.g., "Phone Call", "Email", "Visit"
    follow_date = Column(DateTime, default=datetime.datetime.utcnow)
    intention_level = Column(String) # e.g., "High", "Medium", "Low"
    next_follow_date = Column(DateTime, nullable=True)

    customer = relationship("Customer")
    employee = relationship("Employee")