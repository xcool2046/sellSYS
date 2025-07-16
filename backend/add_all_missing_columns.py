import sys
sys.path.append('.')

from sqlalchemy import create_engine, text
from app.config import settings

engine = create_engine(settings.DATABASE_URL)

print("添加所有缺失的列...")

try:
    with engine.connect() as conn:
        # 添加customers表缺失的列
        print("\n检查customers表...")
        result = conn.execute(text("PRAGMA table_info(customers)"))
        customer_columns = [row[1] for row in result]
        
        customer_columns_to_add = {
            'company': 'VARCHAR',
            'company_name': 'VARCHAR',
            'industry': 'VARCHAR',
            'updated_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
        }
        
        for col_name, col_type in customer_columns_to_add.items():
            if col_name not in customer_columns:
                conn.execute(text(f"ALTER TABLE customers ADD COLUMN {col_name} {col_type}"))
                print(f"  成功添加customers.{col_name}列")
            else:
                print(f"  customers.{col_name}列已存在")
        
        # 添加service_records表缺失的列
        print("\n检查service_records表...")
        result = conn.execute(text("PRAGMA table_info(service_records)"))
        service_columns = [row[1] for row in result]
        
        service_columns_to_add = {
            'order_id': 'INTEGER',
            'contact_id': 'INTEGER',
            'title': 'VARCHAR',
            'feedback': 'TEXT',
            'response': 'TEXT',
            'status': 'VARCHAR',
            'created_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
            'closed_at': 'TIMESTAMP'
        }
        
        for col_name, col_type in service_columns_to_add.items():
            if col_name not in service_columns:
                conn.execute(text(f"ALTER TABLE service_records ADD COLUMN {col_name} {col_type}"))
                print(f"  成功添加service_records.{col_name}列")
            else:
                print(f"  service_records.{col_name}列已存在")
                
        # 添加products表缺失的列
        print("\n检查products表...")
        result = conn.execute(text("PRAGMA table_info(products)"))
        product_columns = [row[1] for row in result]
        
        product_columns_to_add = {
            'supplier_price': 'DECIMAL(10, 2)',
            'price': 'DECIMAL(10, 2)',
            'description': 'TEXT',
            'type': 'VARCHAR',
            'created_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
            'updated_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
        }
        
        for col_name, col_type in product_columns_to_add.items():
            if col_name not in product_columns:
                conn.execute(text(f"ALTER TABLE products ADD COLUMN {col_name} {col_type}"))
                print(f"  成功添加products.{col_name}列")
            else:
                print(f"  products.{col_name}列已存在")
        
        # 添加departments表缺失的列
        print("\n检查departments表...")
        result = conn.execute(text("PRAGMA table_info(departments)"))
        dept_columns = [row[1] for row in result] if result else []
        
        if not dept_columns:
            # 如果表不存在，创建它
            conn.execute(text("""
                CREATE TABLE departments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            print("  成功创建departments表")
        
        # 添加department_groups表缺失的列
        print("\n检查department_groups表...")
        result = conn.execute(text("PRAGMA table_info(department_groups)"))
        group_columns = [row[1] for row in result] if result else []
        
        if not group_columns:
            # 如果表不存在，创建它
            conn.execute(text("""
                CREATE TABLE department_groups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR NOT NULL,
                    department_id INTEGER,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (department_id) REFERENCES departments(id)
                )
            """))
            print("  成功创建department_groups表")
            
        # 添加contacts表缺失的列
        print("\n检查contacts表...")
        result = conn.execute(text("PRAGMA table_info(contacts)"))
        contact_columns = [row[1] for row in result] if result else []
        
        if not contact_columns:
            # 如果表不存在，创建它
            conn.execute(text("""
                CREATE TABLE contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER,
                    name VARCHAR,
                    position VARCHAR,
                    phone VARCHAR,
                    email VARCHAR,
                    is_primary BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (customer_id) REFERENCES customers(id)
                )
            """))
            print("  成功创建contacts表")
            
        # 添加sales_follows表缺失的列
        print("\n检查sales_follows表...")
        result = conn.execute(text("PRAGMA table_info(sales_follows)"))
        follow_columns = [row[1] for row in result] if result else []
        
        if not follow_columns:
            # 如果表不存在，创建它
            conn.execute(text("""
                CREATE TABLE sales_follows (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER,
                    employee_id INTEGER,
                    follow_date TIMESTAMP,
                    next_follow_date TIMESTAMP,
                    intention_level VARCHAR,
                    content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (customer_id) REFERENCES customers(id),
                    FOREIGN KEY (employee_id) REFERENCES employees(id)
                )
            """))
            print("  成功创建sales_follows表")
        
        conn.commit()
        print("\n所有表和列更新完成！")
            
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()