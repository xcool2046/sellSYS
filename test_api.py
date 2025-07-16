import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_endpoint(name, url):
    print(f"\n测试 {name}...")
    try:
        response = requests.get(url, timeout=5)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print(f"成功! 返回数据: {json.dumps(response.json()[:2] if isinstance(response.json(), list) else response.json(), ensure_ascii=False, indent=2)}")
        else:
            print(f"错误响应: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")

# 测试各个端点
endpoints = [
    ("员工列表", f"{BASE_URL}/employees/"),
    ("客户列表", f"{BASE_URL}/customers/"),
    ("产品列表", f"{BASE_URL}/products/"),
    ("订单列表", f"{BASE_URL}/orders/"),
    ("服务记录", f"{BASE_URL}/service-records/"),
    ("销售视图", f"{BASE_URL}/sales-view/"),
]

print("开始API测试...")
for name, url in endpoints:
    test_endpoint(name, url)