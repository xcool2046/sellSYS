"""
客户端配置文件
可以在本地开发和生产环境之间切换
"""

import os

# 环境变量控制使用哪个后端
# 设置 SELLSYS_ENV=production 使用生产服务器
# 默认使用本地开发服务器
ENV = os.environ.get('SELLSYS_ENV', 'development')

# API配置
API_CONFIGS = {
    'development': {
        'base_url': 'http://127.0.0.1:8000/api/v1',
        'timeout': 30
    },
    'production': {
        'base_url': 'http://YOUR_SERVER_IP:8000/api/v1',  # 替换为您的服务器IP
        'timeout': 60
    }
}

# 获取当前配置
API_CONFIG = API_CONFIGS.get(ENV, API_CONFIGS['development'])

# 导出配置
API_BASE_URL = API_CONFIG['base_url']
API_TIMEOUT = API_CONFIG['timeout']

print(f"[配置] 当前环境: {ENV}")
print(f"[配置] API地址: {API_BASE_URL}")