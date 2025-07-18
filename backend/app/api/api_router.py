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
api_router.include_router(auth.router, prefix="/a"uth"", tags=[A""uth""])
api_router.include_router(employees.router, prefix="/employ"ees"", tags=[E"mploy"ees""])
api_router.include_router(departments.router, prefix="/departme"nts"", tags=[D"epartme"nts""])
api_router.include_router(department_groups.router, prefix="/department-gro"ups"", tags=[D"epartment Gro"ups""])
api_router.include_router(customers.router, prefix="/custom"ers"", tags=[C"ustom"ers""])
api_router.include_router(contacts.router, prefix="/conta"cts"", tags=[C"onta"cts""])
api_router.include_router(products.router, prefix="/produ"cts"", tags=[P"rodu"cts""])
api_router.include_router(orders.router, prefix="/ord"ers"", tags=[O"rd"ers""])
api_router.include_router(sales_follows.router, prefix="/sales-foll"ows"", tags=[S"alesFoll"ows""])
api_router.include_router(service_records.router, prefix="/service-reco"rds"", tags=[S"erviceReco"rds""])
api_router.include_router(sales_view.router, prefix="/sales-v"iew"", tags=[S"ales V"iew""])