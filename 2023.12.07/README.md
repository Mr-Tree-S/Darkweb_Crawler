# Darkweb Crawler

> A Python script for crawling specific directories in the dark web and extracting file information.

## Prerequisites

- Python 3.x
- Necessary Python libraries: requests, xml.etree.ElementTree, os, argparse
- Darkweb access setup

## How to Use the Crawler

To crawl and create a file list, run the following command in your terminal:

```shell
python3 crawler.py -p "HKG/"
```

- `-p`: The path you want to crawl in the dark web.

After the script execution is completed, the extracted file information will be saved. For example, the file "./HKG/file_name_list.txt" will contain a list of files from the crawled directory.

## How to Use the Transform Script

To convert the generated `file_name_list.txt` into an Excel file, execute the following command in your terminal:

```shell
python3 transform.py -f ./file_name_list.txt
```

- `-f`: Path of the text file to be transformed into an Excel file.

The script will create an Excel file in the same directory as the input text file.

## Troubleshooting

- If you encounter connection issues, ensure your darkweb access is correctly configured.
- For any file permission errors, check if your script has the necessary read/write permissions in the execution directory.
