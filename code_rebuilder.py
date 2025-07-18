#!/usr/bin/env python3
"""
代码重构工具 - 彻底解决字符串和语法问题
"""
import os
import ast
import re
from pathlib import Path

class CodeRebuilder:
    """代码重构器"""
    
    def __init__(self):
        self.chinese_punctuation = {
            '！': '!',
            '，': ',',
            '：': ':',
            '；': ';',
            '？': '?',
            '（': '(',
            '）': ')',
            '【': '[',
            '】': ']',
            '《': '<',
            '》': '>',
            '"': '"',
            '"': '"',
            ''': "'",
            ''': "'",
        }
    
    def fix_chinese_punctuation(self, content):
        """修复中文标点符号"""
        for chinese, english in self.chinese_punctuation.items():
            content = content.replace(chinese, english)
        return content
    
    def fix_string_literals(self, content):
        """修复字符串字面量"""
        lines = content.split('\n')
        fixed_lines = []
        
        for line_num, line in enumerate(lines, 1):
            original_line = line
            
            # 跳过注释行
            if line.strip().startswith('#'):
                fixed_lines.append(line)
                continue
            
            # 修复常见的字符串问题
            try:
                # 1. 修复f字符串
                line = re.sub(r'"f"([^"]*)"', r'f"\1"', line)
                line = re.sub(r'"f([^"]*)"', r'f"\1"', line)
                
                # 2. 修复函数调用中的字符串参数
                patterns = [
                    (r'setPlaceholderText\("([^"]*)\)', r'setPlaceholderText("\1")'),
                    (r'setObjectName\("([^"]*)\)', r'setObjectName("\1")'),
                    (r'setText\("([^"]*)\)', r'setText("\1")'),
                    (r'setWindowTitle\("([^"]*)\)', r'setWindowTitle("\1")'),
                    (r'addItem\("([^"]*)\)', r'addItem("\1")'),
                    (r'QLabel\("([^"]*)\)', r'QLabel("\1")'),
                    (r'QPushButton\("([^"]*)\)', r'QPushButton("\1")'),
                ]
                
                for pattern, replacement in patterns:
                    line = re.sub(pattern, replacement, line)
                
                # 3. 修复字典键值对
                line = re.sub(r'(["\']?)(\w+)(["\']?)\s*:\s*([^,}\]]*)', 
                             lambda m: f'"{m.group(2)}": {m.group(4)}' if not m.group(1) else m.group(0), 
                             line)
                
                # 4. 修复未闭合的字符串
                if line.count('"') % 2 == 1 and not line.strip().startswith('#'):
                    # 简单的修复策略
                    if line.rstrip().endswith(')') and '(' in line:
                        line = line.rstrip()[:-1] + '")'
                    elif not line.rstrip().endswith('"'):
                        line = line + '"'
                
            except Exception as e:
                print(f"警告: 第{line_num}行修复失败: {e}")
                # 如果修复失败，使用原始行
                line = original_line
            
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def fix_docstrings(self, content):
        """修复文档字符串"""
        # 修复单行文档字符串
        content = re.sub(r'^\s*"""([^"]*)"$', r'    """\1"""', content, flags=re.MULTILINE)
        content = re.sub(r'^\s*""([^"]*)"$', r'    """\1"""', content, flags=re.MULTILINE)
        content = re.sub(r'^\s*"([^"]*)"$', r'    """\1"""', content, flags=re.MULTILINE)
        
        return content
    
    def validate_syntax(self, content):
        """验证语法"""
        try:
            ast.parse(content)
            return True, None
        except SyntaxError as e:
            return False, str(e)
    
    def rebuild_file(self, file_path):
        """重构单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 应用修复
            content = self.fix_chinese_punctuation(content)
            content = self.fix_string_literals(content)
            content = self.fix_docstrings(content)
            
            # 验证语法
            is_valid, error = self.validate_syntax(content)
            
            if is_valid:
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"✅ 已重构: {file_path}")
                    return True
                else:
                    print(f"⚪ 无需重构: {file_path}")
                    return False
            else:
                print(f"❌ 重构后仍有语法错误 {file_path}: {error}")
                # 不保存有语法错误的文件
                return False
                
        except Exception as e:
            print(f"❌ 重构失败 {file_path}: {e}")
            return False
    
    def rebuild_project(self, project_root="client"):
        """重构整个项目"""
        print("🚀 开始重构项目...")
        
        rebuilt_count = 0
        total_count = 0
        error_count = 0
        
        for root, dirs, files in os.walk(project_root):
            # 跳过__pycache__目录
            dirs[:] = [d for d in dirs if d != '__pycache__']
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    total_count += 1
                    
                    result = self.rebuild_file(file_path)
                    if result is True:
                        rebuilt_count += 1
                    elif result is False and "语法错误" in str(result):
                        error_count += 1
        
        print(f"\n🎉 重构完成！")
        print(f"总文件数: {total_count}")
        print(f"已重构: {rebuilt_count}")
        print(f"语法错误: {error_count}")
        print(f"无需重构: {total_count - rebuilt_count - error_count}")

def main():
    """主函数"""
    rebuilder = CodeRebuilder()
    rebuilder.rebuild_project()

if __name__ == "__main__":
    main()
