import requests
import xml.etree.ElementTree as ET
import os
import argparse


# Define the base URL
base_url = "http://weqv4fxkacebqrjd3lmnss6lrmoxoyihtcc6kdc6mblbv62p5q6skgid.onion/public/GROUPHCkg3z2BDTMdh7r5Nn6X4eWpHmVLEjbvJ9wR8GCauU/"

def requests_handler(input_dir_path, output_file_path):
    url = base_url + input_dir_path
    
    # Create a session object
    session = requests.session()
    session.trust_env = False
    session.proxies = {'http': 'socks5h://localhost:9150', 'https': 'socks5h://localhost:9150'}

    # Define request headers
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

    # Send a request using the proxy
    response = session.request("PROPFIND", url, headers=headers)
    session.close()

    # print the response
    # print("Response Status Code:", response.status_code)
    # print("Response Content:")
    # print(response.text)

    # Parse the XML response
    root = ET.fromstring(response.text)

    # Iterate through each <D:response> element except the parent node
    for xml_response in root.findall("{DAV:}response")[1:]:
        # Extract file or directory path
        href = xml_response.find("{DAV:}href").text
        prefix = "/GROUPHCkg3z2BDTMdh7r5Nn6X4eWpHmVLEjbvJ9wR8GCauU/"
        href = href.replace(prefix, "")
        # Extract display name
        displayname = xml_response.find(".//{DAV:}displayname").text
        # Determine resource type (file or directory)
        resourcetype = xml_response.find(".//{DAV:}resourcetype")
        resourcetype = "Directory" if resourcetype.find("{DAV:}collection") is not None else "File"
        # Extract file size if available
        contentlength = xml_response.find(".//{DAV:}getcontentlength")
        contentlength = contentlength.text if contentlength is not None else "N/A"
        # Extract last modified time
        lastmodified = xml_response.find(".//{DAV:}getlastmodified").text

        # Prepare data row
        delimiter = "|"
        data_row = delimiter.join([href, displayname, resourcetype, contentlength, lastmodified])
        # print(data_row)
        # print("--------------------")

        with open(output_file_path, 'a') as file:
            if resourcetype == "Directory":
                # Recursively handle directories
                requests_handler(href, output_file_path)
            else:
                # Write file data to output file
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

# path = "HKG/HKDC/DEPARTMENTS/ACL_Customer_Complaint_Registry/Customer Doc/D/"
# path = "HKG/HKDC/DEPARTMENTS/ACL_Customer_Complaint_Registry/"
# path = "HKG/"