from pydantic import BaseModel
from typing import Optional

# 基础模型
class DepartmentGroupBase(BaseModel):
    name: str

# 创建模型
class DepartmentGroupCreate(DepartmentGroupBase):
    pass

# 更新模型
class DepartmentGroupUpdate(BaseModel):
    name: Optional[str] = None

# 数据库返回模型
class DepartmentGroup(DepartmentGroupBase):
    id: int

    class Config:
        from_attributes = True