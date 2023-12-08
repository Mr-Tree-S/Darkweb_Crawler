import pandas as pd
import argparse
import os


def transfer(directory):
    # 创建DataFrame
    df = pd.read_csv(directory, sep='|', header=None, names=['href', 'displayname', 'resourcetype', 'contentlength', 'lastmodified'])

    # 保存DataFrame为Excel文件
    output_file = os.path.splitext(input_file)[0] + ".xlsx"
    df.to_excel(output_file, index=False)

parser = argparse.ArgumentParser(description='transform txt to xlsx')
parser.add_argument('-f', '--input_file', type=str, help='Input file containing directories')
args = parser.parse_args()
# main
if args.input_file:
    with open(args.input_file, 'r') as file:
        input_file = args.input_file
        transfer(input_file)
else:
    print('Usage: python3 a.py [-d <input_directory> | -f <input_file>]')
