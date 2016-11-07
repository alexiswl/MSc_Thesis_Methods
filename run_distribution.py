#!/usr/bin/env python

#!/usr/bin/env python

# Shows a nice plot of the run and the read distribution by metrichor exit status.

from Bio import SeqIO
import os
import time
import argparse
import sys

help_descriptor = "Shows a nice plot of the run and the read distribution by metrichor exit status"

parser = argparse.ArgumentParser(description=help_descriptor)
parser.add_argument("--working_directory", nargs='?', dest="WORKING_DIRECTORY", type=str,
                    help="Where would you like to run this script?", required=True)
parser.add_argument("--run_name", nargs='?', dest="RUN_NAME", type=str,
                    help="For the purposes of the title in the R plots, what is the name of the run?", required=True)

args = parser.parse_args()

WORKING_DIRECTORY = args.WORKING_DIRECTORY
RUN_NAME = args.RUN_NAME
DATE_PREFIX = str(time.strftime("%Y-%m-%d"))

if not os.path.isdir(WORKING_DIRECTORY):
    error_message = "Error: Working directory specified does not exist"
    sys.exit(error_message)

WORKING_DIRECTORY = os.path.abspath(WORKING_DIRECTORY) + "/"
os.chdir(WORKING_DIRECTORY)

analytics_directory = WORKING_DIRECTORY + "analytics/"
if not os.path.isdir(analytics_directory):
    os.mkdir(analytics_directory)


# Now, for each 2d read generated, where did that read go??
pass_directory = WORKING_DIRECTORY + "reads/downloads/pass/"
fail_directory = WORKING_DIRECTORY + "reads/downloads/fail/"
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
                         fail_directory + "Calibration_strand_detected/" + calibration_sub_folder + "/"})
    distribution.update({"Calibration_strand_detected/" + calibration_sub_folder: 0})

for fail_folder, fail_folder_path in fail_folders.iteritems():
    fast5_files = [fail_folder_path + fast5_file for fast5_file in os.listdir(fail_folder_path)
                   if fast5_file.endswith(".fast5")]
    distribution[fail_folder] += len(fast5_files)

fast5_files = [pass_directory + fast5_file for fast5_file in os.listdir(pass_directory)
                if fast5_file.endswith(".fast5")]
distribution["pass"] += len(fast5_files)

col_names = []
col_values = []
for key, value in distribution.iteritems():
    col_names.append(key)
    col_values.append(value)

run_distribution_summary_file = analytics_directory + DATE_PREFIX + "_" + RUN_NAME + "_run_distribution.txt"

output_handle = open(run_distribution_summary_file, "w+")
output_handle.write("\t".join(map(str, col_names)) + "\n")
output_handle.write("\t".join(map(str, col_values)) + "\n")
output_handle.close()

os.chdir(analytics_directory)
os.system("run_distribution.R %s %s" % (run_distribution_summary_file, RUN_NAME))
