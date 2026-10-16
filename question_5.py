"""
第五题

通关 https://match.yuanrenxue.cn/match/19
"""

import requests

URL = "https://match.yuanrenxue.cn/api/question/19"

HEADERS = {
    'user-agent': 'yuanrenxue',
}

COOKIES = {
    "sessionid": "unhg7w1n705unghjqze1l05lz4xyk6h5"
}

count = 0
# 循环遍历取每一页的数据
for page in range(1, 6):
    params = {
        'page': f'{page}',
        'pageSize': '10',
        'kw': '',
    }
    response = requests.get(URL, params=params, headers=HEADERS, cookies=COOKIES)
    response.raise_for_status()
    print(response.json())

    count += sum(response.json()["data"])

print(count)
