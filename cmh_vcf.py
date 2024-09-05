#!/usr/bin/env python3
#!/usr/bin/env /home/jbrown/.linuxbrew/bin/python3

import math
import vcf
import numpy as np
import statsmodels.api as sm
import sys
import argparse
import copy

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

def cmh_vcf(vcfin, control, test, control_names, test_names, cnames, tnames, outwriter):
    
    for index, record in enumerate(vcfin):
        calls = [call for call in record]
        
        if index == 0:
            if cnames:
                colnames = [x.sample for x in calls]
                control_cols = [colnames.index(control_name) for control_name in control_names]
            else:
                control_cols = control
            
            if tnames:
                colnames = [x.sample for x in calls]
                test_cols = [colnames.index(test_name) for test_name in test_names]
            else:
                test_cols = test
            
            tester = np.ndarray(shape=(2,2,len(control_cols)))
        
        try:
            for i in range(len(control_cols)):
                tester[0,0,i] = calls[control_cols[i]].data.AD[0]
                tester[0,1,i] = calls[control_cols[i]].data.AD[1]
                tester[1,0,i] = calls[test_cols[i]].data.AD[0]
                tester[1,1,i] = calls[test_cols[i]].data.AD[1]
            cmh = sm.stats.StratifiedTable(tester)
        except (ValueError, TypeError):
            cmh = "NA"
        writeout(cmh, record, outwriter)
        #print(cmh.summary())

        #control_ad0, control_ad1 = [calls.AD[:2] for i in control]
        #test_ad0, test_ad1 = [calls.AD[:2] for i in test]

def writeout(cmh, record, writer):
    #newrecord = copy.deepcopy(record)
    try:
        record.INFO["CMH"] = str(cmh.test_null_odds().pvalue)
    except ValueError:
        record.INFO["CMH"] = "NA"
    try:
        record.INFO["NLOG10CMH"] = str(-math.log10(cmh.test_null_odds().pvalue))
    except ValueError:
        record.INFO["NLOG10CMH"] = "NA"
    writer.write_record(record)

def main():
    args = parse_my_args()

    inconn, control, test, control_names, test_names, cnames, tnames = get_arg_vars(args)

    vcfin = vcf.Reader(inconn)
    outwriter = vcf.Writer(sys.stdout, vcfin)
    cmh_vcf(vcfin, control, test, control_names, test_names, cnames, tnames, outwriter)

    inconn.close()

if __name__ == "__main__":
    main()

#>>> for i in b:
#...     for j in i:
#...         try:print(j.data.AD)
