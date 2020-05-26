#!/usr/bin/env python3

cat vcf100.vcf | sed '/^#CHROM/q' >header_temp.txt

cat vcf100.vcf | grep -v '^#' | parallel -k -j 6 -l 100000 --spreadstdin python3 vcf2sync_supply_header.py --header header_temp.txt 2>/dev/null | pigz -p 2 -c > vcf_af_parallel.sync.gz
