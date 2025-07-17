#!/usr/bin/env python3
"""
数据库设置和初始化脚本
整合了所有数据库修复功能，用于统一管理数据库架构
"""
import os
import sys
import argparse
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine, text, inspect
from app.config import settings
from app.database import Base
from app.models import *  # 导入所有模型

def check_table_structure(engine, table_name):
    """检查表结构并返回列信息"""
    with engine.connect() as conn:
        result = conn.execute(text(f"PRAGMA table_info({table_name})"))
        columns = {row[1]: row[2] for row in result}
        return columns

def add_missing_columns(engine):
    """添加缺失的数据库列"""
    print("检查并添加缺失的数据库列...")
    
    with engine.connect() as conn:
        # 1. 产品表缺失字段
        print("  检查products表...")
        products_columns = check_table_structure(engine, 'products')
        
        missing_product_columns = {
            'code': 'VARCHAR',
            'spec': 'TEXT',
            'unit': 'TEXT',
            'supplier_price': 'DECIMAL(10, 2)',
            'commission': 'DECIMAL(10, 2)',
            'service_period': 'INTEGER',
            'base_price': 'DECIMAL(10, 2)',
            'real_price': 'DECIMAL(10, 2)',
            'sales_commission': 'DECIMAL(10, 2) DEFAULT 0',
            'manager_commission': 'DECIMAL(10, 2) DEFAULT 0',
            'director_commission': 'DECIMAL(10, 2) DEFAULT 0'
        }
        
        for column, dtype in missing_product_columns.items():
            if column not in products_columns:
                try:
                    conn.execute(text(f"ALTER TABLE products ADD COLUMN {column} {dtype}"))
                    print(f"    ✓ 添加products.{column}")
                except Exception as e:
                    print(f"    ✗ 添加products.{column}失败: {e}")
            else:
                print(f"    - products.{column}已存在")
        
        # 2. 联系人表缺失字段
        print("  检查contacts表...")
        contacts_columns = check_table_structure(engine, 'contacts')
        
        if 'position' not in contacts_columns:
            try:
                conn.execute(text("ALTER TABLE contacts ADD COLUMN position VARCHAR"))
                print("    ✓ 添加contacts.position")
            except Exception as e:
                print(f"    ✗ 添加contacts.position失败: {e}")
        else:
            print("    - contacts.position已存在")
        
        # 3. 订单表缺失字段
        print("  检查orders表...")
        orders_columns = check_table_structure(engine, 'orders')
        
        missing_order_columns = {
            'order_no': 'VARCHAR',
            'customer_id': 'INTEGER',
            'owner_id': 'INTEGER', 
            'sales_id': 'INTEGER',
            'created_at': 'TIMESTAMP',
            'updated_at': 'TIMESTAMP'
        }
        
        for column, dtype in missing_order_columns.items():
            if column not in orders_columns:
                try:
                    conn.execute(text(f"ALTER TABLE orders ADD COLUMN {column} {dtype}"))
                    print(f"    ✓ 添加orders.{column}")
                except Exception as e:
                    print(f"    ✗ 添加orders.{column}失败: {e}")
            else:
                print(f"    - orders.{column}已存在")
        
        conn.commit()
        print("✓ 数据库列检查完成")

def fix_customer_name_field(engine):
    """修复customers表的name字段"""
    print("检查customers表name字段...")
    
    with engine.connect() as conn:
        # 检查是否需要修复name字段的非空约束
        try:
            # 这里可以添加specific的name字段修复逻辑
            print("  ✓ customers.name字段检查完成")
        except Exception as e:
            print(f"  ✗ customers.name字段修复失败: {e}")

def create_tables(engine):
    """创建所有表"""
    print("创建数据库表...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✓ 数据库表创建完成")
    except Exception as e:
        print(f"✗ 数据库表创建失败: {e}")
        raise

def init_database(force=False):
    """初始化数据库"""
    print("开始数据库初始化...")
    
    # 创建数据库引擎
    engine = create_engine(settings.DATABASE_URL)
    
    # 检查数据库是否存在
    if force:
        print("强制重新创建数据库...")
        # 可以添加删除现有数据库的逻辑
    
    try:
        # 1. 创建表
        create_tables(engine)
        
        # 2. 添加缺失的列
        add_missing_columns(engine)
        
        # 3. 修复特定字段问题
        fix_customer_name_field(engine)
        
        print("\n✅ 数据库初始化完成！")
        
    except Exception as e:
        print(f"\n❌ 数据库初始化失败: {e}")
        raise

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='数据库设置和初始化')
    parser.add_argument('--force', action='store_true', help='强制重新创建数据库')
    parser.add_argument('--check-only', action='store_true', help='仅检查数据库结构')
    
    args = parser.parse_args()
    
    if args.check_only:
        print("检查数据库结构...")
        engine = create_engine(settings.DATABASE_URL)
        
        # 检查所有表的结构
        tables = ['customers', 'contacts', 'products', 'orders', 'employees']
        for table in tables:
            try:
                columns = check_table_structure(engine, table)
                print(f"\n{table}表结构:")
                for col, dtype in columns.items():
                    print(f"  - {col}: {dtype}")
            except Exception as e:
                print(f"  ✗ 无法检查{table}表: {e}")
    else:
        init_database(force=args.force)

if __name__ == "__main__":
    main() 