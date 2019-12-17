#!/usr/bin/env python3

import sys
import argparse
import subprocess

def parse_my_args():
    parser = argparse.ArgumentParser("Compute the Cochran-Mantel-Haenszel test on a VCF file")
    parser.add_argument("vcf", nargs="?", help="Input VCF file; default stdin")
    parser.add_argument("-C", "--control_names",  help="comma separated names of VCF columns to use as controls. This or -c required; cannot use both.")
    parser.add_argument("-T", "--test_names",  help="comma separated, 0-indexed VCF columns to use as test data. This or -t required; cannot use both.")

    args = parser.parse_args()
    return(args)

def get_arg_vars(args):
    if args.vcf:
        inpath = args.vcf
    else:
        inpath = "-"

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
    return((inpath, control, test, controlnames, testnames, cnames, tnames))

def cmh_pipeline(inpath, control_names, test_names):
    sort_out = open('outfile.txt', 'wb', 0)
    all_names = control_names + test_names
    cnames_text = ",".join(control_names)
    tnames_text = ",".join(test_names)
    all_names_text = ",".join(all_names)
    
    cmh_vcf = subprocess.Popen(['cmh_vcf', "-", '-C', cnames_text, '-T', tnames_text], stdin=subprocess.PIPE)
    cmh_vcf_in = cmh_vcf.stdin
    if inpath == "-":
        subprocess.Popen(['vcf-subset', '-c', all_names_text] , stdout=cmh_vcf_in).communicate()
    else:
        subprocess.Popen(['vcf-subset', '-c', all_names_text, inpath] , stdout=cmh_vcf_in).communicate()
    cmh_vcf.communicate()
    
    # vcf_subset_in = subprocess.Popen(['vcf-subset', '-c', all_names_text] , stdin=subprocess.PIPE).stdin
    # subprocess.Popen(['cmh_vcf', inpath, '-C', cnames_text, '-T', tnames_text], stdout=vcf_subset_in).communicate()

def main():
    args = parse_my_args()

    inpath, control, test, control_names, test_names, cnames, tnames = get_arg_vars(args)
    
    cmh_pipeline(inpath, control_names, test_names)

if __name__ == "__main__":
    main()

#usage: Compute the Cochran-Mantel-Haenszel test on a VCF file
#       [-h] [-c CONTROL] [-t TEST] [-C CONTROL_NAMES] [-T TEST_NAMES] [vcf]
#
#positional arguments:
#  vcf                   Input VCF file; default stdin
#
#optional arguments:
#  -h, --help            show this help message and exit
#  -c CONTROL, --control CONTROL
#                        comma separated, 0-indexed VCF columns to use as
#                        controls. This or -C required; cannot use both.
#  -t TEST, --test TEST  comma separated, 0-indexed VCF columns to use as test
#                        data. This or -T required; cannot use both.
#  -C CONTROL_NAMES, --control_names CONTROL_NAMES
#                        comma separated names of VCF columns to use as
#                        controls. This or -c required; cannot use both.
#  -T TEST_NAMES, --test_names TEST_NAMES
#                        comma separated, 0-indexed VCF columns to use as test
#                        data. This or -t required; cannot use both.
#Usage: vcf-subset [OPTIONS] in.vcf.gz > out.vcf
#Options:
#   -a, --trim-alt-alleles           Remove alternate alleles if not found in the subset
#   -c, --columns <string>           File or comma-separated list of columns to keep in the vcf file. If file, one column per row
#   -e, --exclude-ref                Exclude rows not containing variants.
#   -f, --force                      Proceed anyway even if VCF does not contain some of the samples.
#   -p, --private                    Print only rows where only the subset columns carry an alternate allele.
#   -r, --replace-with-ref           Replace the excluded types with reference allele instead of dot.
#   -t, --type <list>                Comma-separated list of variant types to include: ref,SNPs,indels,MNPs,other.
#   -u, --keep-uncalled              Do not exclude rows without calls.
#   -h, -?, --help                   This help message.
#Examples:
#   cat in.vcf | vcf-subset -r -t indels -e -c SAMPLE1 > out.vcf

