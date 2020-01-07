#!/bin/bash
set -e

vcf2bed_cmh | plot_bed_info -f NLOG10CMH -o $1 -p -d 400 -x 32,6 -a 0.8
