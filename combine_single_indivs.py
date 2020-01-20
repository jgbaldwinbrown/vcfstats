#!/usr/bin/env python3

import re
import collections
import vcf
import sys
import argparse
import copy

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

def combine_vcf(vcfin, name, outwriter):
    regex = re.compile(r"[/|]")
    for record in vcfin:
        calls = [call for call in record]
        ad1 = 0
        ad2 = 0
        for call in calls:
            callgt = regex.split(call["GT"])
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
        writeout(gt, ad1, ad2, name, record, outwriter)
        #print(cmh.summary())

        #control_ad0, control_ad1 = [calls.AD[:2] for i in control]
        #test_ad0, test_ad1 = [calls.AD[:2] for i in test]

def writeout(gt, ad1, ad2, name, record, writer):
    newrecord = copy.deepcopy(record)
    newrecord.samples = []
    CallData = collections.namedtuple("CallData", ["GT", "AD"])
    mycalldat = CallData(GT = str(gt), AD = [str(ad1), str(ad2)])
    newrecord.samples.append(vcf.model._Call(newrecord, name, mycalldat))
    writer.write_record(newrecord)

def main():
    args = parse_my_args()

    inconn, name = get_arg_vars(args)

    vcfin = vcf.Reader(inconn)
    outwriter = vcf.Writer(sys.stdout, vcfin)
    combine_vcf(vcfin, name, outwriter)

    inconn.close()

if __name__ == "__main__":
    main()

#>>> for i in b:
#...     for j in i:
#...         try:print(j.data.AD)
