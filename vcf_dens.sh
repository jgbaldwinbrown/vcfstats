#!/bin/bash
set -e

FAI="$1"
IN="$2"
OPRE="$3"
WIN="$4"
STEP="$5"

# Make 5Mb sliding windows (step 1Mb)
bedtools makewindows \
-g <( grep '^X' ${FAI} ) \
-w ${WIN} \
-s ${STEP} \
-i winnum \
> ${OPRE}_windows.bed

# Obtain densities of genes within individual windows
bedtools coverage \
-a ${OPRE}_windows.bed \
-b <( sortBed -i ${IN} ) \
> ${OPRE}_windows_${WIN}.bed
