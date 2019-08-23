#!/bin/bash
set -e

for i in "$@"; do
    igz=$(echo "$i" | sed 's/\.[^\.]*$//g').vcf.gz
    bgzip -c "$i" > "${igz}"
    tabix -p vcf "${igz}"
done

ls

for i in "$@"; do
    echo "$i" | sed 's/\.[^\.]*$/.vcf.gz/g'
done | \
xargs bcftools merge --force-samples -o Merged.vcf.gz

for i in "$@"; do
    igz=$(echo "$i" | sed 's/\.[^\.]*$//g').vcf.gz
    rm "${igz}"
    rm "${igz}.tbi"
done
