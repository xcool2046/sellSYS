from pydantic import BaseModel
from typing import Optional

# 基础模型
class ContactBase(BaseModel):
    name: str
    title: Optional[str] = None
    phone: str
    email: Optional[str] = None
    notes: Optional[str] = None

# 创建模型
class ContactCreate(ContactBase):
    pass

# 更新模型
class ContactUpdate(BaseModel):
    name: Optional[str] = None
    title: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    notes: Optional[str] = None

# 数据库返回模型
class Contact(ContactBase):
    id: int
    customer_id: int

    class Config:
        from_attributes = True