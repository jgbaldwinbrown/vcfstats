#!/usr/bin/env python3

import re
import os
import subprocess
import tempfile
import math
import sys
import argparse

def parse_my_args():
    parser = argparse.ArgumentParser("Compute the Cochran-Mantel-Haenszel test on a VCF file")
    parser.add_argument("vcf", nargs="?", help="Input VCF file; default stdin")
    parser.add_argument("-c", "--control",  help="comma separated, 0-indexed VCF columns to use as controls; required.")
    parser.add_argument("-t", "--test",  help="comma separated, 0-indexed VCF columns to use as test data; required.")
    parser.add_argument("-w", "--window_size",  help="Window size for sliding window cyber-t.", required=True)
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
    
    if not len(control) == len(test):
        exit("unequal number of control and test pops!")
    window_size = args.window_size
    return((inconn, control, test, window_size, controlnames, cnames, testnames, tnames))

def get_colnums(colres, sl):
    colnums = []
    for regex in colres:
        for i, col in enumerate(sl[9:]):
            colnum = i + 9
            if regex.match(col):
                colnums.append(colnum)
    return(colnums)

def counts2af(count1, count2):
    try:
        out = float(count1) / (float(count1) + float(count2))
    except ZeroDivisionError:
        out = "NA"
    return(out)

def textify_records(records, control_cols, test_cols):
    ncontrol = len(control_cols)
    ntest = len(test_cols)
    text = ""
    for record in records:
        sl = record.rstrip('\n').split('\t')
        #try:
        afs = []
        for i in range(len(control_cols)):
            control_col = control_cols[i]
            control_entry = sl[control_col]
            control_entry_list = control_entry.split(":")
            control_ad = control_entry_list[1]
            control_ad_list = control_ad.split(',')
            control_ad1 = control_ad_list[0]
            control_ad2 = control_ad_list[1]
            afs.append(counts2af(control_ad1, control_ad2))
        
        for i in range(len(test_cols)):
            test_col = test_cols[i]
            test_entry = sl[test_col]
            test_entry_list = test_entry.split(":")
            test_ad = test_entry_list[1]
            test_ad_list = test_ad.split(',')
            test_ad1 = test_ad_list[0]
            test_ad2 = test_ad_list[1]
            afs.append(counts2af(test_ad1, test_ad2))
        text = text + "\t".join(map(str,afs)) + "\n"
        #except:
        #    pass
    return(text)

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

def cybert_vcf(inconn, control, test, outconn, window_size, control_names, cnames, test_names, tnames):
    records = []
    records_txt = []
    test_cols, control_cols = parse_header(inconn, control_names, test_names)
    
    for index, record in enumerate(inconn):
        records.append(record)
        
        records_txt.append(textify_records([record], control_cols, test_cols))
    
    #records_txt = "\n".join(records)
    
    cybert_data = cybert_from_r(records_txt, len(control_cols), len(test_cols), window_size)
    write_it(records, cybert_data, outconn)

def cybert_from_r(records_txt, control_count, test_count, window_size):
    mytemp = tempfile.NamedTemporaryFile(mode="w+", delete=False)
    mytempname = mytemp.name
    mytemp.write("\t".join(["c" + str(x) for x in range(control_count)] + ["t" + str(x) for x in range(test_count)]) + "\n")
    for l in records_txt:
        mytemp.write(l)
    mytemp.close()
    
    out = subprocess.check_output([
        "./run_cybert.R",
        mytempname,
        "-e", str(test_count),
        "-c", str(control_count),
        "-w", str(window_size)
    ]).decode("utf-8")
    
    os.remove(mytempname)
    return(out)

def getpvals(cybert_data):
    pvals = []
    splitcyt = [x.split(' ') for x in cybert_data.split('\n')]
    pcol = splitcyt[0].index('"pVal"') + 1
    for l in splitcyt[1:]:
        try:
            pvals.append(float(l[pcol]))
        except IndexError:
            pass
    return(pvals)

def write_it(records, cybert_data, outconn):
    cybert_pvals = getpvals(cybert_data)
    for record, cyberp in zip(records, cybert_pvals):
        writeout(cyberp, record, outconn)

def writeout(cyberp, record, outconn):
    sl = record.rstrip('\n').split('\t')
    try:
        cyberpstr = str(cyberp)
    except (ValueError, AttributeError):
        cyberpstr = "NA"
    try:
        nlog10cyberpstr = str(-math.log10(float(cyberp)))
    except (ValueError, AttributeError):
        nlog10cyberpstr = "NA"
    if sl[7] == ".":
        sl[7] = "CYBERP=" + cyberpstr
    else:
        sl[7] = sl[7] + ";CYBERP=" + cyberpstr
    sl[7] = sl[7] + ";NLOG10CYBERP=" + nlog10cyberpstr
    outconn.write("\t".join(sl) + "\n")


def main():
    args = parse_my_args()

    inconn, control, test, window_size, control_names, cnames, test_names, tnames = get_arg_vars(args)
    outconn = sys.stdout

    cybert_vcf(inconn, control, test, outconn, window_size, control_names, cnames, test_names, tnames)

    inconn.close()

if __name__ == "__main__":
    main()

