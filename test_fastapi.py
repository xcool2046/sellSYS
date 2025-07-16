import sys
sys.path.append('backend')

from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database import SessionLocal, engine
from backend.app import models

# 创建测试客户端
client = TestClient(app)

print("测试FastAPI应用...")

# 测试根路径
print("\n1. 测试根路径 /")
try:
    response = client.get("/")
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
except Exception as e:
    print(f"   [ERROR] {e}")

# 测试员工列表
print("\n2. 测试 GET /api/employees")
try:
    response = client.get("/api/employees")
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"   员工数量: {len(response.json())}")
    else:
        print(f"   错误: {response.text}")
except Exception as e:
    print(f"   [ERROR] {e}")

# 测试客户列表
print("\n3. 测试 GET /api/customers")
try:
    response = client.get("/api/customers")
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"   客户数量: {len(response.json())}")
    else:
        print(f"   错误: {response.text}")
except Exception as e:
    print(f"   [ERROR] {e}")

# 测试产品列表
print("\n4. 测试 GET /api/products")
try:
    response = client.get("/api/products")
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"   产品数量: {len(response.json())}")
    else:
        print(f"   错误: {response.text}")
except Exception as e:
    print(f"   [ERROR] {e}")

# 检查是否有初始数据
print("\n5. 检查初始数据...")
db = SessionLocal()
try:
    # 检查是否有管理员
    admin = db.query(models.Employee).filter(models.Employee.username == "admin").first()
    if admin:
        print(f"   [OK] 找到管理员账号: {admin.username}")
    else:
        print(f"   [WARNING] 没有找到管理员账号")
        
    # 检查部门
    dept_count = db.query(models.Department).count()
    print(f"   部门数量: {dept_count}")
    
    # 检查部门分组
    group_count = db.query(models.DepartmentGroup).count()
    print(f"   部门分组数量: {group_count}")
    
except Exception as e:
    print(f"   [ERROR] 查询数据库时出错: {e}")
finally:
    db.close()

print("\n测试完成。")