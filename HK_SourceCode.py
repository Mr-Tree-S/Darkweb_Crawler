import requests, json, urllib.parse, subprocess, re, os
from bs4 import BeautifulSoup
import time
import logging
FORMAT = '%(asctime)s %(levelname)s %(message)s'
logger = logging.basicConfig(filename="./crawler_log.txt", level=logging.INFO, format=FORMAT)
# pip install pysocks

# for page_no in range(0, 100):
#     cmd = "torsocks curl 'http://aeey7hxzgl6zowiwhteo5xjbf6sb36tkbn5hptykgmbsjrbiygv4c4id.onion/ajax.php' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Accept-Language: en-US,en;q=0.9' -H 'Connection: keep-alive' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Cookie: PHPSESSID=8c344vcesol3e50qkn7bcu31v5; visit=enwOvkX4%7C' -H 'Origin: http://aeey7hxzgl6zowiwhteo5xjbf6sb36tkbn5hptykgmbsjrbiygv4c4id.onion' -H 'Referer: http://aeey7hxzgl6zowiwhteo5xjbf6sb36tkbn5hptykgmbsjrbiygv4c4id.onion/?id=enwOvkX4&dir=.' -H 'Sec-GPC: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' -H 'X-Requested-With: XMLHttpRequest' --data-raw 'q=&dir=Project&page=10' --compressed --insecure"
#     cmd = cmd.replace("@PAGE@",str(page_no))
#     print(cmd)
#     a = os.popen(cmd).read()
#     jsonObj = json.loads(a)
#     if jsonObj["html"] == "":
#         break

# Edit this
done_items = ["HR/4.   Staff Log",
"HR/3.   HR Operations",
"HR/000 Adonis - Job openings (with expected salary expose to c-level)",
"HR/Variable Pay",
"HR/10. Organisational Chart",
"HR/Staffing",
"HR/15. SharePoint EE Toolkit",
"HR/6.   Budget",
"HR/1.   Compensation and Benefits",
"HR/2.   Recruitment",
"HR/2.   Recruitment",
"HR/11. Performance Management",
"HR/7.   HR Projects",
"HR/2.   Recruitment",
"HR/11. Performance Management",
"HR/5.   Policies & Procedures",
"HR/Payroll",
"HR/Annual report",
"HR/13. Engagement",
"HR/Others",
"HR/9.   Manpower Planning",
"HR/Pay Review",
"HR/8.   Management and Committees Meetings"]


def recursive(directory, root):
    for page_no in range(0, 100):
        cmd = "torsocks curl 'http://aeey7hxzgl6zowiwhteo5xjbf6sb36tkbn5hptykgmbsjrbiygv4c4id.onion/ajax.php' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Accept-Language: en-US,en;q=0.9' -H 'Connection: keep-alive' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Cookie: PHPSESSID=8c344vcesol3e50qkn7bcu31v5; visit=enwOvkX4%7C' -H 'Origin: http://aeey7hxzgl6zowiwhteo5xjbf6sb36tkbn5hptykgmbsjrbiygv4c4id.onion' -H 'Referer: http://aeey7hxzgl6zowiwhteo5xjbf6sb36tkbn5hptykgmbsjrbiygv4c4id.onion/?id=enwOvkX4&dir=.' -H 'Sec-GPC: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' -H 'X-Requested-With: XMLHttpRequest' --data-raw 'q=&dir=@DIR@&page=@PAGE@' --compressed --insecure"
        #logging.info("doing... " + cmd)
        cmd = cmd.replace("@PAGE@", str(page_no))
        cmd = cmd.replace("@DIR@", directory)
        logging.info("doing..." + directory + " " + str(page_no))
        # print(cmd)
        a = os.popen(cmd).read()
        jsonObj = json.loads(a)
        # print(jsonObj["html"])
        if jsonObj["html"] == "":
            break

        soup = BeautifulSoup(jsonObj["html"], "html.parser")
        itemList = soup.find_all('tr')
        for item in itemList:
            cells = item.find_all('td')

            size = cells[2].text
            date = cells[3].text
            type = ""
            itemName = ""

            if cells[0].find('input') == None:
                type = "folder"
                itemName = cells[1].get('dir') if cells[1].get('dir') != None else ""
                if itemName != "" and itemName != "." and itemName != " .." and itemName != "Leasing" and itemName not in done_items:
                    logging.info(type+"|"+itemName+"|"+size+"|"+date)
                    done_items.append(itemName)
                    itemName = urllib.parse.quote(itemName)
                    recursive(itemName, root)
            else:
                type = "file"
                itemName = cells[1].get('file') if cells[1].get('file') != None else ""
                logging.info(type+"|"+itemName+"|"+size+"|"+date)

# Edit this
recursive("HR", "HR")