#!/usr/bin/env python3
"""
最终语法错误修复脚本
"""
import os
import re

def comprehensive_fix(content):
    """全面修复所有语法错误"""
    
    # 1. 修复破损的字符串字面量
    # 修复类似 "messa"ge"": W"elcome 的错误
    content = re.sub(r'([a-z])""([a-z]*)":\s*([A-Z])"([^"]*)', r'"\1\2": "\3\4"', content)
    
    # 修复类似 S"alesFol"low"" 的错误
    content = re.sub(r'([A-Z])"([a-zA-Z]*)"([a-z])"([a-zA-Z]*)', r'"\1\2\3\4"', content)
    
    # 修复类似 a""ll", delete-orp"han"" 的错误
    content = re.sub(r'([a-z])"([a-z,\s-]*)"([a-z]*)', r'"\1\2\3"', content)
    
    # 修复类似 "tit"le"B""ar" 的错误
    content = re.sub(r'"([^"]*)"([a-zA-Z])', r'"\1\2"', content)
    
    # 修复类似 ""r" 的错误
    content = re.sub(r'""([a-zA-Z])', r'"\1"', content)
    
    # 修复类似 p"asswo"rd" 的错误
    content = re.sub(r'([a-z])"([a-z]*)', r'"\1\2"', content)
    
    # 修复类似 "access""_token 的错误
    content = re.sub(r'([a-z]{2})"([a-z_]*)', r'"\1\2"', content)
    
    # 修复类似 f"An" error 的错误
    content = re.sub(r'f([A-Z])"([^"]*)"', r'"f"\1\2"', content)
    
    # 修复类似 "compa"ny"", N"/A" 的错误
    content = re.sub(r'([a-z])"([a-z]*)",\s*([A-Z])"([^"]*)"([A-Z])', r'"\1\2", "\3\4\5"', content)
    
    # 修复类似 "addr"e"s", "N/A" 的错误
    content = re.sub(r'([a-z])"([a-z]*)",\s*([A-Z]/[A-Z])', r'"\1\2", "\3"', content)
    
    # 修复类似 ""no"te"", 的错误
    content = re.sub(r'"([a-z])"([a-z]*)",\s*\)', r'"\1\2", "")', content)
    
    # 修复类似 "f"<b> 的错误
    content = re.sub(r'"f"([^"]*)', r'"f"\1', content)
    
    # 2. 修复特殊情况
    # 修复 DATABASE_URL 相关错误
    content = re.sub(r'DATABASE_U"RL"""', r'D"ATABASE_URL"', content)
    content = re.sub(r'SECRET_K"EY""""', r'S"ECRET_KEY"', content)
    content = re.sub(r'"H"S"""256"', r'H"S256"', content)
    content = re.sub(r'"qlite"":///../sellsys.db', r'"sqlite:///../sellsys.d"b"', content)
    content = re.sub(r'y"o"ur"-secret-"key""', r'"yo"ur"-secret-"key""', content)
    
    # 修复 API 相关错误
    content = re.sub(r'巨炜科技客户管理系统 AP"I"""', r'"巨炜科技客户管理系统 API"', content)
    content = re.sub(r'/"api""', r'"/"api""', content)
    
    # 修复 return 语句错误
    content = re.sub(r'return \{"messa"ge"": W"elcome to SellSYS "A""P"I"""\}', r'return {"messa"ge"": W"elcome to SellSYS API"}', content)
    
    return content

def fix_file_final(file_path):
    """最终修复单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = comprehensive_fix(content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Final fixed: {file_path}")
            return True
            
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False
    
    return False

def main():
    """主函数"""
    print("开始最终语法修复...")
    
    # 重点修复的关键文件
    critical_files = [
        'backend/app/main.py',
        'backend/app/config.py',
        'backend/app/models/customer.py',
        'client/api/auth.py',
        'client/ui/contact_view_dialog.py'
    ]
    
    for file_path in critical_files:
        if os.path.exists(file_path):
            fix_file_final(file_path)
    
    # 修复所有Python文件
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in ['venv', 'client_venv', '__pycache__', '.git']]
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                fix_file_final(file_path)
    
    print("最终语法修复完成")

if __name__ == "__main__":
    main()
