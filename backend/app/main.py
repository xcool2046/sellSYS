from fastapi import FastAPI
from .database import engine, Base
from . import models

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="巨蜂科技客户管理系统 API",
    description="一套完整的客户关系管理（CRM）解决方案",
    version="0.1.0",
)

from .api.api_router import api_router

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to SellSYS API"}