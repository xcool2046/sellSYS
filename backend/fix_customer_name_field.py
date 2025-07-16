"""
修复customers表中的name字段问题
将name字段设置为可空，因为实际使用的是company字段
"""
from sqlalchemy import create_engine, text
from app.config import settings

def fix_customer_name_field():
    # 创建数据库引擎
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        try:
            # 由于SQLite不支持ALTER COLUMN，我们需要重建表
            # 1. 创建新表
            conn.execute(text("""
                CREATE TABLE customers_new (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR,
                    company VARCHAR,
                    company_name VARCHAR,
                    industry VARCHAR,
                    province VARCHAR,
                    city VARCHAR,
                    address VARCHAR,
                    website VARCHAR,
                    scale VARCHAR,
                    status VARCHAR(9) NOT NULL,
                    sales_owner_id INTEGER,
                    service_owner_id INTEGER,
                    created_at DATETIME,
                    updated_at DATETIME,
                    FOREIGN KEY(sales_owner_id) REFERENCES employees (id),
                    FOREIGN KEY(service_owner_id) REFERENCES employees (id)
                )
            """))
            
            # 2. 复制数据
            conn.execute(text("""
                INSERT INTO customers_new 
                SELECT * FROM customers
            """))
            
            # 3. 删除旧表
            conn.execute(text("DROP TABLE customers"))
            
            # 4. 重命名新表
            conn.execute(text("ALTER TABLE customers_new RENAME TO customers"))
            
            conn.commit()
            print("成功修复customers表的name字段")
            
        except Exception as e:
            print(f"修复失败: {e}")
            conn.rollback()

if __name__ == "__main__":
    fix_customer_name_field()