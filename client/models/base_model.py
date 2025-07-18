"""
数据模型基础类
"""
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

class BaseModel:
    """数据模型基础类"""
    
    def __init__(self, data: Optional[Dict[str, Any]] = None):
        self._data = data or {}
        self._original_data = self._data.copy()
    
    def __getattr__(self, name: str) -> Any:
        """获取属性"""
        if name.startswith('_'):
            return super().__getattribute__(name)
        return self._data.get(name)
    
    def __setattr__(self, name: str, value: Any):
        """设置属性"""
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            self._data[name] = value
    
    def __getitem__(self, key: str) -> Any:
        """字典式访问"""
        return self._data.get(key)
    
    def __setitem__(self, key: str, value: Any):
        """字典式设置"""
        self._data[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取值"""
        return self._data.get(key, default)
    
    def set(self, key: str, value: Any):
        """设置值"""
        self._data[key] = value
    
    def update(self, data: Dict[str, Any]):
        """批量更新数据"""
        self._data.update(data)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return self._data.copy()
    
    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self._data, ensure_ascii=False, default=str)
    
    def is_modified(self) -> bool:
        """检查是否已修改"""
        return self._data != self._original_data
    
    def get_changes(self) -> Dict[str, Any]:
        """获取变更的字段"""
        changes = {}
        for key, value in self._data.items():
            if key not in self._original_data or self._original_data[key] != value:
                changes[key] = value
        return changes
    
    def reset_changes(self):
        """重置变更"""
        self._original_data = self._data.copy()
    
    def validate(self) -> List[str]:
        """验证数据，返回错误列表"""
        return []
    
    def is_valid(self) -> bool:
        """检查数据是否有效"""
        return len(self.validate()) == 0
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseModel':
        """从字典创建实例"""
        return cls(data)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'BaseModel':
        """从JSON字符串创建实例"""
        data = json.loads(json_str)
        return cls(data)
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self._data})"
    
    def __repr__(self) -> str:
        return self.__str__()

class Customer(BaseModel):
    """客户模型"""
    
    def __init__(self, data: Optional[Dict[str, Any]] = None):
        super().__init__(data)
        
        # 设置默认值
        if not self.get('status'):
            self.status = 'LEAD'
        if not self.get('created_at'):
            self.created_at = datetime.now().isoformat()
    
    def validate(self) -> List[str]:
        """验证客户数据"""
        errors = []
        
        if not self.get('company'):
            errors.append("客户名称不能为空")
        
        if not self.get('industry'):
            errors.append("行业类别不能为空")
        
        # 验证状态
        valid_statuses = ['LEAD', 'CONTACTED', 'PROPOSAL', 'NEGOTIATION', 'WON', 'LOST']
        if self.get('status') not in valid_statuses:
            errors.append("客户状态无效")
        
        return errors
    
    @property
    def display_name(self) -> str:
        """显示名称"""
        return self.get('company', '未知客户')
    
    @property
    def is_active(self) -> bool:
        """是否为活跃客户"""
        return self.get('status') not in ['LOST']

class Contact(BaseModel):
    """联系人模型"""
    
    def validate(self) -> List[str]:
        """验证联系人数据"""
        errors = []
        
        if not self.get('name'):
            errors.append("联系人姓名不能为空")
        
        if not self.get('customer_id'):
            errors.append("必须关联客户")
        
        # 验证电话或邮箱至少有一个
        if not self.get('phone') and not self.get('email'):
            errors.append("电话和邮箱至少填写一个")
        
        return errors

class Order(BaseModel):
    """订单模型"""
    
    def __init__(self, data: Optional[Dict[str, Any]] = None):
        super().__init__(data)
        
        # 设置默认值
        if not self.get('status'):
            self.status = 'DRAFT'
        if not self.get('created_at'):
            self.created_at = datetime.now().isoformat()
    
    def validate(self) -> List[str]:
        """验证订单数据"""
        errors = []
        
        if not self.get('customer_id'):
            errors.append("必须关联客户")
        
        if not self.get('total_amount') or float(self.get('total_amount', 0)) <= 0:
            errors.append("订单金额必须大于0")
        
        # 验证状态
        valid_statuses = ['DRAFT', 'PENDING', 'CONFIRMED', 'PROCESSING', 'SHIPPED', 'DELIVERED', 'COMPLETED', 'CANCELLED']
        if self.get('status') not in valid_statuses:
            errors.append("订单状态无效")
        
        return errors
    
    @property
    def display_amount(self) -> str:
        """格式化显示金额"""
        amount = self.get('total_amount', 0)
        return f"¥{float(amount):,.2f}"

class Product(BaseModel):
    """产品模型"""
    
    def validate(self) -> List[str]:
        """验证产品数据"""
        errors = []
        
        if not self.get('name'):
            errors.append("产品名称不能为空")
        
        if not self.get('price') or float(self.get('price', 0)) < 0:
            errors.append("产品价格不能为负数")
        
        return errors
    
    @property
    def display_price(self) -> str:
        """格式化显示价格"""
        price = self.get('price', 0)
        return f"¥{float(price):,.2f}"

class ServiceRecord(BaseModel):
    """服务记录模型"""
    
    def __init__(self, data: Optional[Dict[str, Any]] = None):
        super().__init__(data)
        
        # 设置默认值
        if not self.get('status'):
            self.status = 'OPEN'
        if not self.get('created_at'):
            self.created_at = datetime.now().isoformat()
    
    def validate(self) -> List[str]:
        """验证服务记录数据"""
        errors = []
        
        if not self.get('customer_id'):
            errors.append("必须关联客户")
        
        if not self.get('title'):
            errors.append("服务标题不能为空")
        
        # 验证状态
        valid_statuses = ['OPEN', 'IN_PROGRESS', 'RESOLVED', 'CLOSED']
        if self.get('status') not in valid_statuses:
            errors.append("服务状态无效")
        
        return errors

# 导出所有模型
__all__ = ['BaseModel', 'Customer', 'Contact', 'Order', 'Product', 'ServiceRecord']
