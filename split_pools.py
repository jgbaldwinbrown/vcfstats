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
            "treatment": sl[3],
            "replicate": sl[4],
            "outprefix": sl[5],
            "names": [],
            "name_regexes": [],
            "name_full_regex": []
        }
        with open(combo["names_path"], "r") as inpaths_conn:
            for l in inpaths_conn:
                name = l.rstrip('\n')
                name_regex = "^" + name + "$$"
                combo["names"].append(name)
                combo["name_regexes"].append(name_regex)
            combo["name_full_regex"] = ",".join(combo["name_regexes"])
        out.append(combo)
    return(out)

def generate_combo(combo, vcfin, all_targets, all_commands):
    splitvcfname = combo["outprefix"] + ".split.vcf.gz"
    vcf_subset_target = splitvcfname + ": " + vcfin
    vcf_subset_command = "\tgunzip -c " + vcfin + " | vcf-subset-fast-dup '" + combo["name_full_regex"] + "' | bgzip -c > " + splitvcfname
    all_commands.append(vcf_subset_target)
    all_commands.append(vcf_subset_command)
    all_targets.append(splitvcfname)
    
    # outname = combo["breed"] + "_" + combo["gen"] + "_" + combo["treatment"] + "_" + combo["replicate"]
    # outpath = combo["outprefix"] + ".vcf.gz"
    # combine_target = outpath + ": " + splitvcfname
    # combine_command = "\tgunzip -c " + splitvcfname + " | combine_single_indivs_fast -n " + outname + " | bgzip -c > " + outpath
    # all_commands.append(combine_target)
    # all_commands.append(combine_command)
    # all_commands.append("")
    # all_targets.append(outpath)

def generate_combos(combos, vcfin):
    all_targets = []
    all_commands = []
    for combo in combos:
        generate_combo(combo, vcfin, all_targets, all_commands)
    
    print("all: " + " ".join(all_targets))
    print("")
    print("\n".join(all_commands))

def main():
    vcfin = sys.argv[1]
    combos_to_do = get_combos(sys.stdin, vcfin)
    generate_combos(combos_to_do, vcfin)

if __name__ == "__main__":
    main()

# 15515X102
