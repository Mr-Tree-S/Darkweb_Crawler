import requests, json, urllib.parse, subprocess, re, os
from bs4 import BeautifulSoup
import logging
import argparse
import threading
# pip install pysocks


# if you want to exclude some dirpath, please add it to this list
done_dirs = []

def recursive(directory):
    # create logger
    log_path = "./log/" + directory.replace("/", "@") + "_log.txt"
    print("@@@ log_path START @@@", log_path, "@@@ log_path: END @@@")

    logger = logging.getLogger(log_path)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # do the job
    directory_url = urllib.parse.quote(directory)
    directory_url = directory_url.replace("/", "%2F").replace("%20", "+")
    for page_no in range(0, 100):
        cmd = "proxychains4 curl -X PROPFIND 'http://aeey7hxzgl6zowiwhteo5xjbf6sb36tkbn5hptykgmbsjrbiygv4c4id.onion/ajax.php'"
        cmd = cmd.replace("@PAGE@", str(page_no))
        cmd = cmd.replace("@DIR@", directory_url)
        # print("@@@ cmd START @@@", cmd, "@@@ cmd: END @@@")
        a = os.popen(cmd).read()
        jsonObj = json.loads(a)
        # print("@@@ json START @@@", jsonObj["html"], "@@@ json: END @@@")
        if jsonObj["html"] == "":
            print("@@@ HTML IS NULL & break @@@")
            break

        soup = BeautifulSoup(jsonObj["html"], "html.parser")
        itemList = soup.find_all('tr')
        # print("@@@ itemList START @@@", itemList, "@@@ itemList: END @@@")
        for item in itemList:
            cells = item.find_all('td')
            # print("@@@ cells START @@@", cells, "@@@ cells: END @@@")

            input_type = cells[0].find('input')
            summary = cells[1]
            size = cells[2].text
            # print("@@@ size START @@@", size, "@@@ size: END @@@")
            date = cells[3].text
            # print("@@@ date START @@@", date, "@@@ date: END @@@")

            if input_type == None:
                dirpath = ""
                dirpath = summary['dir']
                print("@@@ filepath START @@@", dirpath, "@@@ filepath: END @@@")
                dirhref = summary.find('a')
                print("@@@ filehref START @@@", dirhref, "@@@ filehref: END @@@")
                dirname = summary.text
                print("@@@ filename START @@@", dirname, "@@@ filename: END @@@")
                type = "folder"
                if dirpath != "" and dirpath != "." and dirpath != " .." and dirpath not in done_dirs and dirhref != None:
                    logger.info("|" + type + "|" + dirpath + "|" + size + "|" + date)
                    done_dirs.append(dirpath)
                    dirpath = urllib.parse.quote(dirpath)
                    recursive(dirpath)
            else:
                filepath = ""
                filepath = summary['file']
                print("@@@ filepath START @@@", filepath, "@@@ filepath: END @@@")
                filehref = summary.a['href']
                print("@@@ filehref START @@@", filehref, "@@@ filehref: END @@@")
                filename = summary.text
                print("@@@ filename START @@@", filename, "@@@ filename: END @@@")
                type = filename.split('.')[-1]
                if filepath != None:
                    logger.info("|" + type + "|" + filepath + "|" + size + "|" + date)

# handle arguments
parser = argparse.ArgumentParser(description='Crawler Script')
parser.add_argument('-d', '--input_dir', type=str, help='Input directory')
parser.add_argument('-f', '--input_file', type=str, help='Input file containing directories')
args = parser.parse_args()
# main
if args.input_file:
    with open(args.input_file, 'r') as file:
        threads = []
        for line in file:
            input_dir = line.strip()
            if input_dir:
                thread = threading.Thread(target=recursive, args=(input_dir,))
                thread.start()
                threads.append(thread)
        for thread in threads:
            thread.join()
elif args.input_dir:
    input_dir = args.input_dir
    recursive(input_dir)
else:
    print('Usage: python3 crawler.py [-d <input_directory> | -f <input_file>]')
