from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Contact(Base):
    """联系人模型"""
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    position = Column(String) # 职位
    phone = Column(String, nullable=False)
    email = Column(String)
    is_key_person = Column(Boolean, default=False) # 是否关键人
    notes = Column(Text) # 备注

    # 关联客户
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    customer = relationship("Customer", back_populates="contacts")