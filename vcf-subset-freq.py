#!/usr/bin/env python3

import sys
import re
import subprocess
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser("Filter VCF file by pool allele frequencies and coverages")
    parser.add_argument("-f", "--freq", help="Frequency threshold (default=None)", default = None, type=float)
    parser.add_argument("-c", "--cov", help="Coverage threshold (default=None)", default = None, type=int)
    parser.add_argument("-b", "--bed_output", help="Output a bed file of all good sites (default=vcf output)", action="store_true")
    args = parser.parse_args()
    return(args)
    # threshold = float(sys.argv[1])
    # cov_threshold = int(sys.argv[2])

def parse_header(args):
    for l in sys.stdin:
        l=l.rstrip('\n')
        if not args.bed_output:
            print(l)
        if l[:6] == "#CHROM":
            break

def output_entry(line, args):
    if not args.bed_output:
        print(line)
    else:
        sl = line.split('\t')
        print(sl[0], str(int(sl[1])-1), sl[1], sep="\t")

def parse_body(args):
    for l in sys.stdin:
        l = l.rstrip('\n')
        sl = l.split('\t')
        entries = sl[9:]
        if args.freq:
            internal_freq_threshold = args.freq
        else:
            internal_freq_threshold = -1.0
        if args.cov:
            internal_cov_threshold = args.cov
        else:
            internal_cov_threshold = -10
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
                if tot < internal_cov_threshold:
                    cov_thresh_ok = False
                    break
                if frac >= internal_freq_threshold:
                    thresh_ok = True
            except (ZeroDivisionError, ValueError, TypeError, IndexError):
                error_ok=False
                break
        if thresh_ok and cov_thresh_ok and error_ok:
            output_entry(l, args)

def main():
    args = parse_arguments()
    parse_header(args)
    parse_body(args)

if __name__ == "__main__":
    main()
