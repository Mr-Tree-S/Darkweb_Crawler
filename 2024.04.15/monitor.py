import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
import time
import argparse
from jira_interface import get_jira_instance, create_jira_issue


# Define the base URL
base_url = "http://lockbit3753ekiocyo5epmpy6klmejchjtzddoekjlnt6mu3qh4de2id.onion"

# Define the requests handler
def requests_handler(input_dir_path):
    url = base_url + input_dir_path

    # Create a session object
    session = requests.session()
    session.trust_env = False
    session.proxies = {'http': 'socks5h://localhost:9150', 'https': 'socks5h://localhost:9150'}

    # Define request headers
    headers = {
        'Host': 'lockbit3753ekiocyo5epmpy6klmejchjtzddoekjlnt6mu3qh4de2id.onion',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cookie': 'PHPSESSID=c5ems4n2pn8bc07pbhd9akpnop',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1'
    }

    # Send a request using the proxy
    response = session.request("GET", url, headers=headers)
    response.encoding = 'utf-8'
    session.close()

    # print the response
    print("Response Status Code:", response.status_code)
    # print("Response Content:")
    # print(response.text)

    # Parse the response
    soup = BeautifulSoup(response.text, "html.parser")
    post_title_list = soup.find_all('div',class_='post-title')
    if post_title_list:
        print("#### post-title START ####")
        for post_title in post_title_list:
            post_title_text = post_title.text.strip()
            # print(post_title_text)
        print("#### post-title END ####")
    else:
        print("No post_title_list found")
    # Call to create a Jira issue with all post titles
    create_issue_for_lockbit_info(post_title_list)
    print("#### Create Jira issue Success ####")

# Handle Jira issues
def create_issue_for_lockbit_info(post_title_list):
    # Setup Jira connection
    token = "xxxxxxx"
    jira = get_jira_instance(token)

    # Format all post titles into a single description string
    description = "Org List of Leaked Data:\n" + "\n".join([title.text.strip() for title in post_title_list])

    # Define issue data based on the information collected
    new_issue_data = {
    'project': 'DEMO',
    'summary': 'LockBit Monitor',
    'description': description,
    'issuetype': 'Incident'
    }

    # Create the Jira issue
    create_jira_issue(jira, new_issue_data)


# Parse arguments
parser = argparse.ArgumentParser(description='LockBit Monitor')
parser.add_argument('-p', '--path', type=str, default="/", help='Input path to be monitored')
parser.add_argument('-t', '--time', type=int, help='Interval time in seconds for repeating the script')
args = parser.parse_args()

# Main execution
if args.path:
    if args.time:
        while True:
            requests_handler(args.path)
            print(f"Waiting {args.time} seconds to repeat...")
            time.sleep(args.time)
    else:
        requests_handler(args.path)
else:
    print('Usage: python3 monitor.py -p <path> [-t <time>]')
