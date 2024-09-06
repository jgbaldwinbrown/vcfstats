# Vcfstats

Utilities for modifying VCF files and performing population genetic statistics on them

## Installation

To install, just run the following

```sh
./install.sh /path/to/bin/dir/
```

## Usage

### vcf2sync

```
usage: Convert a VCF file to the sync format [-h] [-c COLUMNS]
                                             [-C COLUMN_NAMES]
                                             [vcf]

positional arguments:
  vcf                   Input VCF file; default stdin

options:
  -h, --help            show this help message and exit
  -c COLUMNS, --columns COLUMNS
                        comma separated, 0-indexed VCF columns to convert
                        (default = all); not compatible with -C.
  -C COLUMN_NAMES, --column_names COLUMN_NAMES
                        comma separated names of VCF columns to convert
                        (default = all); not compatible with -c.
```

### vcf-subset-fast

```
usage: vcf-subset-fast colregexes
```

vcf-subset-fast extracts specified columns from a VCF file very quickly. All
standard columns are retained. Sample-specific columns are retained according
to colregexes. Colregexes should be a comma-separated list of regular
expressions that will be matched to the names of the sample columns. Any column
that matches any of the regular expressions will be retained.

### combine\_single\_indivs\_fast

```
usage: Combines a VCF of individual calls into one large VCF for population.
       [-h] -n NAME [vcf]

positional arguments:
  vcf                   Input VCF file; default stdin.

options:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  name of combined population.
```

### vcf2bed\_*

This set of commands converts a vcf file to a bed file. All of the commands
correctly convert each VCF entry into a bed entry with corresponding
coordinates. The fourth and fifth columns are determined by the suffix of the command:

- vcf2bed\_clean: no 4th and 5th columns
- vcf2bed\_cmh: if the vcf file has information fields named 'CMH' and 'NLOG10CMH', the values of these are, respectively the 4th and 5th columns.
- vcf2bed\_cybert: if the vcf file has information fields named 'CYBERP' and 'NLOG10CYBERP', the values of these are, respectively the 4th and 5th columns.
- vcf2bed\_pfst: if the vcf file has information fields named 'PFST' and 'NLOG10PFST', the values of these are, respectively the 4th and 5th columns.

### cmh\_vcf

```
usage: Compute the Cochran-Mantel-Haenszel test on a VCF file
       [-h] [-c CONTROL] [-t TEST] [-C CONTROL_NAMES] [-T TEST_NAMES] [vcf]

positional arguments:
  vcf                   Input VCF file; default stdin

options:
  -h, --help            show this help message and exit
  -c CONTROL, --control CONTROL
                        comma separated, 0-indexed VCF columns to use as
                        controls. This or -C required; cannot use both.
  -t TEST, --test TEST  comma separated, 0-indexed VCF columns to use as test
                        data. This or -T required; cannot use both.
  -C CONTROL_NAMES, --control_names CONTROL_NAMES
                        comma separated names of VCF columns to use as
                        controls. This or -c required; cannot use both.
  -T TEST_NAMES, --test_names TEST_NAMES
                        comma separated, 0-indexed VCF columns to use as test
                        data. This or -t required; cannot use both.
```

### cybert\_vcf

```
usage: Compute the Cochran-Mantel-Haenszel test on a VCF file
       [-h] [-c CONTROL] [-t TEST] -w WINDOW_SIZE [-C CONTROL_NAMES]
       [-T TEST_NAMES]
       [vcf]

positional arguments:
  vcf                   Input VCF file; default stdin

options:
  -h, --help            show this help message and exit
  -c CONTROL, --control CONTROL
                        comma separated, 0-indexed VCF columns to use as
                        controls; required.
  -t TEST, --test TEST  comma separated, 0-indexed VCF columns to use as test
                        data; required.
  -w WINDOW_SIZE, --window_size WINDOW_SIZE
                        Window size for sliding window cyber-t.
  -C CONTROL_NAMES, --control_names CONTROL_NAMES
                        comma separated names of VCF columns to use as
                        controls. This or -c required; cannot use both.
  -T TEST_NAMES, --test_names TEST_NAMES
                        comma separated, 0-indexed VCF columns to use as test
                        data. This or -t required; cannot use both.
```

### pfst\_nopool

Take a VCF file of non-pooled (i.e. individual sequencing) samples and calculate pFST. Arguments:

1. Comma-separated regexes specifying the control columns.
2. Comma-separated regexes specifying the experimental columns.
3. Path to the input VCF file.
4. Prefix for output files.

### pfst

Take a VCF file of pooled (i.e. one population per column) samples and calculate pFST. Arguments:

1. Comma-separated regexes specifying the control columns.
2. Comma-separated regexes specifying the experimental columns.
3. Path to the input VCF file.
4. Prefix for output files.
