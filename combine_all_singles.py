#!/usr/bin/env python3

import sys
import subprocess

def get_combos(inconn, vcfin):
    out = []
    for l in inconn:
        sl = l.rstrip('\n').split('\t')
        combo = {
            "names_path": sl[0],
            "breed": sl[1],
            "gen": sl[2],
            "outprefix": sl[3]
            "names": []
            "name_regexes": []
            "name_full_regex": []
        }
        with open(combo["inpaths_path"], "r") as inpaths_conn:
            for l in inpaths_conn:
                name = l.rstrip('\n')
                name_regex = "^" + name + "$"
                combo["names"].append(name)
                combo["name_regexes"].append(name_regex)
            combo["name_full_regex"] = ",".join(combo["name_regexes"])
        out.append(combo)
    return(out)

def generate_combos(combo, vcfin):
    vcf_subset_command = "gunzip -c " + vcfin + " | vcf_subset_fast '" + combo["name_full_regex"] + "' | gzip -c > " + outprefix + ".split.vcf.gz"
    print(vcf_subset_command)

def main():
    combos_to_do = get_combos(sys.stdin)
    vcfin = sys.argv[1]
    for combo in combos_to_do:
        generate_combo(combo, vcfin)

if __name__ == "__main__":
    main()

# 15515X102
