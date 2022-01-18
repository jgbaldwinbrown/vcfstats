#!/bin/bash
set -e

# command line options:
# $1: control columns
# $2: test columns
# $3: input vcf
# $4: output_prefix

SI=${4}_subsetted_input.vcf
FSI=${4}_freq_subsetted_input.vcf
O=${4}_pfst.txt
OD=`dirname ${4}`

mkdir -p ${OD}

gunzip -c "${3}" | vcf-subset-fast "${1},${2}" > ${SI}
# vcf-subset-freq-nopool 0.1 5 <${SI} > ${FSI}

BACKGROUND_COLS=`vcf_colnums "${1}" <${SI}`
TARGET_COLS=`vcf_colnums "${2}" <${SI}`

pFst \
    --target "${TARGET_COLS}" \
    --background "${BACKGROUND_COLS}" \
    --file ${SI} \
    --type PL \
> ${O}
