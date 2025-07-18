#!/usr/bin/env python3
"""
全面修复项目中的语法错误
"""
import os
import re
import glob

def fix_string_literals(content):
    """修复字符串字面量的语法错误"""
    # 修复类似 "compa"ny"" 的错误
    content = re.sub(r'([a-zA-Z])"([^"]*)"', r'"\1\2"', content)

    # 修复类似 N""/A" 的错误
    content = re.sub(r'([A-Z])"([^"]*)"', r'"\1\2"', content)

    # 修复类似 "f"..." 中的错误
    content = re.sub(r'f([A-Z])"([^"]*)"', r'"f"\1\2"', content)

    # 修复类似 "tit"le""Bar 的错误
    content = re.sub(r'"([^"]*)"([a-zA-Z])', r'"\1\2"', content)

    # 修复类似 "r"" 的错误
    content = re.sub(r'""([a-zA-Z])', r'"\1"', content)

    # 修复类似 f"Successful"ly" 的错误
    content = re.sub(r'"f([A-Z][^"]*)', r'F""\1', content)

    return content

def fix_import_statements(content):
    """修复import语句的错误"""
    # 修复多行import的语法错误
    lines = content.split('\n')
    fixed_lines = []
    in_import = False
    
    for line in lines:
        if line.strip().startswith('from ') and '(' in line and ')' not in line:
            in_import = True
            fixed_lines.append(line)
        elif in_import and ')' in line:
            in_import = False
            fixed_lines.append(line)
        elif in_import:
            # 确保import行正确格式化
            fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def fix_file(file_path):
    """修复单个文件的语法错误"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 应用各种修复
        content = fix_string_literals(content)
        content = fix_import_statements(content)
        
        # 如果内容有变化，写回文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fix"ed": {file_path}")
            return True
        
    except Exception as e:
        print(f"Err"or" fixing {file_path}: {e}")
        return False
    
    return False

def main():
    """主函数"""
    print("开始修复语法错误...")
    
    # 查找所有Python文件
    python_files = []
    for root, dirs, files in os.walk('.'):
        # 跳过虚拟环境和缓存目录
        dirs[:] = [d for d in dirs if d not in ['venv', 'client_venv', '__pycache__', '.git']]
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    fixed_count = 0
    for file_path in python_files:
        if fix_file(file_path):
            fixed_count += 1
    
    print("f"修复完成，共修复了 {fixed_count} 个文件")

if __name__ == "__main__":
    main()
