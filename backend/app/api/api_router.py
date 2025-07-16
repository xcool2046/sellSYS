from fastapi import APIRouter
from .endpoints import (
    auth,
    employees,
    departments,
    department_groups,
    customers,
    contacts,
    products,
    orders,
    sales_follows,
    service_records,
    sales_view
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(employees.router, prefix="/employees", tags=["Employees"])
api_router.include_router(departments.router, prefix="/departments", tags=["Departments"])
api_router.include_router(department_groups.router, prefix="/department-groups", tags=["Department Groups"])
api_router.include_router(customers.router, prefix="/customers", tags=["Customers"])
api_router.include_router(contacts.router, prefix="/contacts", tags=["Contacts"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(orders.router, prefix="/orders", tags=["Orders"])
api_router.include_router(sales_follows.router, prefix="/sales-follows", tags=["SalesFollows"])
api_router.include_router(service_records.router, prefix="/service-records", tags=["ServiceRecords"])
api_router.include_router(sales_view.router, prefix="/sales-view", tags=["Sales View"])