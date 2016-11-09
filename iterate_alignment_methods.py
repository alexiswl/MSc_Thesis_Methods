#!/usr/bin/env python

alignment_methods = ("bwa-mem", "graphmap", "last")

basecalling_types = ("--1D --fasta", "--2D --fasta", "--fwd --fasta", "--rev --fasta",
                     "--2D --fastq", "--2D --fastq --fail", "--fwd --fastq", "--fwd --fastq --fail"
                     "--rev --fastq", "--rev --fastq --fail")

preliminary_commandline_arguments = "alignment.py --run_name E_COLI_R9 --working_directory ./ --reference ../references/.." \
                                    "--threads 20"

for alignment_method in alignment_methods:
    for basecalling_type in basecalling_types:
        full_commandline_argument = preliminary_commandline_arguments + " " + alignment_method + " " + basecalling_type
        os.system(full_commandline_argument)
