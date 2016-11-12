#!/usr/bin/env python
import os


WORKING_DIRECTORY = "/data/Bioinfo/bioinfo-proj-alexis/2016_03_15_E_COLI_R7p3/"
alignment_methods = ("bwa-mem", "graphmap", "last")

nanonet = False

nanonet_basecalling_types = ("--2D --fasta", "--fwd --fasta", "--rev --fasta")

metrichor_basecalling_types = ("--2D --fastq", "--2D --fastq --fail", "--fwd --fastq", "--fwd --fastq --fail",
                     "--rev --fastq", "--rev --fastq --fail")

preliminary_commandline_arguments = "alignment.py --run_name E_COLI_R9 --working_directory ./ " + \
                                    "--reference ../references/e_coli_k12_mg1655/NC_000913.fna " + \
                                    "--threads 20"

for alignment_method in alignment_methods:
    for basecalling_type in metrichor_basecalling_types:
        full_commandline_argument = preliminary_commandline_arguments + " --alignment_method " + alignment_method \
                                    + " " + basecalling_type
        os.system(full_commandline_argument)

if nanonet:
    for basecalling_type in nanonet_basecalling_types:
        full_commandline_argument = preliminary_commandline_arguments + " --alignment_method " + alignment_method \
                                    + " " + basecalling_type
        os.system(full_commandline_argument)
