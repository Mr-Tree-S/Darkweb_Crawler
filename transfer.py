import pandas as pd
import argparse
import threading


def transfer(directory):
    # 读取文本文件并分割成列表
    with open(directory, 'r') as file:
        lines = file.readlines()

    # 解析每一行并构建DataFrame
    data = []
    for line in lines:
        parts = line.strip().split('|')
        Type = parts[1]
        if Type != "folder":
            Type = "file"
        Path = parts[2]
        Depth = Path.count('/')
        Ext = parts[1]
        if Type == "folder":
            Ext = ""
        Size = parts[3]
        Date = parts[4]
        data.append([Type, Path, Depth, Ext, Size, Date])

    # 创建DataFrame
    df = pd.DataFrame(data, columns=['Type', 'Path', 'Depth', 'Ext', 'Size', 'Date'])

    # 保存DataFrame为Excel文件
    df.to_excel(directory + ".xlsx", index=False)

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
                thread = threading.Thread(target=transfer, args=(input_dir,))
                thread.start()
                threads.append(thread)
        for thread in threads:
            thread.join()
elif args.input_dir:
    input_dir = args.input_dir
    transfer(input_dir)
else:
    print('Usage: python3 a.py [-d <input_directory> | -f <input_file>]')


