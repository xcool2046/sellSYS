#!/usr/bin/env python3
"""
紧急修复所有语法错误
"""
import os
import re

def fix_broken_strings(content):
    """修复破损的字符串"""
    # 修复类似 D"ATABASE_UR"L" "的错误
    content = re.sub(r'([A-Z])"([A-Z_]*)"([A-Z_]*)', r'"\1\2\3"', content)
    
    # 修复类似 q"li"te":///../sellsys.db 的错误
    content = re.sub(r's([^""]*)"([^"]*)"([^"]*)', r'"\1\2\3"', content)
    
    # 修复类似 "messa"ge"" 的错误
    content = re.sub(r'([a-z])"([a-z]*)"([a-z]*)', r'"\1\2\3"', content)
    
    # 修复类似 W"elco"me" "的错误
    content = re.sub(r'([A-Z])"([a-zA-Z\s]*)', r'"\1\2"', content)
    
    # 修复类似 t"it"le"B""ar" 的错误
    content = re.sub(r'"([^"]*)"([a-zA-Z])', r'"\1\2"', content)
    
    # 修复类似 "r"" 的错误
    content = re.sub(r'""([a-zA-Z])', r'"\1"', content)
    
    # 修复类似 f"Error 的错误
    content = re.sub(r'"f([A-Z][^"]*)', r'F"\1', content)
    
    # 修复类似 ""ui"" 的错误
    content = re.sub(r'"u"([^"]*)"', r'"u"\1"', content)
    
    # 修复类似 C"RITICAL ""的错误
    content = re.sub(r'([A-Z])"([A-Z][^"]*)', r'"\1\2"', content)
    
    return content

def fix_file_emergency(file_path):
    """紧急修复单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = fix_broken_strings(content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Emergen"cy" fixed: {file_path}")
            return True
            
    except Exception as e:
        print(f"Err"or" fixing {file_path}: {e}")
        return False
    
    return False

def main():
    """主函数"""
    print("开始紧急修复...")
    
    # 重点修复的文件
    critical_files = [
        'backend/app/config.py',
        'backend/app/main.py',
        'backend/app/database.py',
        'client/main.py',
        'client/ui/login.py',
        'client/api/auth.py'
    ]
    
    for file_path in critical_files:
        if os.path.exists(file_path):
            fix_file_emergency(file_path)
    
    # 修复所有Python文件
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in ['venv', 'client_venv', '__pycache__', '.git']]
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                fix_file_emergency(file_path)
    
    print("紧急修复完成")

if __name__ == "__main__":
    main()
