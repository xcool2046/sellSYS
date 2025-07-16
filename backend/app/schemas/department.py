from pydantic import BaseModel
from typing import Optional

# 基础模型
class DepartmentBase(BaseModel):
    name: str
    group_id: int

# 创建模型
class DepartmentCreate(DepartmentBase):
    pass

# 更新模型
class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    group_id: Optional[int] = None

# 数据库返回模型
class Department(DepartmentBase):
    id: int

    class Config:
        from_attributes = True