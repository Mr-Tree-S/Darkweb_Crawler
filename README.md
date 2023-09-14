# crawler
>
> darkweb crawler

### Options

The script accepts the following command line arguments:

- `-d`: Input directory.

- `-f`: Input file containing directories.

### How to use crawler

To crawler a directory, run the following command in your terminal:

```shell
python crawler.py -d "Finance/Intern/Shan/02.Cheque Format"

```

If you have a text file containing a list of directories crawler, you can use the following command:

```shell
python crawler.py -f ./Finance.txt

```

After the script execution is completed, you will obtain the corresponding log files.
For example, in the Finance_log folder.

### How to use transform

If you need to transform log.txt into xlsx files.
write the corresponding file names into a txt, like Finance_log_name.txt,
Then execute the command,you will get xlsx files.

```shell
python transform.py -f ./Finance_log_name.txt

```
