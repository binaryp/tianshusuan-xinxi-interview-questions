"""
第三题

网址: https://www.questnutrition.com/collections/protein-bars-all/products.json
字段: 每个产品的 handle、title, 以及提取 variants 列表中的变体 id

需求: 将结果保存到 CSV 文件中, id(如果一个产品有多个 id, 请使用 , 分割)
技术: 使用 requests 库爬取
"""

import csv
from pathlib import Path

import requests

URL = "https://www.questnutrition.com/collections/protein-bars-all/products.json"

HEADERS = {
    "sec-fetch-mode": "navigate",  # 检测字段
    "sec-fetch-site": "none",  # 检测字段
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36",
}

# 数据请求
response = requests.get(URL, headers=HEADERS)
response.raise_for_status()
datas = response.json()["products"]

# 数据处理写入
fieldnames = ["handle", "title", "ids"]
with Path("./data/question-3.csv").open(mode="w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    # 遍历提取数据
    for data in datas:
        row = {"handle": data["handle"], "title": data["title"], "ids": ",".join(f"{item['id']}" for item in data["variants"])}
        writer.writerow(row)
        print(row)
