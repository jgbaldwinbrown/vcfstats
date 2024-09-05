#!/bin/bash
set -e

CONTROLNAMES="$1"
EXPNAMES="$2"
SRC="$3"
DEST="$4"

mkdir -p `dirname "${DEST}"`

pigz -p 8 -d -c "${SRC}" | \
cmh_vcf_small_fast -C "${CONTROLNAMES}" -T "${EXPNAMES}" | \
vcf2bed_cmh | \
tee "${DEST}.bed" | \
mawk -F "\t" -v OFS="\t" '{print $1, $2, $4}' \
> "${DEST}.txt"
