#!/usr/bin/env python3

import re
import sys
import argparse

# globals:
ident = ["a","t","g","c","n","0"]

# functions:

def parse_my_args():
    parser = argparse.ArgumentParser("Compute the Cochran-Mantel-Haenszel test on a VCF file")
    parser.add_argument("vcf", nargs="?", help="Input VCF file; default stdin")
    parser.add_argument("-c", "--columns",  help="comma separated, 0-indexed VCF columns to use as controls (default = all); not compatible with -C.")
    parser.add_argument("-C", "--column_names",  help="comma separated names of VCF columns to use as controls (default = all); not compatible with -c.")

    args = parser.parse_args()
    return(args)

def get_arg_vars(args):
    if args.vcf and args.vcf != "-":
        inconn = open(args.vcf, "r")
    else:
        inconn = sys.stdin

    cnames = False
    col = []
    colnames = []
    if args.columns:
        col = [int(x) for x in args.columns.split(",")]
    elif args.column_names:
        colnames = [x for x in args.column_names.split(",")]
        cnames = True
    
    return((inconn, col, colnames, cnames))

def get_colnums(colres, sl):
    colnums = []
    for regex in colres:
        for i, col in enumerate(sl[9:]):
            colnum = i + 9
            if regex.match(col):
                colnums.append(colnum)
    return(colnums)

def parse_header(inconn, colnames, cnames):
    colres = []
    for colname in colnames:
        colres.append(re.compile(colname))
    while True:
        l = inconn.readline()
        l = l
        l=l.rstrip('\n')
        # print(l)
        if l[:6] == "#CHROM":
            sl = l.split('\t')
            if cnames:
                colnums = get_colnums(colres, sl)
            else:
                colnums = [x for x in range(9, len(sl))]
            break
    return(colnums)

def ad2sync(ad, ref_allele, alt_allele):
    out = [0] * 5
    refind = ident.index(ref_allele.lower())
    altind = ident.index(alt_allele.lower())
    out[refind] = int(ad[0])
    out[altind] = int(ad[1])
    return(out)

def strsync(sync_col):
    return(":".join(map(str, sync_col)))

def syncify(chrom, pos, ref_allele, alt_allele, ads):
    out = [chrom, pos, ref_allele]
    for ad in ads:
        sync_col = ad2sync(ad, ref_allele, alt_allele)
        sync_col_str = strsync(sync_col)
        out.append(sync_col_str)
    return(out)
    

def vcf2sync(inconn, col, col_names, cnames, outconn):
    
    cols = parse_header(inconn, col_names, cnames)
    
    for index, l in enumerate(inconn):
        sl = l.rstrip('\n').split('\t')
        chrom = sl[0]
        pos = sl[1]
        ref_allele = sl[3]
        alt_allele = sl[4]
        ads = []
        
        for i in range(len(cols)):
            col = cols[i]
            entry = sl[col]
            entry_list = entry.split(":")
            ad = entry_list[1]
            ad_list = ad.split(',')
            ad1 = ad_list[0]
            ad2 = ad_list[1]
            ads.append((ad1, ad2))
        
        sync_entry = syncify(chrom, pos, ref_allele, alt_allele, ads)
        writeout(sync_entry, sys.stdout)
        #print(cmh.summary())

        #ad0, ad1 = [calls.AD[:2] for i in control]
        #test_ad0, test_ad1 = [calls.AD[:2] for i in test]

def writeout(sync_entry, outconn):
    outconn.write("\t".join(map(str, sync_entry)) + "\n")

def main():
    args = parse_my_args()

    inconn, cols, col_names, cnames, = get_arg_vars(args)
    outconn = sys.stdout

    vcf2sync(inconn, cols, col_names, cnames, outconn)

    inconn.close()

if __name__ == "__main__":
    main()

#>>> for i in b:
#...     for j in i:
#...         try:print(j.data.AD)
