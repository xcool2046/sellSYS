#!/usr/bin/env python3
"""
批量修复客户端代码中的语法问题
"""
import os
import re
import glob

def fix_string_literals(content):
    """修复字符串字面量问题"""
    # 修复 "f"字符串 -> f"字符串"
    content = re.sub(r'"f"([^"]*)"', r'f"\1"', content)
    
    # 修复分割的字符串如 "hello""world" -> "helloworld"
    content = re.sub(r'"([^"]*)"([^"]*)"([^"]*)"', r'"\1\2\3"', content)
    
    # 修复更复杂的分割字符串
    content = re.sub(r'"([^"]*)"([^"]*)"', r'"\1\2"', content)
    
    return content

def fix_import_statements(content, file_path):
    """修复导入语句"""
    # 如果是在client目录下的文件
    if 'client' in file_path:
        # 修复相对导入为绝对导入
        content = re.sub(r'from \.\.api import', 'from api import', content)
        content = re.sub(r'from \.\.config import', 'from config import', content)
        content = re.sub(r'from \.api import', 'from api import', content)
        content = re.sub(r'from \.config import', 'from config import', content)
    
    return content

def fix_object_names(content):
    """修复对象名称中的语法错误"""
    # 修复setObjectName中的错误
    content = re.sub(r'setObjectName\([^)]*"([^"]*)"[^)]*"([^"]*)"[^)]*\)', r'setObjectName("\1\2")', content)
    
    return content

def fix_file(file_path):
    """修复单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 应用各种修复
        content = fix_string_literals(content)
        content = fix_import_statements(content, file_path)
        content = fix_object_names(content)
        
        # 只有内容发生变化时才写入
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"已修复: {file_path}")
            return True
        else:
            print(f"无需修复: {file_path}")
            return False
            
    except Exception as e:
        print(f"修复文件 {file_path} 时出错: {e}")
        return False

def main():
    """主函数"""
    print("开始批量修复语法问题...")
    
    # 查找所有Python文件
    python_files = []
    for root, dirs, files in os.walk('client'):
        # 跳过__pycache__目录
        dirs[:] = [d for d in dirs if d != '__pycache__']
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    fixed_count = 0
    total_count = len(python_files)
    
    for file_path in python_files:
        if fix_file(file_path):
            fixed_count += 1
    
    print(f"\n修复完成！")
    print(f"总文件数: {total_count}")
    print(f"已修复文件数: {fixed_count}")
    print(f"无需修复文件数: {total_count - fixed_count}")

if __name__ == "__main__":
    main()
