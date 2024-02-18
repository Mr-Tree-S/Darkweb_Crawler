import requests
from bs4 import BeautifulSoup
import json
import urllib.parse
import os
import argparse


# if you want to exclude some dirpath, please add it to this list
done_dirs = []

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
    session.close()

    # print the response
    print("Response Status Code:", response.status_code)
    # print("Response Content:")
    # print(response.text)

    # Parse the response
    soup = BeautifulSoup(response.text, "html.parser")
    path_parent = soup.find('h1').text
    print("#### path_parent: ", path_parent)
    itemList = soup.find_all('a')
    # print("#### itemList START ####", itemList, "#### itemList: END ####")
    # for item in itemList:
    item = itemList[0]
    if item is not None:
        # Extract file or directory path
        print("#### item: ", item)
        href = item['href']
        print("#### href: ", href)
        # Extract display name
        displayname = item.text
        print("#### displayname: ", displayname)


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
