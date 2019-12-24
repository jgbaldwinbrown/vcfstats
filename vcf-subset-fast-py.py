#!/usr/bin/env python3

import sys
import re
import subprocess

def get_colnums(colres, sl):
    colnums = list(range(0, 9))
    for regex in colres:
        for i, col in enumerate(sl[9:]):
            colnum = i + 8
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
        print(l)
        if l[:6] == "#CHROM":
            sl = l.split('\t')
            colnums = get_colnums(colres, sl)
            break
    return(colnums)

def parse_body(cols):
    for l in sys.stdin:
        sl = l.rstrip('\n').split('\t')
        out = []
        for col in cols:
            out.append(sl[col])
        print("\t".join(out))

def main():
    cols = parse_header(sys.argv[1])
    parse_body(cols)

if __name__ == "__main__":
    main()
