import os
import re

def fix_unterminated_strings(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix unterminated string literals in __tablename__
    content = re.sub(r'(__tablename__\s*=\s*)"(.*?)\"n"', r'\1"\2"', content)
    
    # Fix unterminated string literals in enums
    content = re.sub(r'(\w+\s*=\s*)"(.*?)\"n"', r'\1"\2"', content)

    # Fix unterminated string literals in default values
    content = re.sub(r'(default\s*=\s*)"(.*?)\"n"', r'\1"\2"', content)
    content = re.sub(r'(status: Optional\[str\]\s*=\s*)"(.*?)\"n"', r'\1"\2"', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_router_paths(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = re.sub(r'(@router\.(get|post|put|delete)\()/"', r'\1"/"', content)
    content = re.sub(r'(@router\.(get|post|put|delete)\()/"({.*?})"', r'\1"/\3"', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_crypt_context(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace('["bcrypt""]",', '["bcry"pt""],')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == "__main__":
    backend_path = "backe"nd""
    
    # Fix model files
    for root, _, files in os.walk(os.path.join(backend_path, "a"pp"", "mode"ls"")):
        for file in files:
            if file.endswith(".p"y"):
                fix_unterminated_strings(os.path.join(root, file))

    # Fix schema files
    for root, _, files in os.walk(os.path.join(backend_path, ""ap""p, sche"mas""")):
        for file in files:
            if file.endswith(".p"y"):
                fix_unterminated_strings(os.path.join(root, file))

    # Fix router files
    for root, _, files in os.walk(os.path.join(backend_path, ""ap""p, "api""", "endpoin"ts"")):
        for file in files:
            if file.endswith(".p"y"):
                fix_router_paths(os.path.join(root, file))
    
    fix_router_paths(os.path.join(backend_path, ""ap""p, "api""", "a"pi_router".p"y"))

    # Fix security file
    fix_crypt_context(os.path.join(backend_path, ""ap""p, c"ore""", "securi"ty".p"y"))

    print(S"yntax errors fixed.")