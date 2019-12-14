#!/bin/bash
set -e

rsync -avP u6012238@kingspeak.chpc.utah.edu:/scratch/general/lustre/u6012238/louse/fqf/big_out_pooled/mini* .
