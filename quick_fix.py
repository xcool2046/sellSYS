#!/usr/bin/env python3
"""
快速修复所有语法错误
"""
import os
import re

def fix_string_issues(content):
    """修复字符串问题"""
    lines = content.split('\n')
    fixed_lines = []

    for line in lines:
        original_line = line

        # 修复中文标点符号
        line = line.replace('！', '!')
        line = line.replace('，', ',')
        line = line.replace('：', ':')
        line = line.replace('；', ';')
        line = line.replace('？', '?')

        # 修复常见的字符串问题
        # 1. 修复 setPlaceholderText("text) -> setPlaceholderText("text")
        line = re.sub(r'setPlaceholderText\("([^"]*)\)', r'setPlaceholderText("\1")', line)

        # 2. 修复 setObjectName(name") -> setObjectName("name")
        line = re.sub(r'setObjectName\(([^"]*)"([^"]*)"?\)', r'setObjectName("\1\2")', line)

        # 3. 修复 setText("text) -> setText("text")
        line = re.sub(r'setText\("([^"]*)\)', r'setText("\1")', line)

        # 4. 修复 setWindowTitle("title) -> setWindowTitle("title")
        line = re.sub(r'setWindowTitle\("([^"]*)\)', r'setWindowTitle("\1")', line)

        # 5. 修复 addItem("item) -> addItem("item")
        line = re.sub(r'addItem\("([^"]*)\)', r'addItem("\1")', line)

        # 6. 修复 print("text) -> print("text")
        line = re.sub(r'print\("([^"]*)\)', r'print("\1")', line)

        # 7. 修复 QLabel("text) -> QLabel("text")
        line = re.sub(r'QLabel\("([^"]*)\)', r'QLabel("\1")', line)

        # 8. 修复 QPushButton("text) -> QPushButton("text")
        line = re.sub(r'QPushButton\("([^"]*)\)', r'QPushButton("\1")', line)

        # 9. 修复函数调用中的字符串
        line = re.sub(r'_create_nav_button\(([^"]*)"([^"]*)"?\)', r'_create_nav_button("\1\2")', line)

        # 10. 修复QMessageBox调用
        line = re.sub(r'QMessageBox\.(\w+)\(self,\s*([^,]*),\s*([^)]*)\)', r'QMessageBox.\1(self, "\2", "\3")', line)

        # 11. 修复未闭合的字符串（通用）
        if line.count('"') % 2 == 1 and not line.strip().startswith('#'):
            # 如果行以某些模式结束，添加引号
            if (line.rstrip().endswith(')') and
                ('(' in line) and
                (line.count('(') == line.count(')'))):
                # 在最后一个)前添加"
                line = line.rstrip()[:-1] + '")'
            elif not line.rstrip().endswith('"'):
                line = line + '"'

        # 12. 修复没有引号的字符串参数
        if ('addItem(' in line or 'QLabel(' in line or 'QPushButton(' in line) and '"' not in line:
            # 简单的修复：为中文内容添加引号
            line = re.sub(r'(\w+)\(([^)]*)\)', lambda m: f'{m.group(1)}("{m.group(2)}")', line)

        fixed_lines.append(line)

    return '\n'.join(fixed_lines)

def fix_docstring_issues(content):
    """修复文档字符串问题"""
    # 修复单引号文档字符串
    content = re.sub(r'^\s*"([^"]*)"$', r'"""\1"""', content, flags=re.MULTILINE)
    return content

def fix_file(file_path):
    """修复单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 应用修复
        content = fix_string_issues(content)
        content = fix_docstring_issues(content)
        
        # 修复f字符串
        content = re.sub(r'"f"([^"]*)"', r'f"\1"', content)
        
        # 修复导入问题
        if 'client' in file_path:
            content = re.sub(r'from \.\.api import', 'from api import', content)
            content = re.sub(r'from \.\.config import', 'from config import', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已修复: {file_path}")
            return True
        else:
            print(f"⚪ 无需修复: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ 修复失败 {file_path}: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始快速修复所有语法错误...")
    
    fixed_count = 0
    total_count = 0
    
    # 遍历client目录下的所有Python文件
    for root, dirs, files in os.walk('client'):
        # 跳过__pycache__目录
        dirs[:] = [d for d in dirs if d != '__pycache__']
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                total_count += 1
                
                if fix_file(file_path):
                    fixed_count += 1
    
    print(f"\n🎉 修复完成！")
    print(f"总文件数: {total_count}")
    print(f"已修复: {fixed_count}")
    print(f"无需修复: {total_count - fixed_count}")

if __name__ == "__main__":
    main()
