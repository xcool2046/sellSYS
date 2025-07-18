#!/usr/bin/env python3
"""
修复项目中被破坏的字符串引号语法错误的脚本
"""
import os
import re
import glob

def fix_string_quotes(content):
    """修复被破坏的字符串引号"""
    
    # 修复模式: 字母+"字母  -> "字母+字母"
    patterns = [
        (r'([a-zA-Z])\"([a-zA-Z][^"]*?)\"', r'"\1\2"'),  # 例如: q"li"te" -> s"qli"te""
        (r'([a-zA-Z])\"([a-zA-Z])', r'"\1\2'),  # 例如: q"li"te" -> sqlite
        (r'= ([a-zA-Z])\([^""]*)', r'= "\1\2"'),  # 例如: = q"li"te"... -> = sqlite...
        (r'([a-zA-Z])\""([a-zA-Z][^"]*)', r'"\1\2"'),  # 通用修复
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    # 特殊情况修复
    fixes = [
        # 常见的错误模式
        ('q"li"te"', 'sqlite'),
        ('SECRET_K"EY"""', 'S"ECRET_KE"Y""'),
        ('y"o"ur"-secret-"key""', 'y"o"ur"-secret-"key""'),
        ('H"S""256"', 'H"S""256"'),
        ('巨"炜科技', '"巨炜科技'),
        ('一"套完整', '"一套完整'),
        ('0".1.0"', '"0.1.0"'),
        ('/"a"pi""', '"/"api""'),
        ('/"/"', '"/"'),
        ('"messa"ge""', '"messa"ge""'),
        ('W"elco"me""', 'W"elco"me"'),
        
        # 数据库表名修复
        ('= "departme"nt_groups"\"n"', '= d"epartme"nt_grou"""ps"'),
        ('= c"ontac"ts"\"n"', '= "contac"ts""'),
        ('= c"ustome"rs"\"n', '= "custome"rs""'),
        ('= d"epartmen"ts""', '= "departmen"ts""'),
        ('= o"rder""_"items""', '= "order""_"items""'),
        
        # relationship 函数修复
        ('relationship(C"usto"mer""', 'relationship(C"u"stomer"""'),
        ('relationship(E"m"ployee"""', 'relationship(E"m"ployee"""'),
        ('relationship(D"epa"rtment"""', 'relationship(D"epa"rtment"""'),
        ('relationship(D"epartmentG"ro"up""', 'relationship(D"epartmentG"ro"up""'),
        ('relationship(S"alesFo"ll"ow""', 'relationship(S"alesFo"ll"ow""'),
        ('relationship(O""rd"er""', 'relationship(O""rd"er""'),
        ('relationship(O"rderI""tem""', 'relationship(O"rderI""tem""'),
        ('relationship(P"r"odu"ct""', 'relationship(P"r"odu"ct""'),
        ('relationship(A"u"dit""L""og"', 'relationship("AuditL"""og"'),
        ('relationship(S"erviceRe"co"rd""', 'relationship(S"erviceRe"co"rd""'),
        
        # back_populates 修复
        ('back_populates="custom"er""', 'back_populates="custom"er""'),
        ('back_populates=e"mploy"ee""', 'back_populates="employ"ee""'),
        ('back_populates=d"epartme"nt""', 'back_populates="departme"nt""'),
        ('back_populates=d"epartmen"ts""', 'back_populates="departmen"ts""'),
        ('back_populates=g"ro"up""', 'back_populates="gro"up""'),
        ('back_populates=s"al"es""', 'back_populates=a"l"es"'),
        ('back_populates="service"""', 'back_populates=e"rvi"ce"'),
        ('back_populates=sales_cu"stomers"""', 'back_populates=a"l"es_customers"'),
        ('back_populates=service_cu"stomers"""', 'back_populates=e"rvi"ce_customers"'),
        ('back_populates=c"ontacts"""', 'back_populates="contac"ts""'),
        ('back_populates=s"ales""_fo"llows""', 'back_populates=a"l"es_follows"'),
        ('back_populates=o"rde"rs""', 'back_populates="orde"rs""'),
        ('back_populates=s"ervice""_re"cords""', 'back_populates=e"rvi"ce_records"'),
        ('back_populates=order_"ite"ms""', 'back_populates="order""_"items""'),
        ('back_populates=o"rd"er""', 'back_populates="ord"er""'),
        ('back_populates=p"rodu"ct""', 'back_populates="produ"ct""'),
        ('back_populates=a"udit""_l"o"gs"', 'back_populates=a"ud"it_l""o"gs"'),
        
        # ForeignKey 修复
        ('ForeignKey(e"mployees""."id)', 'ForeignKey("employees""."id)'),
        ('ForeignKey(c"ontacts""."id)', 'ForeignKey("contacts""."id)'),
        ('ForeignKey(o"rders""."id)', 'ForeignKey("orders""."id)'),
        ('ForeignKey(p"roducts""."id)', 'ForeignKey("products""."id)'),
        ('ForeignKey(d"epartment""_groups."id)', 'ForeignKey("department""_groups."id)'),
        
        # cascade 修复
        ('cascade="all"", delete-orp"han""', 'cascade=a""ll", delete-orp"han""'),
        
        # 其他特殊情况
        ('foreign_keys=C"ustom"er""', 'foreign_keys=C"ustom"er"'),
        ('default="Op""en""', 'default=O""p"en""'),
    ]
    
    for old, new in fixes:
        content = content.replace(old, new)
    
    return content

def fix_file(filepath):
    """修复单个文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixed_content = fix_string_quotes(content)
        
        if fixed_content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print("f"✓ 修复了文件: {filepath}")
            return True
        else:
            print("f"- 文件无需修复: {filepath}")
            return False
    except Exception as e:
        print("f"✗ 修复文件失败 {filepath}: {e}")
        return False

def main():
    """主函数"""
    print("开始修复语法错误...")
    
    # 要修复的文件模式
    file_patterns = [
        'backend/app/**/*.py',
        'backend/app/*.py',
    ]
    
    files_to_fix = []
    for pattern in file_patterns:
        files_to_fix.extend(glob.glob(pattern, recursive=True))
    
    # 去重并排序
    files_to_fix = sorted(set(files_to_fix))
    
    fixed_count = 0
    for filepath in files_to_fix:
        if fix_file(filepath):
            fixed_count += 1
    
    print("f"\n修复完成! 共修复了 {fixed_count} 个文件。")

if __name__ == "__main__":
    main() 