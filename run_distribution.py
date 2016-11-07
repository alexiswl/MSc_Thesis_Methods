#!/usr/bin/env python

#!/usr/bin/env python

# For a 2D run, where did the reads end up post-metrichor?

from Bio import SeqIO
import os

main_directory = "/data/Bioinfo/bioinfo-proj-alexis/2016_08_16_E_COLI_R9/"
analytics_directory = main_directory + "analytics/"
if not os.path.isdir(analytics_directory):
    os.mkdir(analytics_directory)

DATE_PREFIX = str(time.strftime("%Y-%m-%d"))

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

for fail_folder, fail_folder_path in fail_folders.iteritems():
    fast5_files = [fail_folder_path + fast5_file for fast5_file in os.listdir(fail_folder_path)
                   if fast5_file.endswith(".fast5")]
    distribution[fail_folder] += len(fast5_files)

fast5_files = [pass_directory + fast5_file for fast5_file in os.listdir(pass_directory)
                if fast5_file.endswith(".fast5")]
distribution["pass"] += len(fast5_files)

col_names = []
col_values = []
for keys, values in distribution.iterkeys():
    col_names.append[keys]
    col_values.append[values]

run_distribution_summary_file = analytics_directory + DATE_PREFIX + "_" + RUN_NAME + "_run_distribution.txt"

output_handle = open(run_distribution_summary_file, "w+")
output_handle.write("\t".join(col_names) + "\n")
output_handle.write("\t".join(col_values) + "\n")
output_handle.close()

