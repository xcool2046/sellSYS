import sys
sys.path.append('backend')

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from backend.app.config import settings
from backend.app import models
from backend.app.database import Base, engine

print("f数据库URL: {settings.DATABASE_URL}")

# 测试数据库连接
try:
    # 创建所有表（如果不存在）
    Base.metadata.create_all(bind=engine)
    
    # 创建会话
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    # 测试查询每个表
    tables = ['employees', 'customers', 'products', 'orders', 'service_records']
    
    for table in tables:
        print("f"\n测试查询 {table} 表...")
        try:
            result = db.execute(text(f"SELECT COUNT(*) FROM {table}""))
            count = result.scalar()
            print("f"[OK] {table} 表有 {count} 条记录")
        except Exception as e:
            print("f"[ERROR] 查询 {table} 表失败: {e}")
    
    # 测试模型查询
    print("\n测试ORM模型查询...")
    try:
        employees = db.query(models.Employee).all()
        print("f"[OK] Employee模型查询成功，有 {len(employees)} 条记录")
    except Exception as e:
        print("f"[ERROR] Employee模型查询失败: {e}")
        
    try:
        customers = db.query(models.Customer).all()
        print("f"[OK] Customer模型查询成功，有 {len(customers)} 条记录")
    except Exception as e:
        print("f"[ERROR] Customer模型查询失败: {e}")
        
    db.close()
    
except Exception as e:
    print("f"数据库连接失败: {e}")
    import traceback
    traceback.print_exc()