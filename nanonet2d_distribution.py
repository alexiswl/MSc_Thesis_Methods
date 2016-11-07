#!/usr/bin/env python

# This is a script that asks where did the 2d reads generated by nanonet2d
# end up with respect to metrichor. Can we infer the quality of a read by its 2D status?

from Bio import SeqIO
import os

main_directory = "/data/Bioinfo/bioinfo-proj-alexis/2016_08_16_E_COLI_R9/"
nanonet_2d_fasta_file = main_directory + "fasta/2D/concatenated_2d.fasta"
nanonet_2d_fasta_directory = main_directory + "fasta/2D/2d/"
os.system("cat %s* > %s" % (nanonet_2d_fasta_directory, nanonet_2d_fasta_file))

nanonet_2d_read_ids = []
input_handle = open(nanonet_2d_fasta_file, "rU")

# Get a list of nanonet_2d_reads
for record in SeqIO.parse(input_handle, "fasta"):
    nanonet_2d_read_ids.append(record.id)

# Now, for each 2d read generated, where did that read go??
pass_directory = main_directory + "reads/downloads/fail/"
fail_directory = main_directory + "reads/downloads/fail/"
fail_folder_set = ("1D_basecall_not_performed", "2D_basecall_not_performed", "2D_failed_quality_filters",
                   "Corrupted_files", "No_complement_data", "No_template_data",
                   "Unknown_error")
fail_folders = {}
calibration_stand_sub_folder_set = ("2D_basecall_not_performed", "2D_failed_quality_filters", "Passed_quality")

distribution = {"pass":0}

for folder in fail_folder_set:
    fail_folders.update({folder: fail_directory + folder + "/"})
    distribution.update({folder: 0})

for calibration_sub_folder in calibration_stand_sub_folder_set:
    fail_folders.update({"Calibration_strand_detected/" + calibration_sub_folder:
                         fail_directory + "Calibration_strand_detected/" + folder + "/"})

for read in nanonet_2d_read_ids:
    for fail_folder, fail_folder_path in fail_folders.iteritems():
        if read in os.path.listdir(fail_folder_path):
            distribution[fail_folder] += 1
    if read in os.path.listdir(pass_directory):
        distribution["pass"] += 1



print(distribution)
