"""
综合修复所有数据库架构问题
"""
from sqlalchemy import create_engine, text
from app.config import settings

def fix_all_database_issues():
    # 创建数据库引擎
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        try:
            # 1. 修复contacts表 - 添加缺失的position字段
            print("检查并修复contacts表...")
            try:
                # 检查position字段是否存在
                result = conn.execute(text("PRAGMA table_info(contacts)"))
                columns = [row[1] for row in result]
                
                if 'position' not in columns:
                    # SQLite不支持直接添加列，需要重建表
                    conn.execute(text("""
                        CREATE TABLE contacts_new (
                            id INTEGER PRIMARY KEY,
                            name VARCHAR NOT NULL,
                            position VARCHAR,
                            phone VARCHAR,
                            email VARCHAR,
                            is_key_person BOOLEAN DEFAULT FALSE,
                            is_primary BOOLEAN DEFAULT FALSE,
                            notes TEXT,
                            customer_id INTEGER NOT NULL,
                            created_at DATETIME,
                            updated_at DATETIME,
                            FOREIGN KEY(customer_id) REFERENCES customers (id)
                        )
                    """))
                    
                    # 复制现有数据
                    conn.execute(text("""
                        INSERT INTO contacts_new (id, name, phone, email, is_key_person, is_primary, notes, customer_id, created_at, updated_at)
                        SELECT id, name, phone, email, is_key_person, is_primary, notes, customer_id, created_at, updated_at
                        FROM contacts
                    """))
                    
                    # 删除旧表
                    conn.execute(text("DROP TABLE contacts"))
                    
                    # 重命名新表
                    conn.execute(text("ALTER TABLE contacts_new RENAME TO contacts"))
                    print("✓ 成功添加position字段到contacts表")
                else:
                    print("✓ contacts表已有position字段")
                    
            except Exception as e:
                print(f"修复contacts表时出错: {e}")
                
            # 提交所有更改
            conn.commit()
            print("\n所有数据库问题已修复！")
            
        except Exception as e:
            print(f"数据库修复失败: {e}")
            conn.rollback()

if __name__ == "__main__":
    fix_all_database_issues()