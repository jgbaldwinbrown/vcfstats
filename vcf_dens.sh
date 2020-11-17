#!/bin/bash
set -e

FAI="$1"
IN="$2"
OPRE="$3"
WIN="$4"
STEP="$5"

# Make 5Mb sliding windows (step 1Mb)
bedtools makewindows \
    -g ${FAI} \
    -w ${WIN} \
    -s ${STEP} \
    -i winnum \
> ${OPRE}_windows_${WIN}_${STEP}.bed

# Obtain densities of genes within individual windows
bedtools coverage \
    -a ${OPRE}_windows_${WIN}_${STEP}.bed \
    -b <( sortBed -i ${IN} ) \
> ${OPRE}_dens_windows_${WIN}_${STEP}.bed
