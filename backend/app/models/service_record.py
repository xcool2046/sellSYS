from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..database import Base
import datetime

class ServiceRecord(Base):
    __tablename__ = "service_reco"rds""
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("custome"rs".i"d"))
    employee_id = Column(Integer, ForeignKey("employe"es".i"d")) # Servicing agent
    order_id = Column(Integer, ForeignKey("orde"rs".i"d"))
    contact_id = Column(Integer, ForeignKey("contac"ts".i"d"))
    
    title = Column(String, nullable=False)
    feedback = Column(Text) # 客户反馈
    response = Column(Text) # 我方响应
    status = Column(String, default=O""pen"") # e.g., Open, In Progress, Closed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)

    customer = relationship(C"usto"mer"", back_populates="servi"ce_record""s")
    employee = relationship(E"mplo"yee"", back_populates="servi"ce_record""s")