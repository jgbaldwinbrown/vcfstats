#!/usr/bin/env python3

import vcf
import numpy as np
import sys
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sys.path.append("/data1/jbrown/local_programs/vcfstats/geneview/geneview")
#/home/jgbaldwinbrown/Documents/git_repositories/geneview/geneview
import geneview as gv

def parse_my_args():
    parser = argparse.ArgumentParser("Plot the chosen field from a vcf file.")
    parser.add_argument("vcf", nargs="?", help="Input VCF file; default stdin")
    parser.add_argument("-f", "--field",  help="VCF INFO field to plot; required.", required=True)
    parser.add_argument("-o", "--outfile", help="file to plot in; default = show")
    parser.add_argument("-p", "--png", help="Plot a png instead of a pdf; default=pdf", action="store_true")
    parser.add_argument("-d", "--dpi", help="Set dpi; default=300")
    parser.add_argument("-x", "--xy", help="comma-separated number pair for width and height of plot. Default = 8,4.")
    parser.add_argument("-a", "--alpha", help="Alpha (opacity) of plot points. 0.0 to 1.0, default = 1.0.")

    args = parser.parse_args()
    return(args)

def get_arg_vars(args):
    if args.vcf:
        inconn = open(args.vcf, "r")
    else:
        inconn = sys.stdin
    field = args.field
    if args.outfile:
        outfile = args.outfile
        pdf = True
    else:
        outfile = ""
        pdf = False
    
    dpi = 300
    if args.dpi:
        dpi = int(args.dpi)
    
    xy = (8.0, 4.0)
    alpha = 1.0
    if args.xy:
        xy = tuple((float(i) for i in args.xy.split(",")))
    if args.alpha:
        alpha = float(args.alpha)
    
    return((inconn, field, outfile, pdf, args.png, dpi, xy, alpha))

def vcf2pd(vcfin, field):
    data = vcf2list(vcfin, field)
    out = pd.DataFrame.from_records(data).dropna()
    out.columns = ["CHROM", "POS", field]
    return(out)

def vcf2list(vcfin, field):
    out = []
    for record in vcfin:
        record_data = []
        record_data.append(record.CHROM)
        record_data.append(record.POS)
        try:
            record_data.append(float(record.INFO[field][0]))
            out.append(record_data)
        except ValueError:
            pass
    return(out)

def plot_data(data, outfile, pdf, field, png, dpi, xy, alpha):

    #xtick = ['chr'+c for c in map(str, range(1, 15) + ['16', '18', '20', '22'])]
    fig = plt.figure(figsize=xy)
    ax = fig.add_subplot(1,1,1)
    #plt.rcParams["figure.figsize"] = xy
    theplot = gv.gwas.manhattanplot(data,  
                             ax=ax, 
                             xlabel="Chromosome", 
                             ylabel=field, 
                             xticklabel_kws={'rotation': 'vertical'},
                             mlog10=False,
                             alpha=alpha
                             )
    #g = sns.FacetGrid(data)
    #g.map(sns.relplot, x='POS', y=field, data=data, col='CHROM')
    #g.set(xlim = 
    #g.set(ylim=(-1, 11), yticks=[0, 5, 10]);
    #myplot=sns.relplot(x='POS', y=field, data=data, col = 'CHROM')
    #plt.set_size_inches(xy[0], xy[1])
    if pdf:
        if png:
            plt.savefig(outfile, format="png", dpi=dpi)
        else:
            plt.savefig(outfile)
    else:
        plt.show()

def main():
    args = parse_my_args()

    inconn, field , outfile, pdf, png, dpi, xy, alpha = get_arg_vars(args)

    vcfin = vcf.Reader(inconn)
    data = vcf2pd(vcfin, field)
    inconn.close()

    plot_data(data, outfile, pdf, field, png, dpi, xy, alpha)
    
    #print(data)

if __name__ == "__main__":
    main()

#>>> for i in b:
#...     for j in i:
#...         try:print(j.data.AD)
