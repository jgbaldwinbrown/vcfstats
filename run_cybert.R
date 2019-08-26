#!/usr/bin/env Rscript

source("bayesreg.R")
library(argparse)
library(data.table)

parser = ArgumentParser()
parser$add_argument("table", help="data table to run cybert on")
parser$add_argument("-c", "--controls", help="control columns for cybert")
parser$add_argument("-e", "--experimental", help="experimental columns for cybert")
parser$add_argument("-w", "--window_size", help="window size for cybert")

args = parser$parse_args()

control_cols = as.numeric(args$controls)
experimental_cols = as.numeric(args$experimental)

win_size = as.numeric(args$window_size)

data = as.data.frame(fread(args$table, sep="\t", header=TRUE))

odata = bayesT(aData=data, numC=control_cols, numE=experimental_cols, winSize=win_size)

write.table(odata, "")
