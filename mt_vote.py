import requests
from lxml import etree
import re
import os
import json

# MT首页地址
URL = 'https://kp.m-team.cc/'
# 从环境变量中获取cookie
cookie = os.environ.get("MT_COOKIE")
# 构造请求头
HEADERS = {
    'authority': 'kp.m-team.cc',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'sec-ch-ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46',
    'Cookie': cookie
}

# 获取网页元素


def get_element():
    # 请求MT首页
    response = requests.get(URL, headers=HEADERS)
    # 判断请求是否成功
    if response.status_code == 200:
        # 请求成功，返回网页元素
        print('MT投票', "请求MT首页成功!")
        return etree.HTML(response.text)
    else:
        # 请求失败，发送通知
        pushplus_bot('MT投票', f"请求失败，状态码：{response.status_code}")
        return None

# 主函数


def main():
    # 获取网页元素
    root = get_element()
    # 判断是否请求成功
    if root is not None:
        # 获取投票按钮元素
        element = root.xpath('//*[@id="fun"]')
        if element:
            # 将元素转换为字符串
            btn = etree.tostring(element[0]).decode()
            # 正则匹配投票码
            match = re.search(r'funvote\((\d+),', btn)
            if match:
                # 获取投票码
                number = int(match.group(1))
                # 构造投票请求
                url = f"https://kp.m-team.cc/fun.php?action=vote&id={number}&yourvote=fun"
                # 发送投票请求
                response = requests.get(url, headers=HEADERS)
                # 判断请求是否成功
                if response.status_code == 200:
                    # 请求成功，发送通知
                    print('本日投票成功！')
                    pushplus_bot('MT投票', '本日投票成功！')
                else:
                    # 请求失败，发送通知
                    pushplus_bot('MT投票', f"请求失败，状态码：{response.status_code}")
            else:
                # 未找到相应的投票码，发送通知
                print('未找到相应的投票码')
                pushplus_bot('MT投票', '未找到相应的投票码')
        else:
            # 今日已投票，发送通知
            print("今日已投票，请勿重新投票")
            pushplus_bot('MT投票', '今日已投票，请勿重新投票')


def pushplus_bot(title: str, content: str) -> None:
    """
    通过 push+ 推送消息。
    """
    if not os.environ.get("PUSH_PLUS_TOKEN"):
        print("PUSHPLUS 服务的 PUSH_PLUS_TOKEN 未设置!!\n取消推送")
        return
    print("PUSHPLUS 服务启动")

    url = "http://www.pushplus.plus/send"
    data = {
        "token": os.environ.get("PUSH_PLUS_TOKEN"),
        "title": title,
        "content": content
    }
    body = json.dumps(data).encode(encoding="utf-8")
    headers = {"Content-Type": "application/json"}
    response = requests.post(url=url, data=body, headers=headers).json()

    if response["code"] == 200:
        print("PUSHPLUS 推送成功！")

    else:
        url_old = "http://pushplus.hxtrip.com/send"
        headers["Accept"] = "application/json"
        response = requests.post(
            url=url_old, data=body, headers=headers).json()

        if response["code"] == 200:
            print("PUSHPLUS(hxtrip) 推送成功！")

        else:
            print("PUSHPLUS 推送失败！")


if __name__ == "__main__":
    main()
