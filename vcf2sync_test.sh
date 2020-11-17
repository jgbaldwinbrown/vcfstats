#!/bin/bash
set -e

cat vcf_af.txt | python3 vcf2sync.py  > vcf_af.sync
