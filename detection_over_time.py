#!/usr/bin/env python

import os
import commands
import datetime

SUMMARY_DIRECTORY = "/data/Bioinfo/bioinfo-proj-alexis/2016_09_17_RAPID_SWAB_NO_2/one_codex/summary/"
ACCUMULATIVE_SUMMARY_FILE = "/data/Bioinfo/bioinfo-proj-alexis/2016_09_17_RAPID_SWAB_NO_2/one_codex/species/" + \
                            "accumulative.txt"
initial_start_time = datetime.datetime.strptime("2016-10-27-14-11-20", "%Y-%m-%d-%H-%M-S")
species_matched = []
time_points = []


for summary_file in os.path.listdir(SUMMARY_DIRECTORY):
    os.system("cat %s >> %s" % (summary_file, ACCUMULATIVE_SUMMARY_FILE))
    date_string = summary_file.split("-")
    year = date_string[0][-4:]
    seconds = date_string[len(date_string)-1][0:2]
    date_string = year + "-" + "-".join(date_string[1:len(date_string)-1]) + "-" + seconds
    date_format = datetime.datetime.strptime(date_string, "%Y-%m-%d-%H-%M-S")
    time_point = date_format - initial_start_time

    sys_output, species_match = commands.getstatusoutput("detection_over_time.R %s" % ACCUMULATIVE_SUMMARY_FILE)
    species_matched.append(species_match)
    time_points.append(time_point)

output_file = ACCUMULATIVE_SUMMARY_FILE + final_output.txt
output_file_h = open(output_file, "a+")
for species_match, time_point in zip(species_matched, time_points):
    output_file_h.write(time_point + species_match + "\n")




