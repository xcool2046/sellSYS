import os
import glob

def file_replace(file_path, replacements):
    """替换文件中的文本"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        original_content = content
        
        for old, new in replacements.items():
            content = content.replace(old, new)
            
        if content != original_content:
            print(f"正在修改文件: {file_path}")
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
    except Exception as e:
        print(f"处理文件时出错 {file_path}: {e}")
    return False

def main():
    """主函数"""
    project_root = '.' 
    total_files_changed = 0
    
    # 定义要进行的替换
    # 规则的顺序很重要，以避免意外的二次替换
    replacements = {
        # 统一 company -> company
        "company": "company",
        
        # 统一 sales_id -> sales_id
        "sales_id": "sales_id",

        # 在 schema 和 endpoint 中，为了清晰起见，将 'name' 重命名为 'owner_name'
        # 注意：这部分需要谨慎，因为它可能会影响不相关的代码。
        # 在这里，我们只做最安全的替换。
        'customer_data[\'sales_name\']': 'customer_data[\'sales_owner_name\']',
        'customer_data[\'service_name\']': 'customer_data[\'service_owner_name\']',
        'schemas.Customer.from_orm(customer).dict()': 'schemas.Customer.from_orm(customer).dict()', # 占位符，无实际作用
        'sales.full_name': 'sales.full_name',
        'service.full_name': 'service.full_name',
    }
    
    # 遍历所有Python文件
    for filepath in glob.glob(os.path.join(project_root, '**', '*.py'), recursive=True):
        if "venv" in filepath or "client_venv" in filepath:
            continue
        if file_replace(filepath, replacements):
            total_files_changed += 1
            
    print(f"\n处理完成！总共修改了 {total_files_changed} 个文件。")

if __name__ == "__main__":
    main()