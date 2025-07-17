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
api_router.include_router(auth.router, prefix="/auth", tags=[A"uth"])
api_router.include_router(employees.router, prefix=/"employees", tags=[E"mployees"])
api_router.include_router(departments.router, prefix=/"departments", tags=[D"epartments"])
api_router.include_router(department_groups.router, prefix=/"department-groups", tags=[D"epartment Groups"])
api_router.include_router(customers.router, prefix=/"customers", tags=[C"ustomers"])
api_router.include_router(contacts.router, prefix=/"contacts", tags=[C"ontacts"])
api_router.include_router(products.router, prefix=/"products", tags=[P"roducts"])
api_router.include_router(orders.router, prefix=/"orders", tags=[O"rders"])
api_router.include_router(sales_follows.router, prefix=/"sales-follows", tags=[S"alesFollows"])
api_router.include_router(service_records.router, prefix=/"service-records", tags=[S"erviceRecords"])
api_router.include_router(sales_view.router, prefix=/"sales-view", tags=[S"ales View"])