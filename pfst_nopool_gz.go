package main

import (
	"path/filepath"
	"os/exec"
	"os"
	"strings"
	"fmt"
)

type Args struct {
	ControlCols string
	TestCols string
	VcfPath string
	OutputPre string
}

func GetArgs() Args {
	var a Args
	if len(os.Args) < 5 {
		panic(fmt.Errorf("Not enough arguments."))
	}
	a.ControlCols = os.Args[1]
	a.TestCols = os.Args[2]
	a.VcfPath = os.Args[3]
	a.OutputPre = os.Args[4]
	return a
}

func SubsetVcf(vcfPath, controlCols, testCols, vcfSubsetPath string) error {
	r, w, err := os.Pipe()
	if err != nil {
		return err
	}
	defer r.Close()
	defer w.Close()

	gzcmd := exec.Command("gunzip", "-c", vcfPath)
	gzcmd.Stderr = os.Stderr
	gzcmd.Stdout = w
	err = gzcmd.Start()
	if err != nil {
		return err
	}

	out, err := os.Create(vcfSubsetPath)
	if err != nil {
		return err
	}
	defer out.Close()

	subcmd := exec.Command("vcf-subset-fast", strings.Join([]string{controlCols, testCols}, ","))
	subcmd.Stderr = os.Stderr
	subcmd.Stdout = out
	subcmd.Stdin = r
	err = subcmd.Run()
	if err != nil {
		return err
	}

	return nil
}

func VcfColnums(cols, vcfSubsetPath string) (string, error) {
	var out strings.Builder
	cmd := exec.Command("vcf_colnums", cols)
	cmd.Stderr = os.Stderr
	cmd.Stdout = &out
	err := cmd.Run()
	if err != nil {
		return "", err
	}
	return out.String(), nil
}

func Pfst(targetCols, backgroundCols, vcfSubsetPath, PfstOut string) error {
	out, err := os.Open(PfstOut)
	if err != nil {
		return err
	}
	defer out.Close()

	cmd := exec.Command("pFst",
		"--target", targetCols,
		"--background", backgroundCols,
		"--file", vcfSubsetPath,
		"--type", "PL",
	)
	cmd.Stderr = os.Stderr
	cmd.Stdout = out

	err = cmd.Run()
	if err != nil {
		return err
	}

	return nil
}
// pFst \
//     --target "${TARGET_COLS}" \
//     --background "${BACKGROUND_COLS}" \
//     --file ${SI} \
//     --type PL \
// > ${O}


func main() {
	args := GetArgs()
	od := filepath.Base(args.OutputPre)
	os.MkdirAll(od, os.ModePerm)
	vcfSubsetPath := args.OutputPre + "_subsetted_input.vcf"
	PfstOut := args.OutputPre + "_pfst.txt"
	err := SubsetVcf(args.VcfPath, args.ControlCols, args.TestCols, vcfSubsetPath)
	defer os.Remove(vcfSubsetPath)
	if err != nil {
		panic(err)
	}

	backgroundCols, err := VcfColnums(args.ControlCols, vcfSubsetPath)
	if err != nil {
		panic(err)
	}
	targetCols, err := VcfColnums(args.TestCols, vcfSubsetPath)
	if err != nil {
		panic(err)
	}

	err = Pfst(targetCols, backgroundCols, vcfSubsetPath, PfstOut)
	if err != nil {
		panic(err)
	}
}

/*
#!/bin/bash

# command line options:
# $1: control columns
# $2: test columns
# $3: input vcf
# $4: output_prefix

SI=${4}_subsetted_input.vcf
FSI=${4}_freq_subsetted_input.vcf
O=${4}_pfst.txt
OD=`dirname ${4}`

mkdir -p ${OD}

gunzip -c "${3}" | vcf-subset-fast "${1},${2}" > ${SI}
# vcf-subset-freq-nopool 0.1 5 <${SI} > ${FSI}

BACKGROUND_COLS=`vcf_colnums "${1}" <${SI}`
TARGET_COLS=`vcf_colnums "${2}" <${SI}`

pFst \
    --target "${TARGET_COLS}" \
    --background "${BACKGROUND_COLS}" \
    --file ${SI} \
    --type PL \
> ${O}

if -s "${SI}" ; then
	rm "${SI}"
fi
*/
