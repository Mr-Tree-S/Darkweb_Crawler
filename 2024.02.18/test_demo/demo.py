from urllib.parse import unquote

# 原始的href
href = "1.%20%E3%80%8A2022%E7%89%88%E9%A2%84%E7%AE%97%E6%A8%A1%E5%9E%8B2023-2030%E3%80%8B-V2%E7%89%88%208.4%20%281%29.pdf"

# 解码URL编码的字符串
decoded_href = unquote(href)


print(decoded_href)
