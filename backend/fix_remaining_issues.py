"""修复剩余的数据库问题"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.config import settings
from app.database import Base
from app.models import *

def fix_database():
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        # 1. 添加产品表缺失的字段
        print("检查products表缺失的字段...")
        missing_columns = {
            'spec': 'TEXT',
            'unit': 'TEXT',
            'commission': 'DECIMAL(10, 2)',
            'service_period': 'INTEGER',
            'base_price': 'DECIMAL(10, 2)',
            'real_price': 'DECIMAL(10, 2)',
            'sales_commission': 'DECIMAL(10, 2) DEFAULT 0',
            'manager_commission': 'DECIMAL(10, 2) DEFAULT 0',
            'director_commission': 'DECIMAL(10, 2) DEFAULT 0'
        }
        
        for column, dtype in missing_columns.items():
            try:
                # 检查列是否存在
                result = conn.execute(text(f"PRAGMA table_info(products)"))
                columns = [row[1] for row in result]
                
                if column not in columns:
                    conn.execute(text(f"ALTER TABLE products ADD COLUMN {column} {dtype}"))
                    print(f"  成功添加products.{column}列")
                else:
                    print(f"  products.{column}已存在")
            except Exception as e:
                print(f"  错误添加products.{column}: {e}")
        
        # 2. 检查并添加orders表缺失的字段
        print("\n检查orders表缺失的字段...")
        orders_columns = {
            'customer_id': 'INTEGER',
            'owner_id': 'INTEGER',
            'sales_id': 'INTEGER',
            'order_no': 'TEXT',
            'created_at': 'TIMESTAMP',
            'updated_at': 'TIMESTAMP',
            'status': 'TEXT',
            'total_amount': 'DECIMAL(10, 2)',
            'profit': 'DECIMAL(10, 2)',
            'contract_date': 'DATE'
        }
        
        for column, dtype in orders_columns.items():
            try:
                result = conn.execute(text(f"PRAGMA table_info(orders)"))
                columns = [row[1] for row in result]
                
                if column not in columns:
                    conn.execute(text(f"ALTER TABLE orders ADD COLUMN {column} {dtype}"))
                    print(f"  成功添加orders.{column}列")
                else:
                    print(f"  orders.{column}已存在")
            except Exception as e:
                print(f"  错误添加orders.{column}: {e}")
        
        # 3. 检查并添加order_items表
        print("\n检查order_items表...")
        try:
            conn.execute(text("SELECT 1 FROM order_items LIMIT 1"))
            print("  order_items表已存在")
        except:
            print("  创建order_items表...")
            conn.execute(text("""
                CREATE TABLE order_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL DEFAULT 1,
                    unit_price DECIMAL(10, 2) NOT NULL,
                    total_price DECIMAL(10, 2) NOT NULL,
                    commission DECIMAL(10, 2),
                    FOREIGN KEY (order_id) REFERENCES orders(id),
                    FOREIGN KEY (product_id) REFERENCES products(id)
                )
            """))
            print("  成功创建order_items表")
        
        conn.commit()
        print("\n所有修复已完成！")

if __name__ == "__main__":
    fix_database()