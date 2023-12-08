import os
import requests
from urllib.parse import quote

# 定义文件路径
file_path = "/Users/jack/Desktop/Dev/crawler/12.07/list.txt"

session = requests.session()
session.trust_env = False
session.proxies = {'http': 'socks5h://localhost:9150', 'https': 'socks5h://localhost:91ls50'}
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'http://weqv4fxkacebqrjd3lmnss6lrmoxoyihtcc6kdc6mblbv62p5q6skgid.onion/public/GROUPHCkg3z2BDTMdh7r5Nn6X4eWpHmVLEjbvJ9wR8GCauU/HKG/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1'
    }

count = 0

# 逐行读取目录路径
with open(file_path, 'r') as file:
    directories = file.readlines()

# 处理每个目录路径
for directory in directories:
    count = count + 1
    # 去除首尾的空白字符
    directory = directory.strip()[1:]
    specified_directory = os.path.dirname(directory)

    # 创建目录
    if not os.path.exists(specified_directory):
        os.makedirs(specified_directory, exist_ok=True)

    if os.path.exists(directory):
        print(f"文件 {directory} 已存在，跳过下载")
        continue

    print("开始下载第 {}/{} 个文件".format(count, len(directories)))
    # 构建完整的URL
    try:
        url = "http://weqv4fxkacebqrjd3lmnss6lrmoxoyihtcc6kdc6mblbv62p5q6skgid.onion/public/GROUPHCkg3z2BDTMdh7r5Nn6X4eWpHmVLEjbvJ9wR8GCauU/" + quote(directory, safe='')  # 替换为实际的URL前缀
        response = session.request("GET", url, headers=headers)
        # 发起请求并保存文件
        with open(directory, 'wb') as file:
            file.write(response.content)
        expected_size = int(response.headers.get('Content-Length'))
        actual_size = os.path.getsize(directory)
        if expected_size == actual_size:
            print("大小一致，{}==={}文件下载完成！".format(expected_size,actual_size))
        else:
            print("大小不一致，{} != {}文件下载失败！".format(expected_size,actual_size))
    except:
        continue