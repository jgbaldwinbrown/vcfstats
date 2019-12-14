#!/bin/bash
set -e

../cmh_vcf.py \
    mini.vcf \
    -C 16125X10,16125X11,16125X1 \
    -T 16125X12,16125X13,16125X14 \
> cmh.txt
