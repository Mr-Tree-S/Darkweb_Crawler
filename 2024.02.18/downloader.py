import os
import requests
from urllib.parse import quote
import argparse



# 定义文件路径
def requests_handler(input_list):
    session = requests.session()
    session.trust_env = False
    session.proxies = {'http': 'socks5h://localhost:9150', 'https': 'socks5h://localhost:9150'}
    headers = {
        "Host": "rukmycgk3na5szajc4psircu2tf3m32hd2zc6pqsbc2b4d5ovrtmxqid.onion",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1"
    }

    count = 0

    # 逐行读取目录路径
    with open(input_list, 'r') as list:
        file_list= list.readlines()
        # print("#### file_list:", file_list, "####")

    # 处理每个目录路径
    for file_path in file_list:
        count = count + 1
        file_path = file_path.split("|")[0]
        # print("#### file_path:", file_path, "####")
        dir_path = os.path.dirname(file_path)
        # print("#### dir_path:", dir_path, "####")

        # 创建目录
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

        if os.path.exists(file_path):
            print(f"文件 {file_path} 已存在，跳过下载")
            continue

        print("开始下载第 {}/{} 个文件，{}".format(count, len(file_list), file_path))
        # 构建完整的URL
        try:
            url = "http://rukmycgk3na5szajc4psircu2tf3m32hd2zc6pqsbc2b4d5ovrtmxqid.onion/" + quote(file_path, safe='')  # 替换为实际的URL前缀
            response = session.request("GET", url, headers=headers)
            # 发起请求并保存文件
            with open(file_path, 'wb') as file:
                file.write(response.content)
            expected_size = int(response.headers.get('Content-Length'))
            actual_size = os.path.getsize(file_path)
            if expected_size == actual_size:
                print("大小一致，{}==={}文件下载完成！".format(expected_size,actual_size))
            else:
                print("大小不一致，{} != {}文件下载失败！".format(expected_size,actual_size))
        except:
            continue

# Parse arguments
parser = argparse.ArgumentParser(description='Darkweb downloader')
parser.add_argument('-l', '--list', type=str, help='Input file list to be download')
args = parser.parse_args()

# Main execution
if args.list:
    input_list = args.list
    requests_handler(input_list)
else:
    # Display usage information
    print('Usage: python3 downloader.py -l <file_list>')