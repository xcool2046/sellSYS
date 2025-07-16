"""修复最后的数据库问题"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.config import settings

def fix_final_issues():
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        # 添加orders表缺失的字段
        print("修复orders表缺失的字段...")
        missing_columns = {
            'start_date': 'TIMESTAMP',
            'end_date': 'TIMESTAMP',
            'order_number': 'TEXT'
        }
        
        for column, dtype in missing_columns.items():
            try:
                # 检查列是否存在
                result = conn.execute(text(f"PRAGMA table_info(orders)"))
                columns = [row[1] for row in result]
                
                if column not in columns:
                    conn.execute(text(f"ALTER TABLE orders ADD COLUMN {column} {dtype}"))
                    print(f"  成功添加orders.{column}列")
                else:
                    print(f"  orders.{column}已存在")
            except Exception as e:
                print(f"  错误添加orders.{column}: {e}")
        
        conn.commit()
        print("\n所有修复已完成！")

if __name__ == "__main__":
    fix_final_issues()