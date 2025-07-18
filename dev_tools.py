#!/usr/bin/env python3
"""
开发工具集 - 提高开发效率，减少错误
"""
import os
import sys
import subprocess
import ast
import re
from pathlib import Path

class CodeValidator:
    """代码验证器"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate_file(self, file_path):
        """验证单个Python文件"""
        self.errors.clear()
        self.warnings.clear()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 语法检查
            try:
                ast.parse(content)
            except SyntaxError as e:
                self.errors.append(f"语法错误 {file_path}:{e.lineno}: {e.msg}")
                return False
            
            # 常见问题检查
            self._check_common_issues(content, file_path)
            
            return len(self.errors) == 0
            
        except Exception as e:
            self.errors.append(f"文件读取错误 {file_path}: {e}")
            return False
    
    def _check_common_issues(self, content, file_path):
        """检查常见问题"""
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # 检查未闭合的字符串
            if line.count('"') % 2 == 1 and not line.strip().startswith('#'):
                self.warnings.append(f"可能的未闭合字符串 {file_path}:{i}")
            
            # 检查f字符串格式错误
            if '"f"' in line and 'f"' not in line:
                self.warnings.append(f"f字符串格式错误 {file_path}:{i}")
            
            # 检查导入问题
            if 'from ..' in line and 'client' in file_path:
                self.warnings.append(f"相对导入可能有问题 {file_path}:{i}")

class ProjectManager:
    """项目管理器"""
    
    def __init__(self, project_root="client"):
        self.project_root = Path(project_root)
        self.validator = CodeValidator()
    
    def validate_all_files(self):
        """验证所有Python文件"""
        print("🔍 开始验证所有Python文件...")
        
        total_files = 0
        error_files = 0
        
        for py_file in self.project_root.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue
                
            total_files += 1
            print(f"检查: {py_file}")
            
            if not self.validator.validate_file(py_file):
                error_files += 1
                print(f"❌ {py_file} 有错误:")
                for error in self.validator.errors:
                    print(f"   {error}")
            
            if self.validator.warnings:
                print(f"⚠️  {py_file} 有警告:")
                for warning in self.validator.warnings:
                    print(f"   {warning}")
        
        print(f"\n📊 验证完成:")
        print(f"   总文件数: {total_files}")
        print(f"   错误文件数: {error_files}")
        print(f"   正常文件数: {total_files - error_files}")
        
        return error_files == 0
    
    def quick_fix_common_issues(self):
        """快速修复常见问题"""
        print("🔧 开始快速修复常见问题...")
        
        fixed_files = 0
        
        for py_file in self.project_root.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue
            
            if self._fix_file(py_file):
                fixed_files += 1
                print(f"✅ 已修复: {py_file}")
        
        print(f"🎉 修复完成，共修复 {fixed_files} 个文件")
    
    def _fix_file(self, file_path):
        """修复单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 修复常见的字符串问题
            content = self._fix_string_issues(content)
            
            # 修复导入问题
            content = self._fix_import_issues(content, file_path)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
            
            return False
            
        except Exception as e:
            print(f"修复文件 {file_path} 时出错: {e}")
            return False
    
    def _fix_string_issues(self, content):
        """修复字符串问题"""
        # 修复f字符串
        content = re.sub(r'"f"([^"]*)"', r'f"\1"', content)
        
        # 修复简单的未闭合字符串（保守修复）
        lines = content.split('\n')
        fixed_lines = []
        
        for line in lines:
            # 只修复明显的问题
            if (line.count('"') % 2 == 1 and 
                not line.strip().startswith('#') and
                ('print(' in line or 'setWindowTitle(' in line or 'setText(' in line)):
                
                if not line.rstrip().endswith('"') and not line.rstrip().endswith('")'):
                    if line.rstrip().endswith(')'):
                        line = line.rstrip()[:-1] + '")'
                    else:
                        line = line + '"'
            
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def _fix_import_issues(self, content, file_path):
        """修复导入问题"""
        if 'client' in str(file_path):
            # 修复相对导入
            content = re.sub(r'from \.\.api import', 'from api import', content)
            content = re.sub(r'from \.\.config import', 'from config import', content)
        
        return content

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python dev_tools.py validate  # 验证所有文件")
        print("  python dev_tools.py fix       # 快速修复常见问题")
        print("  python dev_tools.py check     # 验证并修复")
        return
    
    command = sys.argv[1]
    manager = ProjectManager()
    
    if command == "validate":
        manager.validate_all_files()
    elif command == "fix":
        manager.quick_fix_common_issues()
    elif command == "check":
        print("🚀 开始检查和修复...")
        manager.quick_fix_common_issues()
        print("\n" + "="*50)
        manager.validate_all_files()
    else:
        print(f"未知命令: {command}")

if __name__ == "__main__":
    main()
