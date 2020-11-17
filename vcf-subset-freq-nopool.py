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

def parse_body(threshold, cov_threshold):
    for l in sys.stdin:
        l = l.rstrip('\n')
        sl = l.split('\t')
        entries = sl[9:]
        for entry in entries:
            thresh_ok = False
            cov_thresh_ok = True
            error_ok = True
            try:
                ad_str = entry.split(':')[1]
                ad = ad_str.split(',')
                ad1 = int(ad[0])
                ad2 = int(ad[1])
                minor = min(ad1,ad2)
                tot = ad1 + ad2
                frac = float(minor) / float(tot)
                if tot < cov_threshold:
                    cov_thresh_ok = False
                    break
                # if frac >= threshold:
                thresh_ok = True
            except (ZeroDivisionError, ValueError, TypeError, IndexError):
                error_ok=False
                break
        if thresh_ok and cov_thresh_ok and error_ok:
            print(l)

def main():
    threshold = float(sys.argv[1])
    cov_threshold = int(sys.argv[2])
    parse_header()
    parse_body(threshold, cov_threshold)

if __name__ == "__main__":
    main()
