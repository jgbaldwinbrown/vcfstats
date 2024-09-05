#!/bin/bash
set -e

bedops \
    --chop 500000 \
    --stagger 100000 \
    -x <(awk -vOFS="\t" '{ print $1, $2-1, $2; }' scaffolds.txt | \
sort-bed | \
    -) \
bedmap \
    --echo \
    --count \
    --delim '\t' - <(vcf2bed < snps.vcf) > answer.bed
