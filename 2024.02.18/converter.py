import pandas as pd
import os
import argparse

def transfer(input_file):
    # Read text file into DataFrame and specify column names
    df = pd.read_csv(input_file, sep='|', header=None, names=['file_path', 'name', 'file_type', 'file_type_detail', 'date_time', 'file_size'])

    # Convert DataFrame to Excel format
    output_file = os.path.splitext(input_file)[0] + ".xlsx"
    df.to_excel(output_file, index=False)

# Set up argument parser
parser = argparse.ArgumentParser(description='Convert text to xlsx format')
parser.add_argument('-f', '--file', type=str, help='Input file path')
args = parser.parse_args()

# Execute transformation
if args.file:
    transfer(args.file)
else:
    print('Usage: python3 converter.py -f <file>')
