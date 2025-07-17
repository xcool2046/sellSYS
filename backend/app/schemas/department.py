from pydantic import BaseModel
from typing import Optional

# 基础模型，包含所有共享字段
class DepartmentBase(BaseModel):
    name: str
    group_id: Optional[int] = None # 部门可以不属于任何分组

# 创建模型，继承自基础模型
class DepartmentCreate(DepartmentBase):
    pass

# 更新模型，所有字段都是可选的
class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    group_id: Optional[int] = None

# 数据库返回模型，包含数据库中的所有字段
class Department(DepartmentBase):
    id: int

    class Config:
        from_attributes = True