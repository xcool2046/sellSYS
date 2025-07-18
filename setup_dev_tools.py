#!/usr/bin/env python3
"""
设置开发工具和代码质量检查
"""
import subprocess
import sys
import os

def install_dev_tools():
    """安装开发工具"""
    tools = [
        'black',      # 代码格式化
        'flake8',     # 代码检查
        'isort',      # 导入排序
        'autopep8',   # 自动修复PEP8问题
    ]
    
    print("安装开发工具...")
    for tool in tools:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', tool])
            print(f"✓ {tool} 安装成功")
        except subprocess.CalledProcessError:
            print(f"✗ {tool} 安装失败")

def create_config_files():
    """创建配置文件"""
    
    # .flake8 配置
    flake8_config = """[flake8]
max-line-length = 120
ignore = E203, E266, E501, W503
max-complexity = 10
exclude = 
    .git,
    __pycache__,
    venv,
    client_venv,
    .venv
"""
    
    # pyproject.toml 配置
    pyproject_config = """[tool.black]
line-length = 120
target-version = ['py39']
include = '\\.pyi?$'
exclude = '''
/(
    \\.git
  | __pycache__
  | venv
  | client_venv
  | \\.venv
)/
'''

[tool.isort]
profile = "black"
line_length = 120
multi_line_output = 3
"""
    
    # 写入配置文件
    with open('.flake8', 'w') as f:
        f.write(flake8_config)
    print("✓ .flake8 配置文件已创建")
    
    with open('pyproject.toml', 'w') as f:
        f.write(pyproject_config)
    print("✓ pyproject.toml 配置文件已创建")

def create_scripts():
    """创建便捷脚本"""
    
    # 代码检查脚本
    check_script = """#!/usr/bin/env python3
import subprocess
import sys

def run_checks():
    print("运行代码质量检查...")
    
    # 运行flake8
    print("\\n1. 运行 flake8 检查...")
    try:
        subprocess.run([sys.executable, '-m', 'flake8', 'client/'], check=True)
        print("✓ flake8 检查通过")
    except subprocess.CalledProcessError:
        print("✗ flake8 检查发现问题")
    
    # 运行black检查
    print("\\n2. 运行 black 格式检查...")
    try:
        subprocess.run([sys.executable, '-m', 'black', '--check', 'client/'], check=True)
        print("✓ black 格式检查通过")
    except subprocess.CalledProcessError:
        print("✗ black 格式检查发现问题")

if __name__ == "__main__":
    run_checks()
"""
    
    # 代码修复脚本
    fix_script = """#!/usr/bin/env python3
import subprocess
import sys

def fix_code():
    print("自动修复代码格式...")
    
    # 运行isort
    print("\\n1. 运行 isort 整理导入...")
    subprocess.run([sys.executable, '-m', 'isort', 'client/'])
    print("✓ 导入整理完成")
    
    # 运行black
    print("\\n2. 运行 black 格式化...")
    subprocess.run([sys.executable, '-m', 'black', 'client/'])
    print("✓ 代码格式化完成")
    
    # 运行autopep8
    print("\\n3. 运行 autopep8 修复...")
    subprocess.run([sys.executable, '-m', 'autopep8', '--in-place', '--recursive', 'client/'])
    print("✓ PEP8 修复完成")

if __name__ == "__main__":
    fix_code()
"""
    
    with open('check_code.py', 'w') as f:
        f.write(check_script)
    print("✓ check_code.py 脚本已创建")
    
    with open('fix_code.py', 'w') as f:
        f.write(fix_script)
    print("✓ fix_code.py 脚本已创建")

def main():
    print("设置开发环境...")
    install_dev_tools()
    create_config_files()
    create_scripts()
    print("\\n开发环境设置完成！")
    print("\\n使用方法:")
    print("- 运行 'python check_code.py' 检查代码质量")
    print("- 运行 'python fix_code.py' 自动修复代码格式")

if __name__ == "__main__":
    main()
