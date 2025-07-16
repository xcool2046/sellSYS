import sqlite3
import os

# 数据库路径
db_path = os.path.join(os.path.dirname(__file__), 'sellsys.db')

# 连接到数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # 检查表结构
    cursor.execute("PRAGMA table_info(products)")
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]
    
    print("当前产品表字段:", column_names)
    
    # 添加新字段（如果不存在）
    if 'code' not in column_names:
        cursor.execute("ALTER TABLE products ADD COLUMN code VARCHAR")
        print("添加字段: code")
    
    if 'supplier_price' not in column_names:
        cursor.execute("ALTER TABLE products ADD COLUMN supplier_price NUMERIC(10, 2)")
        print("添加字段: supplier_price")
    
    if 'price' not in column_names:
        cursor.execute("ALTER TABLE products ADD COLUMN price NUMERIC(10, 2)")
        print("添加字段: price")
    
    if 'commission' not in column_names:
        cursor.execute("ALTER TABLE products ADD COLUMN commission NUMERIC(10, 2)")
        print("添加字段: commission")
    
    # 提交更改
    conn.commit()
    print("\n数据库迁移成功！")
    
    # 再次检查表结构
    cursor.execute("PRAGMA table_info(products)")
    columns = cursor.fetchall()
    print("\n更新后的产品表字段:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
    
except Exception as e:
    print(f"迁移失败: {e}")
    conn.rollback()
finally:
    conn.close()