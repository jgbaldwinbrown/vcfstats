#!/usr/bin/env python3

import os
import subprocess
import tempfile
import math
import vcf
import sys
import argparse

def parse_my_args():
    parser = argparse.ArgumentParser("Compute the Cochran-Mantel-Haenszel test on a VCF file")
    parser.add_argument("vcf", nargs="?", help="Input VCF file; default stdin")
    parser.add_argument("-c", "--control",  help="comma separated, 0-indexed VCF columns to use as controls; required.", required=True)
    parser.add_argument("-t", "--test",  help="comma separated, 0-indexed VCF columns to use as test data; required.", required=True)
    parser.add_argument("-w", "--window_size",  help="Window size for sliding window cyber-t.", required=True)

    args = parser.parse_args()
    return(args)

def get_arg_vars(args):
    if args.vcf:
        inconn = open(args.vcf, "r")
    else:
        inconn = sys.stdin

    control = [int(x) for x in args.control.split(",")]
    test = [int(x) for x in args.test.split(",")]
    if not len(control) == len(test):
        exit("unequal number of control and test pops!")
    window_size = args.window_size
    return((inconn, control, test, window_size))

def counts2af(count1, count2):
    try:
        out = float(count1) / (float(count1) + float(count2))
    except ZeroDivisionError:
        out = "NA"
    return(out)

def textify_records(records, control, test):
    ncontrol = len(control)
    ntest = len(test)
    text = "\t".join(["c" + str(x) for x in range(ncontrol)] + ["t" + str(x) for x in range(ntest)]) + "\n"
    for record in records:
        afs = []
        calls = [call for call in record]
        for i in control:
            count1 = int(calls[i].data.AD[0])
            count2 = int(calls[i].data.AD[1])
            afs.append(counts2af(count1, count2))
        for i in test:
            count1 = int(calls[i].data.AD[0])
            count2 = int(calls[i].data.AD[1])
            afs.append(counts2af(count1, count2))
        text = text + "\t".join(map(str,afs)) + "\n"
    return(text)

def cybert_vcf(vcfin, control, test, outwriter, window_size):
    records = []
    
    for record in vcfin:
        records.append(record)
    
    records_txt = textify_records(records, control, test)
    
    cybert_data = cybert_from_r(records_txt, len(control), len(test), window_size)
    write_it(records, cybert_data, outwriter)

def cybert_from_r(records_txt, control_count, test_count, window_size):
    mytemp = tempfile.NamedTemporaryFile(mode="w+", delete=False)
    mytempname = mytemp.name
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

def write_it(records, cybert_data, writer):
    cybert_pvals = getpvals(cybert_data)
    for record, cyberp in zip(records, cybert_pvals):
        writeout(cyberp, record, writer)

def writeout(cyberp, record, writer):
    #newrecord = copy.deepcopy(record)
    record.INFO["CYBERP"] = str(cyberp)
    record.INFO["NLOG10CYBERP"] = str(-math.log10(cyberp))
    writer.write_record(record)

def main():
    args = parse_my_args()

    inconn, control, test, window_size = get_arg_vars(args)

    vcfin = vcf.Reader(inconn)
    outwriter = vcf.Writer(sys.stdout, vcfin)
    cybert_vcf(vcfin, control, test, outwriter, window_size)

    inconn.close()

if __name__ == "__main__":
    main()

