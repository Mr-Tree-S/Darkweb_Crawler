import requests
import xml.etree.ElementTree as ET
import os


# 定义目标URL的基础部分
base_url = "http://weqv4fxkacebqrjd3lmnss6lrmoxoyihtcc6kdc6mblbv62p5q6skgid.onion/public/GROUPHCkg3z2BDTMdh7r5Nn6X4eWpHmVLEjbvJ9wR8GCauU/"
# path = "HKG/HKDC/DEPARTMENTS/ACL_Customer_Complaint_Registry/Customer Doc/D/"
# path = "HKG/HKDC/DEPARTMENTS/ACL_Customer_Complaint_Registry/"
path = "HKG/"


folder_path = path
output_file_name = "file_name_list.txt"
full_path = os.path.join(folder_path, output_file_name)

def requests_handler(path):
    url = base_url + path
    
    # 创建会话对象
    session = requests.session()
    session.trust_env = False
    session.proxies = {'http': 'socks5h://localhost:9150', 'https': 'socks5h://localhost:9150'}

    # 定义请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "text/plain,application/xml",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "http://weqv4fxkacebqrjd3lmnss6lrmoxoyihtcc6kdc6mblbv62p5q6skgid.onion/GROUPHCkg3z2BDTMdh7r5Nn6X4eWpHmVLEjbvJ9wR8GCauU/",
        "Depth": "1",
        "Origin": "http://weqv4fxkacebqrjd3lmnss6lrmoxoyihtcc6kdc6mblbv62p5q6skgid.onion",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }

    # 使用代理发送请求
    response = session.request("PROPFIND", url, headers=headers)
    session.close()

    # 输出响应
    print("Response Status Code:", response.status_code)
    # print("Response Content:")
    # print(response.text)
    
    # 解析 XML
    root = ET.fromstring(response.text)

    # 获取所有<D:response>元素的迭代器
    xml_responses = root.findall("{DAV:}response")

    # 现在遍历剩下的<D:response>元素
    for xml_response in xml_responses[1:]:
        # 提取文件或目录的路径
        href = xml_response.find("{DAV:}href").text
        prefix = "/GROUPHCkg3z2BDTMdh7r5Nn6X4eWpHmVLEjbvJ9wR8GCauU/"
        href = href.replace(prefix, "")
        # 提取显示名称
        displayname = xml_response.find(".//{DAV:}displayname").text
        # 提取资源类型（文件或目录）
        resourcetype = xml_response.find(".//{DAV:}resourcetype")
        resourcetype = "Directory" if resourcetype.find("{DAV:}collection") is not None else "File"
        # 提取文件大小（如果存在）
        contentlength = xml_response.find(".//{DAV:}getcontentlength")
        contentlength = contentlength.text if contentlength is not None else "N/A"
        # 提取最后修改时间
        lastmodified = xml_response.find(".//{DAV:}getlastmodified").text

        # 打印提取的信息
        delimiter = "|"
        data_row = delimiter.join([href, displayname, resourcetype, contentlength, lastmodified])
        # print(data_row)
        # print("--------------------")

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        with open(full_path, 'a') as file:
            if resourcetype == "Directory":
                requests_handler(href)
            else:
                file.write(data_row + "\n")

requests_handler(path)
