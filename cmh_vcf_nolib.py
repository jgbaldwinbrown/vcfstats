#!/usr/bin/env python3

import re
import math
import numpy as np
import statsmodels.api as sm
import sys
import argparse

def parse_my_args():
    parser = argparse.ArgumentParser("Compute the Cochran-Mantel-Haenszel test on a VCF file")
    parser.add_argument("vcf", nargs="?", help="Input VCF file; default stdin")
    parser.add_argument("-c", "--control",  help="comma separated, 0-indexed VCF columns to use as controls. This or -C required; cannot use both.")
    parser.add_argument("-t", "--test",  help="comma separated, 0-indexed VCF columns to use as test data. This or -T required; cannot use both.")
    parser.add_argument("-C", "--control_names",  help="comma separated names of VCF columns to use as controls. This or -c required; cannot use both.")
    parser.add_argument("-T", "--test_names",  help="comma separated, 0-indexed VCF columns to use as test data. This or -t required; cannot use both.")

    args = parser.parse_args()
    return(args)

def get_arg_vars(args):
    if args.vcf and args.vcf != "-":
        inconn = open(args.vcf, "r")
    else:
        inconn = sys.stdin

    cnames = False
    control = []
    controlnames = []
    if args.control:
        control = [int(x) for x in args.control.split(",")]
        clen = len(control)
    elif args.control_names:
        controlnames = [x for x in args.control_names.split(",")]
        clen = len(controlnames)
        cnames = True
    else:
        sys.exit("Must specify control columns.")
    
    tnames = False
    test = []
    testnames = []
    if args.test:
        test = [int(x) for x in args.test.split(",")]
        tlen = len(test)
    elif args.test_names:
        testnames = [x for x in args.test_names.split(",")]
        tlen = len(testnames)
        tnames = True
    else:
        sys.exit("Must specify test columns.")
    
    if not clen == tlen:
        exit("unequal number of control and test pops!")
    return((inconn, control, test, controlnames, testnames, cnames, tnames))

def get_colnums(colres, sl):
    colnums = []
    for regex in colres:
        for i, col in enumerate(sl[9:]):
            colnum = i + 9
            if regex.match(col):
                colnums.append(colnum)
    return(colnums)

def parse_header(inconn, control_colnames, test_colnames):
    test_colres = []
    control_colres = []
    for colname in test_colnames:
        test_colres.append(re.compile(colname))
    for colname in control_colnames:
        control_colres.append(re.compile(colname))
    while True:
        l = inconn.readline()
        l = l
        l=l.rstrip('\n')
        print(l)
        if l[:6] == "#CHROM":
            sl = l.split('\t')
            test_colnums = get_colnums(test_colres, sl)
            control_colnums = get_colnums(control_colres, sl)
            break
    #sys.stdout.flush()
    #sys.stdin.flush()
    return(test_colnums, control_colnums)

def cmh_vcf(inconn, control, test, control_names, test_names, cnames, tnames, outconn):
    
    test_cols, control_cols = parse_header(inconn, control_names, test_names)
    tester = np.ndarray(shape=(2,2,len(control_cols)))
    
    for index, l in enumerate(inconn):
        sl = l.rstrip('\n').split('\t')
        
        try:
            for i in range(len(control_cols)):
                control_col = control_cols[i]
                control_entry = sl[control_col]
                control_entry_list = control_entry.split(":")
                control_ad = control_entry_list[1]
                control_ad_list = control_ad.split(',')
                control_ad1 = control_ad_list[0]
                control_ad2 = control_ad_list[1]
                tester[0,0,i] = int(control_ad1)
                tester[0,1,i] = int(control_ad2)
                
                test_col = test_cols[i]
                test_entry = sl[test_col]
                test_entry_list = test_entry.split(":")
                test_ad = test_entry_list[1]
                test_ad_list = test_ad.split(',')
                test_ad1 = test_ad_list[0]
                test_ad2 = test_ad_list[1]
                tester[1,0,i] = int(test_ad1)
                tester[1,1,i] = int(test_ad2)
                #tester[0,0,i] = int(sl[control_cols[i]].split(":")[1].split(",")[0])
                #tester[0,1,i] = int(sl[control_cols[i]].split(":")[1].split(",")[1])
                #tester[1,0,i] = int(sl[test_cols[i]].split(":")[1].split(",")[0])
                #tester[1,1,i] = int(sl[test_cols[i]].split(":")[1].split(",")[1])
            cmh = sm.stats.StratifiedTable(tester)
        except (ValueError, TypeError, IndexError):
            cmh = "NA"
        writeout(cmh, sl, sys.stdout)
        #print(cmh.summary())

        #control_ad0, control_ad1 = [calls.AD[:2] for i in control]
        #test_ad0, test_ad1 = [calls.AD[:2] for i in test]

def writeout(cmh, sl, outconn):
    try:
        cmhstr = str(cmh.test_null_odds().pvalue)
    except (ValueError, AttributeError):
        cmhstr = "NA"
    try:
        nlog10cmhstr = str(-math.log10(cmh.test_null_odds().pvalue))
    except (ValueError, AttributeError):
        nlog10cmhstr = "NA"
    if sl[7] == ".":
        sl[7] = "CMH=" + cmhstr
    else:
        sl[7] = sl[7] + ";CMH=" + cmhstr
    sl[7] = sl[7] + ";NLOG10CMH=" + nlog10cmhstr
    outconn.write("\t".join(sl) + "\n")

def main():
    args = parse_my_args()

    inconn, control, test, control_names, test_names, cnames, tnames = get_arg_vars(args)
    outconn = sys.stdout

    cmh_vcf(inconn, control, test, control_names, test_names, cnames, tnames, outconn)

    inconn.close()

if __name__ == "__main__":
    main()

#>>> for i in b:
#...     for j in i:
#...         try:print(j.data.AD)
