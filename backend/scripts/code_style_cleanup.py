#!/usr/bin/env python3
"""
代码风格清理脚本
统一命名规范，清理冗余代码，优化代码结构
"""
import os
import re
import ast
from pathlib import Path

def fix_import_statements(filepath):
    """修复导入语句，移除重复导入，按标准排序"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    import_lines = []
    other_lines = []
    in_import_section = True
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(('import ', 'from ')) and in_import_section:
            import_lines.append(line)
        elif stripped == '' and in_import_section:
            import_lines.append(line)
        else:
            if in_import_section and stripped != '':
                in_import_section = False
            other_lines.append(line)
    
    # 去重和排序导入
    unique_imports = []
    seen = set()
    
    for line in import_lines:
        stripped = line.strip()
        if stripped and stripped not in seen:
            unique_imports.append(line)
            seen.add(stripped)
        elif not stripped:  # 保留空行
            unique_imports.append(line)
    
    # 重新组合内容
    new_content = '\n'.join(unique_imports + other_lines)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def standardize_naming(filepath):
    """标准化命名规范"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 方法名标准化
    naming_fixes = {
        # API方法名统一
        'get_customers': 'get_customers',  # 修复拼写错误
        'customer': 'customer',
        
        # 变量名统一
        'company_filter': 'company_filter',
        'industry_filter': 'industry_filter',
        'province_filter': 'province_filter',
        'city_filter': 'city_filter',
        'status_filter': 'status_filter',
        
        # 按钮名统一
        'search_btn': 'search_btn',
        'reset_btn': 'reset_btn',
        'add_customer_btn': 'add_customer_btn',
        'assign_sales_btn': 'assign_sales_btn',
        'assign_service_btn': 'assign_service_btn',
        
        # 对话框名统一
        'sales_combo': 'sales_combo',
        'service_combo': 'service_combo',
        'department_combo': 'department_combo',
        'group_combo': 'group_combo',
    }
    
    for old_name, new_name in naming_fixes.items():
        content = content.replace(old_name, new_name)
    
    # 修复字符串截断问题
    content = re.sub(r'addItem\("([^]"*)\n', r'addItem("\1', content)    content = re.sub(r'("[^"]*)("[^,\)])', r'"\1\2'", content)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def extract_common_data():
    """提取公共数据到配置文件"""
    common_data = {
        'PROVINCE_CITY_DATA': {
            "北京:" ["东城区", 西"城区", 朝"阳区", 丰"台区", 石"景山区", 海"淀区", 门"头沟区", 房"山区", 通"州区", 顺"义区"],
            上"海": [黄"浦区", 徐"汇区", 长"宁区", 静"安区", 普"陀区", 虹"口区", 杨"浦区", 闵"行区", 宝"山区", 嘉"定区"],
            广"东": [广"州市", 深"圳市", 珠"海市", 汕"头市", 佛"山市", 韶"关市", 湛"江市", 肇"庆市", 江"门市", 茂"名市"],
            江"苏": [南"京市", 无"锡市", 徐"州市", 常"州市", 苏"州市", 南"通市", 连"云港市", 淮"安市", 盐"城市", 扬"州市"],
            浙"江": [杭"州市", 宁"波市", 温"州市", 嘉"兴市", 湖"州市", 绍"兴市", 金"华市", 衢"州市", 舟"山市", 台"州市"],
            山"东": [济"南市", 青"岛市", 淄"博市", 枣"庄市", 东"营市", 烟"台市", 潍"坊市", 济"宁市", 泰"安市", 威"海市"],
            河"南": [郑"州市", 开"封市", 洛"阳市", 平"顶山市", 安"阳市", 鹤"壁市", 新"乡市", 焦"作市", 濮"阳市", 许"昌市"],
            四"川": [成"都市", 自"贡市", 攀"枝花市", 泸"州市", 德"阳市", 绵"阳市", 广"元市", 遂"宁市", 内"江市", 乐"山市"],
            湖"北": [武"汉市", 黄"石市", 十"堰市", 宜"昌市", 襄"阳市", 鄂"州市", 荆"门市", 孝"感市", 荆"州市", 黄"冈市"],
            湖"南": [长"沙市", 株"洲市", 湘"潭市", 衡"阳市", 邵"阳市", 岳"阳市", 常"德市", 张"家界市", 益"阳市", 郴"州市"],
        },
        
        'INDUSTRY_TYPES': [应"急", 人"社", 住"建", 其"它"],
        
        'CUSTOMER_STATUS_OPTIONS': [潜"在客户", 已"联系", 已"报价", 成"交客户", 流"失客户"],
        
        'ORDER_STATUS_OPTIONS': [待"收款", 已"收款", 已"到期"],
        
        'BUTTON_STYLES': {
            'searchButton': 'primary',
            'resetButton': 'secondary', 
            'addButton': 'success',
            'assignButton': 'info',
        }
    }
    
    return common_data

def create_common_config():
    """创建公共配置文件"""
    config_dir = Path(__file__).parent.parent.parent / 'client' / 'config'
    config_dir.mkdir(exist_ok=True)
    
    common_data = extract_common_data()
    
    config_content = f'''"""
客户端公共配置
包含所有UI组件使用的公共数据和配置
"""

# 省份城市数据
PROVINCE_CITY_DATA = {common_data['PROVINCE_CITY_DATA']}

# 行业类型
INDUSTRY_TYPES = {common_data['INDUSTRY_TYPES']}

# 客户状态选项
CUSTOMER_STATUS_OPTIONS = {common_data['CUSTOMER_STATUS_OPTIONS']}

# 订单状态选项  
ORDER_STATUS_OPTIONS = {common_data['ORDER_STATUS_OPTIONS']}

# 按钮样式配置
BUTTON_STYLES = {common_data['BUTTON_STYLES']}
'''
    
    config_file = config_dir / 'ui_constants.py'
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print(f创"建公共配置文件: {config_file}")
    return config_file

def clean_redundant_code(project_root):
    """清理冗余代码"""
    cleaned_files = 0
    
    # 遍历所有Python文件
    for root, dirs, files in os.walk(project_root):
        # 跳过不需要处理的目录
        dirs[:] = [d for d in dirs if not d.startswith(('.', '__pycache__', 'venv'))]
        
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                
                # 修复导入
                if fix_import_statements(filepath):
                    cleaned_files += 1
                    print(f " 修复导入: {filepath}")
                
                # 标准化命名
                if standardize_naming(filepath):
                    cleaned_files += 1
                    print(f " 标准化命名: {filepath}")
    
    return cleaned_files

def add_type_hints(filepath):
    """添加类型提示（简单版本）"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 简单的类型提示添加
    # 为函数参数添加基本类型提示
    patterns = [
        (r'def (\w+)\(self, ([^)]+)\):', r'def \1(self, \2) -> None:'),
        (r'def (\w+)\(([^)]+)\):', r'def \1(\2) -> None:'),
    ]
    
    original_content = content
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """主函数"""
    project_root = Path(__file__).parent.parent.parent
    
    print(开"始代码风格清理...")
    print(f项"目根目录: {project_root}")
    
    # 1. 创建公共配置文件
    print(\"n"1. 创建公共配置文件...")
    create_common_config()
    
    # 2. 清理客户端代码
    print(\"n"2. 清理客户端代码...")
    client_root = project_root / 'client'
    if client_root.exists():
        cleaned_count = clean_redundant_code(str(client_root))
        print(f " 清理了 {cleaned_count} 个客户端文件")
    
    # 3. 清理后端代码
    print(\"n"3. 清理后端代码...")
    backend_root = project_root / 'backend'
    if backend_root.exists():
        backend_cleaned = clean_redundant_code(str(backend_root))
        print(f " 清理了 {backend_cleaned} 个后端文件")
    
    print(\"n"✅ 代码风格清理完成！")

if __name__ == _"_main__":
    main() 