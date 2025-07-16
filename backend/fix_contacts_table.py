"""
修复contacts表结构
"""
from sqlalchemy import create_engine, text
from app.config import settings

def fix_contacts_table():
    # 创建数据库引擎
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        try:
            print("开始修复contacts表...")
            
            # 创建新表结构
            conn.execute(text("""
                CREATE TABLE contacts_new (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR NOT NULL,
                    position VARCHAR,
                    phone VARCHAR,
                    email VARCHAR,
                    is_key_person BOOLEAN DEFAULT 0,
                    is_primary BOOLEAN DEFAULT 0,
                    notes TEXT,
                    customer_id INTEGER NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME,
                    FOREIGN KEY(customer_id) REFERENCES customers (id)
                )
            """))
            
            # 复制现有数据，title字段映射到position
            conn.execute(text("""
                INSERT INTO contacts_new (id, name, position, phone, email, notes, customer_id)
                SELECT id, name, title, phone, email, notes, customer_id
                FROM contacts
            """))
            
            # 删除旧表
            conn.execute(text("DROP TABLE contacts"))
            
            # 重命名新表
            conn.execute(text("ALTER TABLE contacts_new RENAME TO contacts"))
            
            conn.commit()
            print("成功修复contacts表结构")
            
        except Exception as e:
            print(f"修复失败: {e}")
            conn.rollback()

if __name__ == "__main__":
    fix_contacts_table()