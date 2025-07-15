from fastapi import APIRouter
from .endpoints import auth, employees, customers, contacts, products, orders, sales_follows, service_records

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(employees.router, prefix="/employees", tags=["Employees"])
api_router.include_router(customers.router, prefix="/customers", tags=["Customers"])
api_router.include_router(contacts.router, tags=["Contacts"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(orders.router, prefix="/orders", tags=["Orders"])
api_router.include_router(sales_follows.router, prefix="/sales-follows", tags=["SalesFollows"])
api_router.include_router(service_records.router, prefix="/service-records", tags=["ServiceRecords"])