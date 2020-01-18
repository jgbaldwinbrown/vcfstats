#!/bin/bash
set -e

cat "$@" | \
mawk -F "\t" -v OFS="\t" \
'!/^#/{
    printf("%s\t%d\t%s\n", $1, $2 - 1, $2);
}
'
