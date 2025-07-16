from fastapi import FastAPI
from .database import engine, Base, SessionLocal
from . import models
# from .crud import crud_employee  # This import causes circular dependencies and model redefinition.
# from .schemas.employee import EmployeeCreate, EmployeeRole # This should be handled in a separate script.

# 创建数据库表
Base.metadata.create_all(bind=engine)

# def create_initial_admin():
#     db = SessionLocal()
#     try:
#         # 检查管理员用户是否已存在
#         admin = crud_employee.get_employee_by_username(db, username="admin")
#         if not admin:
#             admin_user = EmployeeCreate(
#                 username="admin",
#                 email="admin@sellsys.com",
#                 password="admin",
#                 full_name="Administrator",
#                 role=EmployeeRole.ADMIN
#             )
#             crud_employee.create_employee(db, admin_user)
#             print("Initial admin user created.")
#     finally:
#         db.close()

# # 在应用启动时创建初始数据
# # This should be done via a separate CLI command or script to avoid issues on app startup.
# # create_initial_admin()


app = FastAPI(
    title="巨蜂科技客户管理系统 API",
    description="一套完整的客户关系管理（CRM）解决方案",
    version="0.1.0",
)

from .api.api_router import api_router

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to SellSYS API"}