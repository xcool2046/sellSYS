"""修复client目录下所有文件的相对导入问题"""
import os
import re

def fix_imports_in_file(filepath):
    """修复单个文件中的导入路径"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 记录原始内容用于比较
    original_content = content
    
    # 修复各种导入模式
    # from client.xxx import -> from xxx import
    content = re.sub(r'from client\.', 'from ', content)
    
    # from ..xxx import -> from xxx import (处理相对导入)
    content = re.sub(r'from \.\.([a-zA-Z_]+)', r'from \1', content)
    
    # from .xxx import -> from xxx import (可选，根据需要)
    # 注意：同级目录的相对导入通常是可以的，但如果有问题也可以修复
    # content = re.sub(r'from \.([a-zA-Z_]+)', r'from \1', content)
    
    # 如果文件被修改了，写回文件
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"修复了文件: {filepath}")
        return True
    return False

def fix_all_imports(root_dir='client'):
    """遍历所有Python文件并修复导入"""
    fixed_count = 0
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.py'):
                filepath = os.path.join(dirpath, filename)
                if fix_imports_in_file(filepath):
                    fixed_count += 1
    
    print(f"\n总共修复了 {fixed_count} 个文件")

if __name__ == "__main__":
    fix_all_imports()