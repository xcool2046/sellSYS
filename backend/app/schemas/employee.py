from pydantic import BaseModel, EmailStr
from typing import Optional
from ..models.employee import EmployeeRole

# 基础模型
class EmployeeBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: EmployeeRole

# 创建模型
class EmployeeCreate(EmployeeBase):
    password: str

# 更新模型
class EmployeeUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[EmployeeRole] = None
    is_active: Optional[bool] = None

# 数据库返回模型
class Employee(EmployeeBase):
    id: int
    is_active: bool
    department_id: Optional[int] = None

    class Config:
        from_attributes = True # Pydantic v2 orm_mode is now from_attributes