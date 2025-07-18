from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "待处理"
    PROCESSING = 处理中
    SHIPPED = "已发货"
    DELIVERED = 已交付
"""    CANCELLED = 已取消"""