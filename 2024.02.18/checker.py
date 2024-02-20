import os
import argparse
from datetime import datetime


def list_files(input_dir_path, output_file_path):
    for root, dirs, files in os.walk(input_dir_path):
        for file in files:
            path = os.path.join(root, file)
            file_path = path.split("/proof/")[1]
            file_path = "proof/" + file_path
            name = os.path.basename(path)
            file_type = "file"
            file_type_detail = name.split(".")[-1]
            date_time = datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M:%S')
            file_size = str(os.path.getsize(path))
            # Prepare data row
            delimiter = "|"
            data_row = delimiter.join([file_path, name, file_type, file_type_detail, date_time, file_size])
            # print("--------------------")
            print(data_row)
            # print("--------------------")

            with open(output_file_path, 'a') as file:
                file.write(data_row + "\n")


# Parse arguments
parser = argparse.ArgumentParser(description='Darkweb file list checker')
parser.add_argument('-p', '--path', type=str, help='Input path to be checked')
args = parser.parse_args()

# Main execution
if args.path:
    input_dir_path = args.path
    output_file_name = "file_list_check.txt"
    output_file_path = os.path.join(input_dir_path, output_file_name)
    list_files(input_dir_path, output_file_path)
else:
    # Display usage information
    print('Usage: python3 checker.py -p <path>')
