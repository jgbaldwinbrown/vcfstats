#!/bin/bash
set -e

cat vcf100.vcf | python3 vcf2sync.py | gzip -c  > vcf_af.sync.gz
#cat vcf100.vcf | python3 -m cProfile vcf2sync.py | gzip -c  > vcf_af.sync.gz
