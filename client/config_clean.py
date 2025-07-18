"""
系统配置管理 - 干净版本
"""
import os
from typing import Dict, Any

class Config:
    """配置管理类"""
    
    def __init__(self):
        self.env = os.getenv('ENV', 'development')
        self._load_config()
    
    def _load_config(self):
        """加载配置"""
        if self.env == 'production':
            self._load_production_config()
        elif self.env == 'testing':
            self._load_testing_config()
        else:
            self._load_development_config()
    
    def _load_development_config(self):
        """开发环境配置"""
        self.API_BASE_URL = "http://127.0.0.1:8000/api"
        self.API_TIMEOUT = 30
        self.DEBUG = True
        self.LOG_LEVEL = "DEBUG"
        
        # 数据库配置（如果需要）
        self.DATABASE_URL = "sqlite:///./sellsys_dev.db"
        
        # UI配置
        self.WINDOW_TITLE = "巨炜科技客户管理信息系统 [开发版]"
        self.WINDOW_MIN_WIDTH = 1200
        self.WINDOW_MIN_HEIGHT = 800
        
        # 分页配置
        self.PAGE_SIZE = 20
        self.MAX_PAGE_SIZE = 100
    
    def _load_testing_config(self):
        """测试环境配置"""
        self.API_BASE_URL = "http://test.example.com/api"
        self.API_TIMEOUT = 15
        self.DEBUG = True
        self.LOG_LEVEL = "INFO"
        
        self.DATABASE_URL = "sqlite:///./sellsys_test.db"
        
        self.WINDOW_TITLE = "巨炜科技客户管理信息系统 [测试版]"
        self.WINDOW_MIN_WIDTH = 1200
        self.WINDOW_MIN_HEIGHT = 800
        
        self.PAGE_SIZE = 10
        self.MAX_PAGE_SIZE = 50
    
    def _load_production_config(self):
        """生产环境配置"""
        self.API_BASE_URL = os.getenv('API_BASE_URL', "https://api.sellsys.com/api")
        self.API_TIMEOUT = 60
        self.DEBUG = False
        self.LOG_LEVEL = "WARNING"
        
        self.DATABASE_URL = os.getenv('DATABASE_URL', "postgresql://user:pass@localhost/sellsys")
        
        self.WINDOW_TITLE = "巨炜科技客户管理信息系统"
        self.WINDOW_MIN_WIDTH = 1200
        self.WINDOW_MIN_HEIGHT = 800
        
        self.PAGE_SIZE = 50
        self.MAX_PAGE_SIZE = 200
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        return getattr(self, key, default)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            key: value for key, value in self.__dict__.items()
            if not key.startswith('_')
        }

# 创建全局配置实例
config = Config()

# 导出常用配置
API_BASE_URL = config.API_BASE_URL
API_TIMEOUT = config.API_TIMEOUT
DEBUG = config.DEBUG
LOG_LEVEL = config.LOG_LEVEL
WINDOW_TITLE = config.WINDOW_TITLE
WINDOW_MIN_WIDTH = config.WINDOW_MIN_WIDTH
WINDOW_MIN_HEIGHT = config.WINDOW_MIN_HEIGHT
PAGE_SIZE = config.PAGE_SIZE

# 打印配置信息
if DEBUG:
    print(f"[配置] 当前环境: {config.env}")
    print(f"[配置] API地址: {API_BASE_URL}")
    print(f"[配置] 调试模式: {DEBUG}")

# 行业类别配置
INDUSTRY_CATEGORIES = [
    "软件开发", "互联网", "电子商务", "金融服务", "教育培训",
    "医疗健康", "制造业", "建筑工程", "房地产", "零售贸易",
    "物流运输", "餐饮服务", "旅游酒店", "文化传媒", "咨询服务",
    "能源化工", "农业", "其他"
]

# 客户状态配置
CUSTOMER_STATUS = {
    "LEAD": "潜在客户",
    "CONTACTED": "已联系",
    "PROPOSAL": "已报价",
    "NEGOTIATION": "商务谈判",
    "WON": "成交客户",
    "LOST": "流失客户"
}

# 订单状态配置
ORDER_STATUS = {
    "DRAFT": "草稿",
    "PENDING": "待确认",
    "CONFIRMED": "已确认",
    "PROCESSING": "处理中",
    "SHIPPED": "已发货",
    "DELIVERED": "已交付",
    "COMPLETED": "已完成",
    "CANCELLED": "已取消"
}

# 服务状态配置
SERVICE_STATUS = {
    "OPEN": "待处理",
    "IN_PROGRESS": "处理中",
    "RESOLVED": "已解决",
    "CLOSED": "已关闭"
}

# 省份城市数据
PROVINCE_CITY_DATA = {
    "北京": ["东城区", "西城区", "朝阳区", "丰台区", "石景山区", "海淀区", "门头沟区", "房山区", "通州区", "顺义区"],
    "上海": ["黄浦区", "徐汇区", "长宁区", "静安区", "普陀区", "虹口区", "杨浦区", "闵行区", "宝山区", "嘉定区"],
    "广东": ["广州市", "深圳市", "珠海市", "汕头市", "佛山市", "韶关市", "湛江市", "肇庆市", "江门市", "茂名市"],
    "江苏": ["南京市", "无锡市", "徐州市", "常州市", "苏州市", "南通市", "连云港市", "淮安市", "盐城市", "扬州市"],
    "浙江": ["杭州市", "宁波市", "温州市", "嘉兴市", "湖州市", "绍兴市", "金华市", "衢州市", "舟山市", "台州市"],
    "山东": ["济南市", "青岛市", "淄博市", "枣庄市", "东营市", "烟台市", "潍坊市", "济宁市", "泰安市", "威海市"],
    "河南": ["郑州市", "开封市", "洛阳市", "平顶山市", "安阳市", "鹤壁市", "新乡市", "焦作市", "濮阳市", "许昌市"],
    "四川": ["成都市", "自贡市", "攀枝花市", "泸州市", "德阳市", "绵阳市", "广元市", "遂宁市", "内江市", "乐山市"],
    "湖北": ["武汉市", "黄石市", "十堰市", "宜昌市", "襄阳市", "鄂州市", "荆门市", "孝感市", "荆州市", "黄冈市"],
    "湖南": ["长沙市", "株洲市", "湘潭市", "衡阳市", "邵阳市", "岳阳市", "常德市", "张家界市", "益阳市", "郴州市"]
}

# 公司规模配置
COMPANY_SCALES = [
    "1-10人", "11-50人", "51-100人", "101-500人", 
    "501-1000人", "1000-5000人", "5000人以上"
]
