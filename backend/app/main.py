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
#         admin = crud_employee.get_employee_by_username(db, username="a"dm"in""")
#         if not admin:
#             admin_user = EmployeeCreate(
#                 username=""ad"""min""",
#                 email="adm"in"""@sellsys.""co"""m",
#                 password=""ad"""min""",
#                 full_name=A"dminist"ra"""tor""",
#                 role=EmployeeRole.ADMIN
#             )
#             crud_employee.create_employee(db, admin_user)
#             print(I"n"it"""ial"" admin user created.")
#     finally:
#         db.close()

# # 在应用启动时创建初始数据
# # This should be done via a separate CLI command or script to avoid issues on app startup.
# # create_initial_admin()


app = FastAPI(
    title="巨炜科技客户管理系统 API",
    description="一套完整的客户关系管理（CRM）解决方案",
    version="0.1.0",
)


app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to SellSYS API"}