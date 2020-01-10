#!/bin/bash
set -e

# command line options:
# $1: control columns
# $2: test columns
# $3: input vcf
# $4: subsetted vcf name
# $5: freq-subsetted vcf name
# $6: pfst output filename

vcf-subset-fast "${1},${2}" <${3} > ${4}
vcf-subset-freq 0.1 20 <${4} > ${5}

background_cols=`vcf_colnums "${1}" <${5}`
target_cols=`vcf_colnums "${2}" <${5}`

pFst \
    --target "${target_cols}" \
    --background "${background_cols}" \
    --file ${5} \
    --type PO \
> ${6}
