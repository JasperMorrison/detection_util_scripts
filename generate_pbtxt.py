import pandas as pd
import argparse
from functools import cmp_to_key

def pbtxt_from_classlist(l, pbtxt_path):
    pbtxt_text = ''

    for i, c in enumerate(l):
        pbtxt_text += 'item {\n    id: ' + str(
            i + 1) + '\n    display_name: "' + c + '"\n}\n\n'

    with open(pbtxt_path, "w+") as pbtxt_file:
        pbtxt_file.write(pbtxt_text)

'''
sort by end str
'''
def my_cmp(a, b):
    a_l = a.split('-')
    b_l = b.split('-')
    if len(a_l) == 2 and a_l[1].isdigit() and len(b_l) == 2 and b_l[1].isdigit():
        a = a_l[1]
        b = b_l[1]
    if a > b:
        return 1
    elif a<b:
        return -1
    else:
        return 0

def pbtxt_from_csv(csv_path, pbtxt_path):
    class_list = list(pd.read_csv(csv_path)['class'].unique())
    sorted(class_list, key=cmp_to_key(my_cmp))

    pbtxt_from_classlist(class_list, pbtxt_path)


def pbtxt_from_txt(txt_path, pbtxt_path):
    # read txt into a list, splitting by newlines
    data = [
        l.rstrip('\n').strip()
        for l in open(txt_path, 'r', encoding='utf-8-sig')
    ]

    data = [l for l in data if len(l) > 0]

    pbtxt_from_classlist(data, pbtxt_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=
        'Reads all XML files, generated by labelImg, from a directory and generates a single CSV file')
    parser.add_argument(
        'input_type',
        choices=['csv', 'txt'],
        help=
        'type of input file (csv with at least one \'class\' column or txt with one class name by line)'
    )
    parser.add_argument(
        'input_file',
        metavar='input_file',
        type=str,
        help='Path to the input txt or csv file')
    parser.add_argument(
        'output_file',
        metavar='output_file',
        type=str,
        help='Path where the .pbtxt output will be created')

    args = parser.parse_args()

    if args.input_type == 'csv':
        pbtxt_from_csv(args.input_file, args.output_file)
    elif args.input_type == 'txt':
        pbtxt_from_txt(args.input_file, args.output_file)