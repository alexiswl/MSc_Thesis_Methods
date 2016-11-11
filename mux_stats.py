#!/usr/bin/env python
import h5py
import os
import argparse
import sys

version = 1.0
help_descriptor = "This is a simple script that creates a summary of the channels that produced decent reads."
parser = argparse.ArgumentParser(description=help_descriptor)
parser.add_argument('--version', action='version', version="%%(prog)s %s" % str(version))
parser.add_argument("--run_name", nargs='?', dest="RUN_NAME", type=str,
                    help="What do want to put in the prefix of the filenames?",
                    required=True)
parser.add_argument("--working_directory", nargs='?', dest="WORKING_DIRECTORY", type=str,
                    help="This is the main directory." +
                         "This directory is generally the run directory." +
                         "If not specified, this is the current directory.")
parser.add_argument("--pass_directory", nargs='?', dest="PASS_DIRECTORY", type=str,
                    help="This is the directory with all the pass files in it." +
                         "If not specified, it will be <working_directory>/reads/pass/")

args = parser.parse_args()

RUN_NAME = args.RUN_NAME
WORKING_DIRECTORY = args.WORKING_DIRECTORY
PASS_DIRECTORY = args.PASS_DIRECTORY

if WORKING_DIRECTORY:
    if not os.path.isdir(WORKING_DIRECTORY):
        error_message = "Error: Working directory %s does not exist." % WORKING_DIRECTORY
        sys.exit(error_message)
if not WORKING_DIRECTORY:
    WORKING_DIRECTORY = os.getcwd()
    general_message = "Working directory not specified. Using current directory. %s. \n" % WORKING_DIRECTORY
    print general_message
WORKING_DIRECTORY = os.path.abspath(WORKING_DIRECTORY) + "/"

if PASS_DIRECTORY:
    if not os.path.isdir(PASS_DIRECTORY):
        error_message = "Error: Pass directory %s does not exist." % PASS_DIRECTORY
        sys.exit(error_message)
if not PASS_DIRECTORY:
    PASS_DIRECTORY = WORKING_DIRECTORY + "reads/downloads/pass/"
PASS_DIRECTORY = os.path.abspath(PASS_DIRECTORY) + "/"

METRICS_DIRECTORY = WORKING_DIRECTORY + "metrics/"
if not os.path.isdir(METRICS_DIRECTORY):
    os.mkdir(METRICS_DIRECTORY)

mux_file = METRICS_DIRECTORY + RUN_NAME + ".mux_aggregate_txt"
mux_output = open(mux_file, "a+")

for fast5file in os.listdir(PASS_DIRECTORY):
        channel = fast5file.split('_')[-3]
        channel_num = channel.replace("ch",'')
        read = fast5file.split('_')[-2]
        read_num = read.replace("read", '')
        #print fast5file
        #print channel_num
        #print read_num
        f = h5py.File(PASS_DIRECTORY + fast5file)
        #print f["/Raw/Reads/Read_" + read_num].attrs.values()[2]
        mux_output.write(channel_num + "\t" + str(f["/Raw/Reads/Read_" + read_num].attrs.values()[2]) + "\n")

mux_output.close()

os.system("mux_stats.R %s %s" % (mux_file, RUN_NAME))

