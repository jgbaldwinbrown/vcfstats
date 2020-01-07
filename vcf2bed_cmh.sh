#!/bin/bash
set -e

cat "$@" | \
mawk -F "\t" -v OFS="\t" \
'!/^#/{
    match($0, /(\t|;)CMH=([0-9a-zA-Z.\-]+)/);
    cmh_match = substr($0, RSTART, RLENGTH);
    match(cmh_match, /=/);
    cmh = substr(cmh_match, RSTART+1, length(cmh_match) - RSTART)
    
    match($0, /;NLOG10CMH=([0-9a-zA-Z.\-]+)/);
    nlcmh_match = substr($0, RSTART, RLENGTH);
    match(nlcmh_match, /=/);
    nlcmh = substr(nlcmh_match, RSTART+1, length(nlcmh_match) - RSTART)
    printf("%s\t%d\t%s\t%s\t%s\n", $1, $2 - 1, $2, cmh, nlcmh);
}
'
