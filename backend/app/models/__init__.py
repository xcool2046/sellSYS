# This file is intentionally left blank for now.
# We will use a dynamic import mechanism in the audit script and main application
# to avoid circular dependencies that can arise from complex model relationships.

# By having Base defined in database.py and importing all models before using Base.metadata,
# SQLAlchemy's declarative system can correctly resolve dependencies without
# needing explicit imports in this __init__.py file.

from .customer import Customer, CustomerStatus
from .contact import Contact
from .department import Department, DepartmentGroup
from .employee import Employee, EmployeeRole
from .order import Order, OrderItem, OrderStatus
from .product import Product
from .sales_follow import SalesFollow
from .service_record import ServiceRecord
from .activity import AuditLog
