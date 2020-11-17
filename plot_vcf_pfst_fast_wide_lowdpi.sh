#!/bin/bash
set -e

vcf2bed_pfst | plot_bed_info -f NLOG10PFST -o $1 -p -d 72 -x 256,6 -a 0.8
