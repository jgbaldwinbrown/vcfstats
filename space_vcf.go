package main

import (
    "fmt"
    "os"
    "flag"
    "bufio"
    "strconv"
    "io"
    "strings"
)

type flags struct {
    min_space int
}

func get_flags() flags {
    var f flags
    flag.IntVar(&f.min_space, "space", 100000, "Minimum space between polymorphic sites to keep")
    flag.Parse()
    return f
}

func get_chrompos(line string) (string, int) {
    split_line := strings.Split(line, "\t")
    chrom := split_line[0]
    pos, err := strconv.Atoi(split_line[1])
    if err != nil {
        panic(err)
    }
    return chrom, pos
}

func check_line(chrom string, pos int, prev_chrom string, prev_pos int, my_flags flags) bool {
    return (chrom != prev_chrom) || pos - prev_pos >= my_flags.min_space
}

func space_vcf(vcf_inconn io.Reader, vcf_outconn io.Writer, my_flags flags) {
    prev_chrom := ""
    prev_pos := -10000000000
    scanner := bufio.NewScanner(vcf_inconn)
    for scanner.Scan() {
        if scanner.Text() == "" {
            fmt.Fprintln(vcf_outconn, scanner.Text())
        } else if scanner.Text()[0] == '#' {
            fmt.Fprintln(vcf_outconn, scanner.Text())
        } else {
            chrom, pos := get_chrompos(scanner.Text())
            if check_line(chrom, pos, prev_chrom, prev_pos, my_flags) {
                fmt.Fprintln(vcf_outconn, scanner.Text())
                prev_chrom = chrom
                prev_pos = pos
            }
        }
    }
}

func main() {
    my_flags := get_flags()
    space_vcf(os.Stdin, os.Stdout, my_flags)
}
