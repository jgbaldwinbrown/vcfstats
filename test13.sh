#!/bin/bash
set -e

mkdir -p test11_out
pfst "^NA00002$,^NA00003$" "^NA00005$,^NA00006$" vcf7.txt test13_out_vcf7
