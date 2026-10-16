"""
第一题

网址: https://roark.com/products/mens-bless-up-breathable-stretch-shirt-fossil-print
字段: 产品名称 (name)、原价 (price)、产品图片 (images)、
     当前选中的颜色名称 (Color) 以及尺码选项 (Size)

需求: 能够在控制台中打印结果即可
技术: 使用 requests 库爬取
"""

import re
from pprint import pprint
from typing import Any

import chompjs
import requests
from parsel import Selector

PRODUCT_URL = "https://roark.com/products/mens-bless-up-breathable-stretch-shirt-fossil-print"

HEADERS = {
    "accept-language": "zh-CN,zh;q=0.9",  # 返回货币字段
    "sec-fetch-mode": "navigate",  # 检测字段
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36",
}

PRODUCT_HANDLE = PRODUCT_URL.split("products")[1].replace("/", "")

PRODUCT_PATTERN = re.compile(rf"window\.products\['{PRODUCT_HANDLE}']\s*=\s*(\{{.*}})\s*;", re.DOTALL)


def get_html() -> str:
    """
    请求商品页面返回 HTML
    :return:
    """
    response = requests.get(PRODUCT_URL, headers=HEADERS)
    response.raise_for_status()

    return response.text


def get_product(html: str) -> dict[str, Any]:
    """
    从 HTML 中提取商品数据
    :param html:
    :return:
    """

    # 从 HTML 找原始商品数据
    selector = Selector(text=html)
    script = selector.css("script[product-data]::text").get()
    if script is None:
        raise ValueError("未找到原始商品数据")

    # 匹配商品数据变量
    match = PRODUCT_PATTERN.search(script)
    if match is None:
        raise ValueError("未匹配到商品数据")

    # 转换为 Python 字典
    product: dict[str, Any] = chompjs.parse_js_object(match.group(1))

    return product


def parsel_product(product: dict[str, Any]) -> dict[str, Any]:
    """
    解析指定字段商品数据
    :param product:
    :return:
    """

    images = ["https:" + item["src"] for item in product["images"]]
    name = product["title"].split(" - ")[0]
    price = product["price"] / 100

    return {
        "name": name,
        "price": price,
        "images": images,
        "Color": product["options_by_name"]["Color"]["option"]["values"][0],
        "Size": product["options_by_name"]["Size"]["option"]["values"],
    }


def main() -> None:
    html = get_html()
    product = get_product(html)
    result = parsel_product(product)

    pprint(result)


if __name__ == "__main__":
    main()
