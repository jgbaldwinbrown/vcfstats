#!/usr/bin/env python3

import re
import sys
import argparse

def parse_my_args():
    parser = argparse.ArgumentParser("Combines a VCF of individual calls into one large VCF for population.")
    parser.add_argument("vcf", nargs="?", help="Input VCF file; default stdin.")
    parser.add_argument("-n", "--name", help="name of combined population.", required=True)

    args = parser.parse_args()
    return(args)

def get_arg_vars(args):
    if args.vcf:
        inconn = open(args.vcf, "r")
    else:
        inconn = sys.stdin
    name = args.name
    return(inconn, name)

def combine_vcf(inconn, name, outconn):
    regex = re.compile(r"[/|]")
    for line in inconn:
        line = line.rstrip('\n')
        record = line.split('\t')
        if line[0] == "#" and line[1] != "C":
            outconn.write(line + "\n")
            continue
        if line[:6] == "#CHROM":
            out = record[:9]
            out.append(name)
            outconn.write("\t".join(map(str, out)))
            continue
        calls = record[9:]
        ad1 = 0
        ad2 = 0
        for call in calls:
            callgt_str = call.split(":")[0]
            callgt = regex.split(callgt_str)
            if len(callgt) == 1:
                inc = 2
            else:
                inc = 1
            for i in callgt:
                if i=="0":
                    ad1 += inc
                if i=="1":
                    ad2 += inc
        if ad1 >0 and ad2 > 0:
            gt = "0|1"
        elif ad2 > 0:
            gt = "1"
        else:
            gt = "0"
        writeout(gt, ad1, ad2, name, record, outconn)

        #control_ad0, control_ad1 = [calls.AD[:2] for i in control]
        #test_ad0, test_ad1 = [calls.AD[:2] for i in test]

def writeout(gt, ad1, ad2, name, record, outconn):
    ads = str(ad1) + "," + str(ad2)
    call = str(gt) + ":" + ads
    out = record[:9]
    out[8] = "GT:AD"
    out.append(str(call))
    outconn.write("\t".join(map(str, out)) + "\n")

def main():
    args = parse_my_args()

    inconn, name = get_arg_vars(args)

    combine_vcf(inconn, name, sys.stdout)

    inconn.close()

if __name__ == "__main__":
    main()
