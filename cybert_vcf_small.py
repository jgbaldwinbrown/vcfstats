#!/usr/bin/env python3

import sys
import argparse
import subprocess

def parse_my_args():
    parser = argparse.ArgumentParser("Compute the Cochran-Mantel-Haenszel test on a VCF file")
    parser.add_argument("vcf", nargs="?", help="Input VCF file; default stdin")
    parser.add_argument("-C", "--control_names",  help="comma separated names of VCF columns to use as controls. This or -c required; cannot use both.", required=True)
    parser.add_argument("-T", "--test_names",  help="comma separated, 0-indexed VCF columns to use as test data. This or -t required; cannot use both.", required=True)
    parser.add_argument("-w", "--window_size",  help="Window size for sliding window cyber-t.", required=True)

    args = parser.parse_args()
    return(args)

def get_arg_vars(args):
    if args.vcf and args.vcf != "-":
        inpath = args.vcf
    else:
        inpath = "-"
    
    window_size = args.window_size

    cnames = False
    control = []
    controlnames = []
    if args.control_names:
        controlnames = [x for x in args.control_names.split(",")]
        clen = len(controlnames)
        cnames = True
    else:
        sys.exit("Must specify control columns.")
    
    tnames = False
    test = []
    testnames = []
    if args.test_names:
        testnames = [x for x in args.test_names.split(",")]
        tlen = len(testnames)
        tnames = True
    else:
        sys.exit("Must specify test columns.")
    
    if not clen == tlen:
        exit("unequal number of control and test pops!")
    return((inpath, control, test, controlnames, testnames, cnames, tnames, window_size))

def cybert_pipeline(inpath, control_names, test_names, window_size):
    sort_out = open('outfile.txt', 'wb', 0)
    all_names = control_names + test_names
    cnames_text = ",".join(control_names)
    tnames_text = ",".join(test_names)
    all_names_text = ",".join(all_names)
    
    cybert_vcf = subprocess.Popen(['cybert_vcf', "-", '-C', cnames_text, '-T', tnames_text, '-w', window_size], stdin=subprocess.PIPE)
    cybert_vcf_in = cybert_vcf.stdin
    if inpath == "-":
        subprocess.Popen(['vcf-subset', '-c', all_names_text] , stdout=cybert_vcf_in).communicate()
    else:
        subprocess.Popen(['vcf-subset', '-c', all_names_text, inpath] , stdout=cybert_vcf_in).communicate()
    cybert_vcf.communicate()
    
    # vcf_subset_in = subprocess.Popen(['vcf-subset', '-c', all_names_text] , stdin=subprocess.PIPE).stdin
    # subprocess.Popen(['cybert_vcf', inpath, '-C', cnames_text, '-T', tnames_text], stdout=vcf_subset_in).communicate()

def main():
    args = parse_my_args()

    inpath, control, test, control_names, test_names, cnames, tnames , window_size = get_arg_vars(args)
    
    cybert_pipeline(inpath, control_names, test_names, window_size)

if __name__ == "__main__":
    main()

