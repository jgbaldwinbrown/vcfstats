#!/usr/bin/env python3

import sys

ident = ["A","T","C","G","N","0"]

class Entry:
    def __init__(self, input_line):
        sl = input_line.rstrip('\n').split('\t')
        self.chrom = sl[0]
        self.pos = sl[1]
        self.ref_allele = sl[2]
        self.ref_index = ident.index(self.ref_allele)
        self.freqs = sl[3:]
        self.original_line = input_line

def parse_sync(inconn):
    for line in inconn:
        yield Entry(line)

def good_entry(entry):
    ok = False
    for freqset in entry.freqs:
        individual_freqs = [int(x) for x in freqset.split(":")]
        if individual_freqs[entry.ref_index] != 0:
            ok = True
            break
    return ok

def printable(entry):
    return(entry.original_line)

def filter_sync(inconn, outconn):
    for entry in parse_sync(inconn):
        if good_entry(entry):
            outconn.write(printable(entry))

def main():
    filter_sync(sys.stdin, sys.stdout)

if __name__ == "__main__":
    main()
