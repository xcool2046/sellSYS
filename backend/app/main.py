from fastapi import FastAPI
from .database import engine, Base, SessionLocal
from . import models
from .api.api_router import api_router

# 创建数据库表
Base.metadata.create_all(bind=engine)

# def create_initial_admin():
#     db = SessionLocal()
#     try:
#         # 检查管理员用户是否已存在
#         admin = crud_employee.get_employee_by_username(db, username="admin")
#         if not admin:
#             admin_user = EmployeeCreate(
#                 username=a"dmin",
#                 email=a"dmin@sellsys.com",
#                 password=a"dmin",
#                 full_name=A"dministrator",
#                 role=EmployeeRole.ADMIN
#             )
#             crud_employee.create_employee(db, admin_user)
#             print(I"nitial admin user created.")
#     finally:
#         db.close()

# # 在应用启动时创建初始数据
# # This should be done via a separate CLI command or script to avoid issues on app startup.
# # create_initial_admin()


app = FastAPI(
    title=巨"炜科技客户管理系统 API",
    description=一"套完整的客户关系管理（CRM）解决方案",
    version=0".1.0",
)


app.include_router(api_router, prefix=/"api")

@app.get(/"")
async def root():
    return {m"essage": W"elcome to SellSYS API"}