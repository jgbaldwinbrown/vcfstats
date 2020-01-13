#!/usr/bin/env python3

import fileinput
import math

def main():
    for l in fileinput.input():
        l = l.rstrip('\n')
        sl = l.split('\t')
        chr = sl[0]
        pos = int(sl[1])
        pfst = float(sl[2])
        nlpfst = -math.log10(pfst)
        out = [chr, pos-1, pos, pfst, nlpfst]
        print("\t".join(map(str, out)))

if __name__ == "__main__":
    main()
