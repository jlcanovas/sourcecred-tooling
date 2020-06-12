#!/usr/bin/python
##
# Author: Javier Canovas (me@jlcanovas.es)
#

import sys
import csv

"""
Usage of this script
"""
USAGE = 'join_csvs.py FILE1.csv FILE2.csv'


def main(argv):
    if len(argv) == 0:
        print(USAGE)
        sys.exit(0)

    csv1_path = argv[0]
    csv1_map = {}
    with open(csv1_path, newline='') as csv1_file:
        csv1_reader = csv.reader(csv1_file, delimiter=',')
        for row in csv1_reader:
            if row[2] == "USERLIKE":
                csv1_map[row[3]] = row

    csv2_path = argv[1]
    csv2_map = {}
    with open(csv2_path, newline='') as csv2_file:
        csv2_reader = csv.reader(csv2_file, delimiter=',')
        for row in csv2_reader:
            if row[2] == "USERLIKE":
                csv2_map[row[3]] = row

    print(f'id,username,cred_coder,cred_coder_perc,cred_commenter,cred_commenter_perc,cred_total')
    for key in csv1_map:
        csv1_row = csv1_map[key]
        csv2_row = csv2_map[key]
        cred_coder = csv1_row[1]
        cred_commenter = csv2_row[1]
        cred_total = str(float(csv1_row[1])+float(csv2_row[1]))
        cred_coder_perc = str(float(cred_coder)/float(cred_total)) if float(cred_total) > 0 else 0
        cred_commenter_perc = str(float(cred_commenter)/float(cred_total)) if float(cred_total) > 0 else 0
        print(f'{csv1_row[0]},{key},{cred_coder},{cred_coder_perc},{cred_commenter},{cred_commenter_perc},{cred_total}')


if __name__ == "__main__":
    main(sys.argv[1:])