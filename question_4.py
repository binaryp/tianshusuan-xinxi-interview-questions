"""
第四题

给定一个包含重复元素的列表 [3, 1, 2, 3, 4, 1, 2], 请使用 三种不同 的方法去除重复的元素, 同时保持元素原本的出现顺序。结果在控制台打印即可
"""
data = [3, 1, 2, 3, 4, 1, 2]


def fun_1() -> None:
    """
    新版本字典中 key 是有序的
    :return:
    """
    print(list(dict.fromkeys(data)))


def fun_2() -> None:
    """
    列表追加判断
    :return:
    """
    temp = []
    for item in data:
        if item not in temp:
            temp.append(item)

    print(temp)


def fun_3():
    """
    使用集合的唯一性质
    :return:
    """
    seen = set()
    result = []

    for item in data:
        if item not in seen:
            seen.add(item)
            result.append(item)

    print(result)


if __name__ == '__main__':
    fun_1()
    fun_2()
    fun_3()
