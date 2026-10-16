"""
第二题

网址: https://www.cosrx.com/collections/all
字段: 产品名称 (name)、原价 (price)、产品图片 (images)、成分 (Key Ingredients)、尺码选项 (Size)

需求: 爬取链接中的所有商品(共 6 页), 并将数据存储到 CSV 文件中, images 字段多张图片请使用 , 分割
技术: 使用 requests 库爬取
"""

import csv
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

import chompjs
import requests
from parsel import Selector

HEADERS = {
    "sec-fetch-mode": "navigate",  # 检测字段
    "sec-fetch-site": "none",  # 检测字段
    "accept-language": "zh-CN,zh;q=0.9",  # 检测字段, 没有会返回其他地区的数据
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36",
}


class Spider:
    def __init__(self, total: int = 6) -> None:
        """
        :param total: 总页数
        """
        self.base_url = "https://www.cosrx.com/collections/all"
        self.handles_pattern = re.compile(r"var meta\s*=\s*(\{.*})\s*;")
        self.total = total

    def get_handles(self, page: int) -> list[str]:
        """
        获取当前也的全部产品句柄, 为了访问下一页
        :param page: 页码
        :return:
        """
        # 请求当前页的 HTML
        params = {"page": page}
        response = requests.get(self.base_url, headers=HEADERS, params=params)
        response.raise_for_status()

        # 从 HTML 找原始商品数据
        selector = Selector(text=response.text)
        scripts = selector.css("script::text").getall()
        script = ""
        for item in scripts:
            if "var meta = " in item:
                script = item
                break

        # 匹配商品数据变量
        match = self.handles_pattern.search(script)
        if match is None:
            raise ValueError("未匹配到商品数据")

        # 转换为 Python 字典
        products: dict[str, Any] = chompjs.parse_js_object(match.group(1))

        # 只返回 handle 数据
        return [item["handle"] for item in products["products"]]

    def get_data(self, handle: str) -> dict[str, Any]:
        """
        传入句柄采集商品详情数据
        :param handle: 商品页句柄
        :return:
        """
        response = requests.get(f"{self.base_url}/products/{handle}.json", headers=HEADERS)
        response.raise_for_status()

        return response.json()["product"]

    @staticmethod
    def parsel_data(data: dict[str, Any]) -> dict[str, Any]:
        """
        解析数据
        :param data: 原始数据
        :return:
        """
        body_html = data["body_html"]
        selector = Selector(text=body_html)

        key_ingredients = selector.css("p:nth-of-type(1) > em").xpath("following-sibling::text()").get()
        size = selector.css("p:nth-of-type(2) > em > strong").xpath("following-sibling::text()").get()
        images = [item["src"] for item in data["images"]]

        return {
            "name": data["title"],
            "price": data["variants"][0]["price"],
            "images": images,
            "KeyIngredients": key_ingredients or "无",
            "Size": size or "无",
        }

    @staticmethod
    def save_csv(data: list[dict[str, Any]]) -> None:
        """
        保存数据为 csv
        :param data:
        :return:
        """
        fieldnames = ["name", "price", "images", "KeyIngredients", "Size"]

        with Path("./data/question-2.csv").open(mode="w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for item in data:
                item["images"] = ",".join(item["images"])
                writer.writerow(item)

    def main(self) -> None:
        results = []
        for page in range(1, self.total + 1):
            handles = self.get_handles(page)

            print(f"正在采集第 {page} 页")
            if not handles:
                print(f"第 {page} 页没数据, 自动终止采集")
                break

            """
            for handle in handles:
                data = self.get_data(handle)
                result = self.parsel_data(data)
                print(result)
                results.append(result)
            """

            # 引入多线程提高采集效率, 并发太多会 429 状态码
            with ThreadPoolExecutor(max_workers=2) as executor:
                data_list = executor.map(self.get_data, handles)

                for data in data_list:
                    result = self.parsel_data(data)
                    print(result)
                    results.append(result)

        self.save_csv(results)


if __name__ == "__main__":
    spider = Spider()
    spider.main()
