package main

import (
    "strings"
    "fmt"
    "bufio"
    "os"
    "flag"
    "io"
    "strconv"
)

type key struct {
    chrom string
    pos int
    feature string
}

type flags struct {
    win_size int
    win_step int
}

type bins_map map[key]float64

type bins_data struct {
    chrlens map[string]int
    chr_list []string
    features map[string]bool
    features_list []string
    data bins_map
}

func get_flags() flags {
    var f flags
    flag.IntVar(&f.win_size, "win", 100000, "Window size")
    flag.IntVar(&f.win_step, "step", 10000, "Window step")
    flag.Parse()
    return f
}

func int_max(x, y int) int {
    if x < y {
        return y
    }
    return x
}

func int_min(x, y int) int {
    if x > y {
        return y
    }
    return x
}

func get_pos_list(start int, end int, f flags) []int {
    base1 := (start / f.win_step) * f.win_step;
    base2 := ((end-1) / f.win_step) * f.win_step;
    wins := (f.win_size / f.win_step) + 1;
    out := make([]int, 0)
    base_to_use := base2 + f.win_step
    if base2 > base1 {
        wins += (base2 / f.win_step) - (base1 / f.win_step)
    }
    if start % f.win_step == 0 {
        wins++
    }
    for i := wins - 1; i >= 0; i-- {
        // fmt.Printf("base_to_use: %v; wins: %v; i: %v; win: %v; win_step: %v\n", base_to_use, wins, i, base_to_use - (i*f.win_step), f.win_step)
        out = append(out, base_to_use - (i * f.win_step))
    }
    // fmt.Print(out)
    return out
}

func get_amount_to_add(pos int, start int, end int, f flags) int {
    amount := int(0)
    win_end := pos + f.win_size
    if end >= pos && start < win_end {
        left_max := int_max(pos, start)
        right_min := int_min(end, win_end)
        amount = right_min - left_max
    }
    return amount
}

func update_bins(bins bins_data, pos_list []int, chrom string, start int, end int, feature string, f flags) {
    for _, pos := range pos_list {
        my_key := key {
            chrom: chrom,
            pos: pos,
            feature: feature,
        }
        // fmt.Print(my_key)
        amount_to_add := get_amount_to_add(pos, start, end, f)
        // fmt.Printf("chrom: %v, pos: %v, width: %v, start: %v, end: %v, feature: %v, amount_to_add: %v\n", chrom, pos, f.win_size, start, end, feature, amount_to_add)
        _, ok := bins.data[my_key]
        if !ok {
            bins.data[my_key] = float64(amount_to_add)
        } else {
            bins.data[my_key] += float64(amount_to_add)
        }
        // fmt.Printf("bins: %v\n", bins)
    }
}

func add_line_to_entry(bins *bins_data, split_line []string, f flags) {
    chrom := split_line[0]
    feature := split_line[1] + ":" + split_line[2]
    start, serr := strconv.Atoi(split_line[3])
    end, eerr := strconv.Atoi(split_line[4])
    if (serr != nil) {
        panic(serr)
    }
    if (eerr != nil) {
        panic(eerr)
    }
    start--

    current_chrlen, ok := bins.chrlens[chrom]
    if !ok {
        bins.chr_list = append(bins.chr_list, chrom)
        bins.chrlens[chrom] = end
    } else {
        bins.chrlens[chrom] = int_max(current_chrlen, end)
    }

    _, ok = bins.features[feature]
    if !ok {
        bins.features_list = append(bins.features_list, feature)
        bins.features[feature] = true
    }

    pos_list := get_pos_list(start, end, f)

    update_bins(*bins, pos_list, chrom, start, end, feature, f)
}

func new_bins_data() bins_data {
    chrlens := make(map[string]int)
    features := make(map[string]bool)
    data := make(bins_map)
    return bins_data{
        chrlens: chrlens,
        features: features,
        data: data,
    }
}

func get_bins(inconn io.Reader, f flags) bins_data {
    bins := new_bins_data()
    scanner := bufio.NewScanner(inconn)
    for scanner.Scan() {
        split_line := strings.Split(scanner.Text()[:(len(scanner.Text())-1)], "\t")
        add_line_to_entry(&bins, split_line, f)
    }
    return bins
}

func print_header(bins bins_data, outconn io.Writer) {
    fmt.Printf("chrom\tstart\tend")
    for _, feature := range bins.features_list {
        fmt.Printf("\t%v", feature)
    }
    fmt.Printf("\n")
}

func print_body(bins bins_data, outconn io.Writer, f flags) {
    /*
    fmt.Printf("%v\n", bins.features)
    fmt.Printf("%v\n", bins.chrlens)
    */
    for _, chr := range bins.chr_list {
        chrlen := bins.chrlens[chr]
        for pos := int(0); pos < chrlen - f.win_size; pos += f.win_step {
            fmt.Printf("%v\t%v\t%v", chr, pos, pos + f.win_size)
            for _, feature := range bins.features_list {
                my_key := key {
                    chrom: chr,
                    pos: pos,
                    feature: feature,
                }
                // fmt.Printf("chrom: %v, pos: %v, width: %v, feature: %v, bin_content: %v\n", chr, pos, f.win_size, feature, bins.data[my_key])
                fmt.Printf("\t%v", bins.data[my_key])
            }
            fmt.Printf("\n")
        }
    }
}

func print_bins(bins bins_data, outconn io.Writer, f flags) {
    print_header(bins, outconn)
    // fmt.Println(bins)
    print_body(bins, outconn, f)
}

func main() {
    f := get_flags()
    bins := get_bins(os.Stdin, f)
    // fmt.Print(bins)
    print_bins(bins, os.Stdout, f)
}
