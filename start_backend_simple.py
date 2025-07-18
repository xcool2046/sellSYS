#!/usr/bin/env python3
"""
简单的后端启动脚本
"""
import os
import sys
import subprocess
from pathlib import Path

def check_backend_files():
    """检查后端文件是否存在"""
    backend_dir = Path("backend")
    required_files = [
        "backend/app/main.py",
        "backend/app/__init__.py",
        "backend/app/models/__init__.py",
        "backend/app/models/customer.py"
    ]
    
    print("🔍 检查后端文件...")
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - 文件不存在")
    
    return all(Path(f).exists() for f in required_files)

def check_python_environment():
    """检查Python环境"""
    print("\n🐍 检查Python环境...")
    print(f"Python版本: {sys.version}")
    
    # 检查必要的包
    required_packages = ["fastapi", "uvicorn", "sqlalchemy", "pydantic"]
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - 未安装")
            missing_packages.append(package)
    
    return len(missing_packages) == 0, missing_packages

def create_simple_backend():
    """创建一个简单的后端服务"""
    backend_code = '''
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
import uuid
from datetime import datetime

app = FastAPI(title="SellSYS API", version="1.0.0")

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

class Customer(BaseModel):
    id: str
    industry: str
    company: str
    province: Optional[str] = ""
    city: Optional[str] = ""
    address: Optional[str] = ""
    notes: Optional[str] = ""
    status: str = "LEAD"
    contacts: List[Dict[str, Any]] = []
    created_at: str
    updated_at: str

@app.get("/")
async def root():
    return {"message": "SellSYS API is running", "version": "1.0.0"}

@app.get("/api/customers/")
async def get_customers():
    """获取所有客户"""
    return customers_db

@app.post("/api/customers/")
async def create_customer(customer: CustomerCreate):
    """创建新客户"""
    try:
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
        print(f"[API] 创建客户成功: {new_customer['company']}")
        return new_customer
        
    except Exception as e:
        print(f"[API] 创建客户失败: {str(e)}")
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
            return updated_customer
    raise HTTPException(status_code=404, detail="Customer not found")

@app.delete("/api/customers/{customer_id}")
async def delete_customer(customer_id: str):
    """删除客户"""
    for i, customer in enumerate(customers_db):
        if customer["id"] == customer_id:
            deleted_customer = customers_db.pop(i)
            return {"message": "Customer deleted", "customer": deleted_customer}
    raise HTTPException(status_code=404, detail="Customer not found")

if __name__ == "__main__":
    import uvicorn
    print("🚀 启动简单后端服务...")
    print("📍 API地址: http://127.0.0.1:8000")
    print("📖 API文档: http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
'''
    
    # 创建后端目录
    os.makedirs("backend_simple", exist_ok=True)
    
    # 写入后端代码
    with open("backend_simple/main.py", "w", encoding="utf-8") as f:
        f.write(backend_code)
    
    print("✅ 简单后端服务创建完成")
    return "backend_simple/main.py"

def main():
    """主函数"""
    print("🔧 SellSYS 后端启动工具")
    print("=" * 50)
    
    # 检查后端文件
    if check_backend_files():
        print("\n✅ 后端文件检查通过")
        backend_path = "backend/app/main.py"
    else:
        print("\n⚠️ 原始后端文件缺失，创建简单后端服务...")
        backend_path = create_simple_backend()
    
    # 检查Python环境
    env_ok, missing = check_python_environment()
    if not env_ok:
        print(f"\n❌ 缺少必要的Python包: {', '.join(missing)}")
        print("请运行以下命令安装:")
        print(f"pip install {' '.join(missing)}")
        return
    
    print("\n🚀 启动后端服务...")
    print("按 Ctrl+C 停止服务")
    print("=" * 50)
    
    try:
        # 启动后端服务
        if "backend_simple" in backend_path:
            subprocess.run([sys.executable, backend_path], cwd=".")
        else:
            subprocess.run([sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"], cwd="backend")
    except KeyboardInterrupt:
        print("\n\n🛑 后端服务已停止")
    except Exception as e:
        print(f"\n❌ 启动后端服务失败: {str(e)}")

if __name__ == "__main__":
    main()
