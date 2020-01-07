#!/usr/bin/env python3

import sys
import re
import subprocess

def parse_header():
    for l in sys.stdin:
        l=l.rstrip('\n')
        print(l)
        if l[:6] == "#CHROM":
            break

def parse_body(threshold):
    for l in sys.stdin:
        l = l.rstrip('\n')
        sl = l.split('\t')
        entries = sl[9:]
        ok = False
        for entry in entries:
            ad_str = entry.split(':')[1]
            ad = ad_str.split(',')
            ad1 = int(ad[0])
            ad2 = int(ad[1])
            minor = min(ad1,ad2)
            tot = ad1 + ad2
            frac = float(minor) / float(tot)
            if frac >= threshold:
                ok = True
        if ok:
            print(l)

def main():
    threshold = float(sys.argv[1])
    parse_header()
    parse_body(threshold)

if __name__ == "__main__":
    main()
