# Darkweb Crawler

> A Python script for crawling specific directories in the dark web and extracting file information.

## Prerequisites

- Python 3.x
- Necessary Python libraries: requests, BeautifulSoup, os, argparse, concurrent.futures, urllib.parse, pandas
- Darkweb proxy setup

## How to Use the Crawler

To crawl and create a file list, run the following command in your terminal:

```shell
python3 crawler.py -p "proof/"
```

or crawl a child directory

```shell
python3 crawler.py -p "proof/12Y Planning/"  
```

- `-p`: The path you want to crawl in the dark web.

After the script execution is completed, the extracted file information will be saved. For example, the file "./proof/file_list.txt" will contain a list of files from the crawled directory.

## How to Use the Downloader

To download the files from the `file_list.txt`, execute the following command in your terminal:

```shell
python3 downloader.py -l proof/file_list.txt
```

or download files from a specific directory

```shell
python3 downloader.py -l proof/12Y\ Planning/file_list.txt
```

- `-l`: Path of the file list to be downloaded.

The script will download all the files, maintaining the same directory structure as in file_list.

## How to Use the Converter

To convert the `file_list.txt` to `file_list.xlsx`, execute the following command in your terminal:

```shell
python3 converter.py -f ./proof/file_list.txt 
```

- `-f`: Path of the text file to be converted.

The script will create an xlsx file in the same directory as the input text file.

## How to Use the checker

To check the file list for any missing files, execute the following command in your terminal:

```shell
python3 checker.py -p ./proof
```

- `-p`: Path of the directory that you want to check.

After the script execution is completed, the extracted file information will be saved. For example, the file "./proof/file_list_check.txt" will contain a list of files from the directory that you want to check.

## Troubleshooting

- If you encounter connection issues, ensure your darkweb access is correctly configured.
- For any file permission errors, check if your script has the necessary read/write permissions in the execution directory.
