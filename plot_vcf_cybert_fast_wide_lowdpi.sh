#!/bin/bash
set -e

vcf2bed_cybert | plot_bed_info -f NLOG10CYBERT -o $1 -p -d 72 -x 256,6 -a 0.8
