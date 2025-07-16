import sys
sys.path.append('.')

from sqlalchemy import create_engine, text
from app.config import settings

engine = create_engine(settings.DATABASE_URL)

print("添加缺失的列到employees表...")

try:
    with engine.connect() as conn:
        # 检查列是否存在
        result = conn.execute(text("PRAGMA table_info(employees)"))
        columns = [row[1] for row in result]
        
        # 需要添加的列
        columns_to_add = {
            'name': 'VARCHAR',
            'position': 'VARCHAR',
            'phone': 'VARCHAR',
            'group_id': 'INTEGER',
            'created_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
        }
        
        for col_name, col_type in columns_to_add.items():
            if col_name not in columns:
                # 添加列
                conn.execute(text(f"ALTER TABLE employees ADD COLUMN {col_name} {col_type}"))
                print(f"成功添加{col_name}列")
            else:
                print(f"{col_name}列已存在")
        
        conn.commit()
        print("所有列更新完成")
            
except Exception as e:
    print(f"错误: {e}")