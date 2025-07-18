#!/usr/bin/env python3
"""
简单的后端API服务 - 用于测试客户添加功能
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime

app = FastAPI(title="SellSYS Simple API", version="1.0.0")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 内存存储（临时解决方案）
customers_db = []

class ContactCreate(BaseModel):
    name: str
    phone: str
    is_primary: bool = False

class CustomerCreate(BaseModel):
    industry: str
    company: str
    province: Optional[str] = ""
    city: Optional[str] = ""
    address: Optional[str] = ""
    notes: Optional[str] = ""
    status: Optional[str] = "LEAD"
    contacts: List[ContactCreate] = []

@app.get("/")
async def root():
    return {"message": "SellSYS Simple API is running", "version": "1.0.0"}

@app.get("/api/customers/")
async def get_customers():
    """获取所有客户"""
    print(f"[API] 获取客户列表，当前客户数量: {len(customers_db)}")
    return customers_db

@app.post("/api/customers/")
async def create_customer(customer: CustomerCreate):
    """创建新客户"""
    try:
        print(f"[API] 收到创建客户请求: {customer.dict()}")
        
        # 创建新客户
        new_customer = {
            "id": str(uuid.uuid4()),
            "industry": customer.industry,
            "company": customer.company,
            "province": customer.province or "",
            "city": customer.city or "",
            "address": customer.address or "",
            "notes": customer.notes or "",
            "status": customer.status or "LEAD",
            "contacts": [contact.dict() for contact in customer.contacts],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        customers_db.append(new_customer)
        print(f"[API] ✅ 客户创建成功: {new_customer['company']} (ID: {new_customer['id']})")
        print(f"[API] 当前客户总数: {len(customers_db)}")
        
        return new_customer
        
    except Exception as e:
        print(f"[API] ❌ 创建客户失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/customers/{customer_id}")
async def get_customer(customer_id: str):
    """获取单个客户"""
    for customer in customers_db:
        if customer["id"] == customer_id:
            return customer
    raise HTTPException(status_code=404, detail="Customer not found")

@app.put("/api/customers/{customer_id}")
async def update_customer(customer_id: str, customer: CustomerCreate):
    """更新客户"""
    for i, existing_customer in enumerate(customers_db):
        if existing_customer["id"] == customer_id:
            updated_customer = {
                **existing_customer,
                "industry": customer.industry,
                "company": customer.company,
                "province": customer.province or "",
                "city": customer.city or "",
                "address": customer.address or "",
                "notes": customer.notes or "",
                "status": customer.status or "LEAD",
                "contacts": [contact.dict() for contact in customer.contacts],
                "updated_at": datetime.now().isoformat()
            }
            customers_db[i] = updated_customer
            print(f"[API] ✅ 客户更新成功: {updated_customer['company']}")
            return updated_customer
    raise HTTPException(status_code=404, detail="Customer not found")

@app.delete("/api/customers/{customer_id}")
async def delete_customer(customer_id: str):
    """删除客户"""
    for i, customer in enumerate(customers_db):
        if customer["id"] == customer_id:
            deleted_customer = customers_db.pop(i)
            print(f"[API] ✅ 客户删除成功: {deleted_customer['company']}")
            return {"message": "Customer deleted", "customer": deleted_customer}
    raise HTTPException(status_code=404, detail="Customer not found")

if __name__ == "__main__":
    import uvicorn
    print("🚀 启动简单后端API服务...")
    print("📍 API地址: http://127.0.0.1:8000")
    print("📖 API文档: http://127.0.0.1:8000/docs")
    print("🔧 这是一个临时的内存数据库，重启后数据会丢失")
    print("=" * 60)
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
