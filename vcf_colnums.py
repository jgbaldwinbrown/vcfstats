#!/usr/bin/env python3

import sys
import re
import subprocess
import os

def get_colnums(colres, sl):
    colnums = []
    for regex in colres:
        for i, col in enumerate(sl[9:]):
            colnum = i
            if regex.match(col):
                colnums.append(colnum)
    return(colnums)

def parse_header(com_cols):
    colnames = com_cols.split(",")
    colres = []
    for colname in colnames:
        colres.append(re.compile(colname))
    for l in sys.stdin:
        l=l.rstrip('\n')
        if l[:6] == "#CHROM":
            sl = l.split('\t')
            colnums = get_colnums(colres, sl)
            colnums_fix = [x-1 for x in colnums]
            break
    return(colnums)

def print_cols(cols):
    print(",".join(map(str, cols)))

def main():
    cols = parse_header(sys.argv[1])
    print_cols(cols)

if __name__ == "__main__":
    main()
