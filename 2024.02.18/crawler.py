import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
import os
import argparse
import threading

# Define the base URL
base_url = "http://rukmycgk3na5szajc4psircu2tf3m32hd2zc6pqsbc2b4d5ovrtmxqid.onion/"

def requests_handler(input_dir_path, output_file_path):
    url = base_url + input_dir_path

    # Create a session object
    session = requests.session()
    session.trust_env = False
    session.proxies = {'http': 'socks5h://localhost:9150', 'https': 'socks5h://localhost:9150'}

    # Define request headers
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

    # Send a request using the proxy
    response = session.request("GET", url, headers=headers)
    response.encoding = 'utf-8'
    session.close()

    # print the response
    # print("Response Status Code:", response.status_code)
    # print("Response Content:")
    # print(response.text)

    # Parse the response
    soup = BeautifulSoup(response.text, "html.parser")
    # path_parent_debug = soup.find('h1').text
    # print("#### path_parent_debug:", path_parent_debug, "####")
    path_parent = soup.find('h1').text.split("Index of /")[1]
    # print("#### path_parent:", path_parent, "####")
    itemList = soup.find_all('a')
    # print("#### itemList START ####", itemList, "#### itemList: END ####")

    for item in itemList:
        if item.text == "../":
            continue
        href = item['href']
        # print("#### href:", href, "####")
        name = unquote(href)
        # print("#### name:", name, "####")
        date_time = item.next_sibling.strip().split("  ")[0]
        # print("#### date_time:", date_time, "####")
        file_size = item.next_sibling.strip().split("  ")[-1].strip()
        # print("#### file_size:", file_size, "####")
        if file_size == "-":
            file_type = "dir"
            dir_path = path_parent + name
            dir_path = dir_path.replace("#", "%23")
            # print("#### dir_path:", dir_path, "####")
            # Create a thread to handle subdirectory
            threading.Thread(target=requests_handler, args=(dir_path, output_file_path)).start()
        else:
            file_type = "file"
            file_type_detail = name.split(".")[-1]
            file_path = path_parent + name
            # Prepare data row
            delimiter = "|"
            data_row = delimiter.join([file_path, name, file_type, file_type_detail, date_time, file_size])
            # print("--------------------")
            print(data_row)
            # print("--------------------")
            
            with open(output_file_path, 'a') as file:
                file.write(data_row + "\n")


# Parse arguments
parser = argparse.ArgumentParser(description='Darkweb crawler')
parser.add_argument('-p', '--path', type=str, help='Input path to be crawled')
args = parser.parse_args()

# Main execution
if args.path:
    input_dir_path = args.path
    # Create directory if it does not exist
    if not os.path.exists(input_dir_path):
        os.makedirs(input_dir_path)
    output_file_name = "file_name_list.txt"
    output_file_path = os.path.join(input_dir_path, output_file_name)
    requests_handler(input_dir_path, output_file_path)
else:
    # Display usage information
    print('Usage: python3 crawler.py -p <path>')
