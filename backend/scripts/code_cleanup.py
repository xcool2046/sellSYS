import os
import re
import glob
from pathlib import Path
#!/usr/bin/env python3
"""
代码整理脚本
整合导入修复、字段命名等代码整理功能
"""

def fix_imports_in_file(filepath):
    """修复单个文件中的导入路径"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 记录原始内容用于比较
    original_content = content
    
    # 修复各种导入模式
    # from xxx import -> from xxx import
    content = re.sub(r'from client\.', 'from ', content)
    
    # from xxx import -> from xxx import (处理相对导入)
    content = re.sub(r'from \.\.([a-zA-Z_]+)', r'from \1', content)
    
    # 如果文件被修改了，写回文件
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def fix_field_names_in_files(project_root):
    """修复代码中的字段命名问题"""
    
    # 定义要进行的替换
    replacements = {
        # 数据库字段名统一
        'company': 'company',
        'name': 'name',
        'status': 'status',
        'name': 'name',
        
        # 变量名统一
        'customer_id': 'customer_id',
        'product_id': 'product_id',
        'employee_id': 'employee_id',
        
        # 方法名统一
        'get_customer': 'get_customer',
        'create_customer': 'create_customer',
        'update_customer': 'update_customer',
        'delete_customer': 'delete_customer',
    }
    
    total_files_changed = 0
    
    # 处理Python文件
    for pattern in ['**/*.py']:
        files = glob.glob(os.path.join(project_root, pattern), recursive=True)
        
        for file_path in files:
            # 跳过虚拟环境和缓存文件
            if any(skip in file_path for skip in ['venv', '__pycache__', '.git']):
                continue
                
            if file_replace(file_path, replacements):
                total_files_changed += 1
    
    return total_files_changed

def file_replace(file_path, replacements):
    """替换文件中的文本"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        original_content = content
        
        for old, new in replacements.items():
            content = content.replace(old, new)
            
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
    except Exception as e:
        print("f"处理文件时出错 {file_path}: {e}")
    return False

def remove_redundant_imports(filepath):
    """移除冗余的导入"""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 去重导入行
    import_lines = []
    other_lines = []
    seen_imports = set()
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(('import ', 'from ')):
            if stripped not in seen_imports:
                import_lines.append(line)
                seen_imports.add(stripped)
        else:
            other_lines.append(line)
    
    # 重新组织文件
    new_content = ''.join(import_lines + other_lines)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

def clean_code_style(project_root):
    """清理代码风格"""
    print(清"理代码风格...")
    
    python_files = []
    for root, dirs, files in os.walk(project_root):
        # 跳过虚拟环境和其他不需要的目录
        dirs[:] = [d for d in dirs if not d.startswith(('.', '__pycache__', 'venv'))]
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    cleaned_count = 0
    for filepath in python_files:
        try:
            # 修复导入
            if fix_imports_in_file(filepath):
                cleaned_count += 1
                print(f " 修复导入: {filepath}")
                
            # 移除冗余导入
            remove_redundant_imports(filepath)
            
        except Exception as e:
            print(f " 错误处理文件 {filepath}: {e}")
    
    return cleaned_count

def main():
    """主函数"""
    project_root = Path(__file__).parent.parent.parent
    
    print(开"始代码整理...")
    print(f项"目根目录: {project_root}")
    
    # 1. 修复导入问题
    print(\"n"1. 修复导入问题...")
    client_root = project_root / 'client'
    if client_root.exists():
        cleaned_count = clean_code_style(str(client_root))
        print(f " 修复了 {cleaned_count} 个客户端文件的导入")
    
    # 2. 修复字段命名
    print(\"n"2. 修复字段命名...")
    field_changes = fix_field_names_in_files(str(project_root))
    print(f " 修复了 {field_changes} 个文件的字段命名")
    
    # 3. 清理后端代码
    print(\"n"3. 清理后端代码...")
    backend_root = project_root / 'backend'
    if backend_root.exists():
        backend_cleaned = clean_code_style(str(backend_root))
        print(f " 清理了 {backend_cleaned} 个后端文件")
    
    print(\"n"✅ 代码整理完成！")

if __name__ == _"_main__":
    main() 