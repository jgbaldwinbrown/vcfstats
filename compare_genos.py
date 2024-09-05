#!/usr/bin/env python3

import vcf
sys

def keep_clean_pairs(vcfin, outwriter):
    
    for index, record in enumerate(vcfin):
        calls = [call for call in record]
        
        try:
            for i in range(len(control_cols)):
                gt0 = calls[0].gt_bases
                gt1 = calls[1].gt_bases
                gt2 = calls[2].gt_bases
                gt3 = calls[3].gt_bases
                if (
                    gt0 == gt1 and
                    gt2 == gt3 and
                    gt0 != gt2 and
                    not calls[0].is_het and
                    not calls[1].is_het and
                    not calls[2].is_het and
                    not calls[3].is_het
                ):
                    writeout(record, outwriter)
                    
        except (ValueError, TypeError):
            pass

def writeout(record, writer):
    writer.write_record(record)

def main():
    
    vcfin = vcf.Reader(sys.stdin)
    outwriter = vcf.Writer(sys.stdout, vcfin)
    keep_clean_pairs(vcfin, outwriter)

    inconn.close()

if __name__ == "__main__":
    main()
