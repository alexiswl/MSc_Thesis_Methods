#!/usr/bin/env python

import os
import commands
import datetime
import argparse
import sys

help_descriptor = "shows a little plot over time of the total number of species detected within a sample."

parser = argparse.ArgumentParser(description=help_descriptor)
parser.add_argument("--working_directory", nargs='?', dest="WORKING_DIRECTORY", type=str,
                    help="Where would you like to work this script?", required=True)
parser.add_argument("--onecodex-directory", nargs='?', dest="ONECODEX_DIRECTORY", type=str,
                    help="This is the onecodex directory. If not specified it is a child directory" +
                         "of the working directory")

args = parser.parse_args()

WORKING_DIRECTORY = args.WORKING_DIRECTORY
ONECODEX_DIRECTORY = args.ONECODEX_DIRECTORY

if WORKING_DIRECTORY:
    if not os.path.isdir(WORKING_DIRECTORY):
        error_message = "Error: Working directory does not exist."
        sys.exit(error_message)
if not WORKING_DIRECTORY:
    WORKING_DIRECTORY = os.getcwd()
    general_message = "Working directory not specified. Using current directory. %s. \n" % WORKING_DIRECTORY
    print general_message
WORKING_DIRECTORY = os.path.abspath(WORKING_DIRECTORY) + "/"

if ONECODEX_DIRECTORY:
    if not os.path.isdir(ONECODEX_DIRECTORY):
        error_message = "Error: Onecodex directory specified but does not exist."
        sys.exit(error_message)
if not ONECODEX_DIRECTORY:
    ONECODEX_DIRECTORY = WORKING_DIRECTORY + "one_codex/"

SUMMARY_DIRECTORY = ONECODEX_DIRECTORY + "summary/"
STATS_DIRECTORY = ONECODEX_DIRECTORY + "stats/"

if not os.path.isdir(STATS_DIRECTORY):
    os.mkdir(STATS_DIRECTORY)

ACCUMULATIVE_SUMMARY_FILE = STATS_DIRECTORY + "accumulative.txt"
SPECIES_BY_TIMEPOINT_FILE = STATS_DIRECTORY + "species_by_time_point.txt"

start_time = int(datetime.datetime.strptime("2016-10-27-14-11-20", "%Y-%m-%d-%H-%M-%S").strftime("%s"))
species_matched = []
time_points = []

summary_files = [SUMMARY_DIRECTORY + summary_file for summary_file in os.listdir(SUMMARY_DIRECTORY)]

for summary_file in summary_files:
    os.system("cat %s >> %s" % (summary_file, ACCUMULATIVE_SUMMARY_FILE))
    date_string = summary_file.split("-")
    year = date_string[0][-4:]
    seconds = date_string[len(date_string)-1][0:2]
    date_string = year + "-" + "-".join(date_string[1:len(date_string)-1]) + "-" + seconds
    current_time = int(datetime.datetime.strptime(date_string, "%Y-%m-%d-%H-%M-%S").strftime("%s"))
    time_point = current_time - start_time

    sys_output, species_match = commands.getstatusoutput("detection_over_time.R %s" % ACCUMULATIVE_SUMMARY_FILE)
    species_matched.append(species_match)
    time_points.append(time_point)

output_file = ACCUMULATIVE_SUMMARY_FILE + "final_output.txt"
output_file_h = open(output_file, "a+")
for species_match, time_point in zip(species_matched, time_points):
    output_file_h.write(time_point + species_match + "\n")





