#!/usr/bin/env python3

import sys
import re
import subprocess
import os

def get_colnums(colres, sl):
    colnums = list(range(1, 10))
    for regex in colres:
        for i, col in enumerate(sl[9:]):
            colnum = i + 10
            if regex.match(col):
                colnums.append(colnum)
    return(colnums)

def parse_header(com_cols):
    sys.stdin = os.fdopen(sys.stdin.fileno(), 'rb', buffering=0)
    colnames = com_cols.split(",")
    colres = []
    for colname in colnames:
        colres.append(re.compile(colname))
    #for l in sys.stdin:
    while True:
        l = sys.stdin.readline()
        l = l.decode('utf-8')
        l=l.rstrip('\n')
        if l[:6] == "#CHROM":
            sl = l.split('\t')
            colnums = get_colnums(colres, sl)
            colnums_fix = [x-1 for x in colnums]
            print("\t".join([sl[x] for x in colnums_fix]))
            break
        print(l)
    sys.stdout.flush()
    sys.stdin.flush()
    return(colnums)

def parse_body(cols):
    col_vars = ["$" + str(col) for col in cols]
    awk_command = '{print(' + ",".join(col_vars) + ')}'
    command = ["mawk", "-F", "\t", "-v", "OFS=\t", awk_command]
    cutrun = subprocess.Popen(command, shell=False)
    cutrun.communicate()

def main():
    cols = parse_header(sys.argv[1])
    parse_body(cols)

if __name__ == "__main__":
    main()
