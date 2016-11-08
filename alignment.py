#!/usr/bin/env python

import os
import sys
import argparse
import time

# Declare directories
WORKING_DIRECTORY = ""
FASTA_DIRECTORY = ""
FASTQ_DIRECTORY = ""
ALIGNMENT_DIRECTORY = ""
STATS_DIRECTORY = ""
VISUALS_DIRECTORY = ""
ALIGNER_DIRECTORY = ""

# Declare global files
LOG_FILE = ""
REFERENCE_FILE = ""
SAM_FILE = ""
BAM_FILE = ""
SORTED_BAM_FILE_NO_SUFFIX = ""
SORTED_BAM_FILE = ""
SORTED_BAM_FILE_INDEX = ""

# Declare miscellaneous
version = 1.0
START_TIME = time.time()
END_TIME = time.time()
DATE_PREFIX = str(time.strftime("%Y-%m-%d"))
RUN_NAME = ""
THREAD_COUNT = 0
ALIGNER = ""
ALIGNMENT_CHOICES = ('bwa-mem', 'graphmap', 'last')
READS_DIRECTORY = ""
READS_FILE = ""
TMP_DIRECTORY = ""
SAMPLE_PREFIX = ""
IS_1D = False
FAIL = False

# Set defaults
THREAD_COUNT_DEFAULT = 20
IS_FASTA = False


def get_commandline_params():
    help_descriptor = "Converts a folder of fasta or fastq files" \
                      "align to a reference and then run SAM to sorted BAM and index pipeline. \n" + \
                      "A log file is generated producing the flag stat output. \n" \
                      "Can also provide just a directory for the SAM file. \n" \
                      "This will find all SAM files within the specified directory.\n"

    parser = argparse.ArgumentParser(description=help_descriptor)

    parser.add_argument("--run_name", dest="RUN_NAME", type=str,
                        help="Name of the alignment run")
    parser.add_argument("--working_directory", dest="WORKING_DIRECTORY", type=str,
                        help="The directory where will do the alignment.")
    parser.add_argument("--reads_directory", dest="READS_DIRECTORY", type=str,
                        help="Where are the fasta/fastq files?")
    parser.add_argument("--alignment_method", dest="ALIGNER", type=str,
                        choices=ALIGNMENT_CHOICES, required=True)
    parser.add_argument("--reference", dest="REFERENCE_FILE", type=str,
                        help="path to the reference", required=True)
    parser.add_argument("--log", nargs='?', dest="LOG_FILE", type=str,
                        help="Capture the output of the alignment. Also gives alignment metrics.")
    parser.add_argument("--1D", action='store_true', dest="IS_1D",
                        help="Used for findings fasta files is directory structure.")
    parser.add_argument("--fail", action='store_true', dest="FAIL",
                        help="Analyse the fail reads from metrichor.")
    parser.add_argument("--threads", nargs='?', dest="THREAD_COUNT", type=int,
                        help="Number of processes used during view and sort. Default is %d" % THREAD_COUNT_DEFAULT)
    data_type = parser.add_mutually_exclusive_group(required=True)
    data_type.add_argument('--fasta', action='store_true', dest="IS_FASTA")
    data_type.add_argument('--fastq', action='store_false', dest="IS_FASTA")

    args = parser.parse_args()
    return args


def set_commandline_variables(args):
    global THREAD_COUNT, WORKING_DIRECTORY, IS_FASTA, READS_DIRECTORY
    global RUN_NAME, LOG_FILE, ALIGNER, REFERENCE_FILE, SAM_FILE, IS_1D, FAIL

    RUN_NAME = args.RUN_NAME
    WORKING_DIRECTORY = args.WORKING_DIRECTORY
    READS_DIRECTORY = args.READS_DIRECTORY
    ALIGNER = args.ALIGNER
    REFERENCE_FILE = args.REFERENCE_FILE
    IS_1D = args.IS_1D
    FAIL = args.FAIL
    LOG_FILE = args.LOG_FILE
    THREAD_COUNT = args.THREAD_COUNT
    IS_FASTA = args.IS_FASTA


def set_directories():
    global THREAD_COUNT, WORKING_DIRECTORY, IS_FASTA, READS_DIRECTORY
    global LOG_FILE, REFERENCE_FILE, ALIGNMENT_DIRECTORY, SAMPLE_PREFIX, TMP_DIRECTORY
    global SAM_FILE, BAM_FILE, SORTED_BAM_FILE_NO_SUFFIX, SORTED_BAM_FILE_INDEX, SORTED_BAM_FILE
    global STATS_DIRECTORY, VISUALS_DIRECTORY, ALIGNER_DIRECTORY

    if not os.path.isdir(WORKING_DIRECTORY):
        error_message = "Error, working directory does not exist."
        sys.exit(error_message)
    WORKING_DIRECTORY = os.path.abspath(WORKING_DIRECTORY) + "/"

    if not READS_DIRECTORY:
        if IS_FASTA:
            READS_DIRECTORY = WORKING_DIRECTORY + "fasta/"
            if IS_1D:
                READS_DIRECTORY += "1D/"
            else:
                READS_DIRECTORY += "2D/2d/"
        else:
            READS_DIRECTORY = WORKING_DIRECTORY + "fastq/"
            if IS_1D:
                READS_DIRECTORY += "1D/"
            else:
                READS_DIRECTORY += "2D/"
            if FAIL:  # Is fastq
                READS_DIRECTORY += "fail/"
            else:
                READS_DIRECTORY += "pass/"
            if not IS_1D:
                READS_DIRECTORY += "2d/"
    if not os.path.isfile(REFERENCE_FILE):
        error_message = "Could not find reference file."
        sys.exit(error_message)
    REFERENCE_FILE = os.path.abspath(REFERENCE_FILE)

    if LOG_FILE:
        if not os.path.isfile(LOG_FILE):
            error_message = "Error, log file specified but does not exist." \
                            "Please create this file first."
            sys.exit(error_message)
    else:
        log_directory = WORKING_DIRECTORY + "log/"
        if not os.path.isdir(log_directory):
            os.mkdir(log_directory)
        LOG_FILE = log_directory + DATE_PREFIX + "_" + RUN_NAME + "." + ALIGNER + ".txt"

    if not THREAD_COUNT:
        general_message = "Thread count has not been specified. Using %s \n" % THREAD_COUNT_DEFAULT
        print(general_message)
        THREAD_COUNT = THREAD_COUNT_DEFAULT

    ALIGNMENT_DIRECTORY = WORKING_DIRECTORY + "alignment/"
    if not os.path.isdir(ALIGNMENT_DIRECTORY):
        os.mkdir(ALIGNMENT_DIRECTORY)

    TMP_DIRECTORY = ALIGNMENT_DIRECTORY + "tmp/"
    if not os.path.isdir(TMP_DIRECTORY):
        os.mkdir(TMP_DIRECTORY)

    ALIGNER_DIRECTORY = ALIGNMENT_DIRECTORY + ALIGNER + "/"
    if not os.path.isdir(ALIGNER_DIRECTORY):
        os.mkdir(ALIGNER_DIRECTORY)

    if IS_FASTA:
        ALIGNER_DIRECTORY += "fasta/"
        if not os.path.isdir(ALIGNER_DIRECTORY):
            os.mkdir(ALIGNER_DIRECTORY)
        if IS_1D:
            ALIGNER_DIRECTORY += "1D/"
        else:
            ALIGNER_DIRECTORY += "2D/2d"
        if not os.path.isdir(ALIGNER_DIRECTORY):
            os.mkdir(ALIGNER_DIRECTORY)
    else:
        ALIGNER_DIRECTORY += "fastq/"
        if not os.path.isdir(ALIGNER_DIRECTORY):
            os.mkdir(ALIGNER_DIRECTORY)
        if IS_1D:
            ALIGNER_DIRECTORY += "1D/"
        else:
            ALIGNER_DIRECTORY += "2D/"
        if not os.path.isdir(ALIGNER_DIRECTORY):
            os.mkdir(ALIGNER_DIRECTORY)
        if FAIL:
            ALIGNER_DIRECTORY += "fail/"
        else:
            ALIGNER_DIRECTORY += "pass/"
        if not IS_1D:
            READS_DIRECTORY += "2d/"
        if not os.path.isdir(ALIGNER_DIRECTORY):
            os.mkdir(ALIGNER_DIRECTORY)

    STATS_DIRECTORY = ALIGNER_DIRECTORY + "stats/"
    if not os.path.isdir(STATS_DIRECTORY):
        os.mkdir(STATS_DIRECTORY)

    VISUALS_DIRECTORY = STATS_DIRECTORY + "visuals/"
    if not os.path.isdir(VISUALS_DIRECTORY):
        os.mkdir(VISUALS_DIRECTORY)

    SAMPLE_PREFIX = ALIGNER_DIRECTORY + DATE_PREFIX + "_" + RUN_NAME + "_" + ALIGNER

    SAM_FILE = SAMPLE_PREFIX + ".sam"
    BAM_FILE = SAMPLE_PREFIX + ".bam"
    SORTED_BAM_FILE_NO_SUFFIX = SAMPLE_PREFIX + ".sorted"
    SORTED_BAM_FILE = SORTED_BAM_FILE_NO_SUFFIX + ".bam"
    SORTED_BAM_FILE_INDEX = SORTED_BAM_FILE_NO_SUFFIX + ".bai"

    os.chdir(WORKING_DIRECTORY)


def start_log():
    logger = open(LOG_FILE, "a+")
    logger.write("Commencing alignment using %s at %s.\n" % (ALIGNER, time.strftime("%c")))
    logger.write("Working directory is %s.\n" % WORKING_DIRECTORY)
    logger.write("Reference file is %s.\n" % REFERENCE_FILE)
    logger.write("Number of threads used is %s.\n" % THREAD_COUNT)
    logger.write("Read directory is %s\n" % READS_DIRECTORY)
    logger.close()


def concatenate_files():
    logger = open(LOG_FILE, "a+")
    global READS_FILE
    if IS_FASTA:
        READS_FILE = TMP_DIRECTORY + "all_reads.fasta"
        logger.write("Concatenating files to %s at %s.\n" % (READS_FILE, time.strftime("%c")))
        fasta_files = [READS_DIRECTORY + reads_file for reads_file in os.listdir(READS_DIRECTORY)
                       if reads_file.endswith('fasta')]
        for fasta_file in fasta_files:
            os.system("cat %s >> %s" % (fasta_file, READS_FILE))
    else:
        READS_FILE = TMP_DIRECTORY + "all_reads.fastq"
        logger.write("Concatenating files to %s at %s.\n" % (READS_FILE, time.strftime("%c")))
        fastq_files = [READS_DIRECTORY + reads_file for reads_file in os.listdir(READS_DIRECTORY)
                       if reads_file.endswith('fastq')]
        for fastq_file in fastq_files:
            os.system("cat %s >> %s" % (fastq_file, READS_FILE))
    logger.write("Completed concatenation of files at %s.\n" % time.strftime("%c"))
    logger.close()


def run_bwa_index():
    bwa_index_command = "bwa index %s 2>> %s" % (REFERENCE_FILE, LOG_FILE)
    logger = open(LOG_FILE, "a+")
    logger.write("Commencing indexing of reference file at %s.\n" % time.strftime("%c"))
    logger.close()

    start_function_time = time.time()
    os.system(bwa_index_command)
    end_function_time = time.time()

    logger = open(LOG_FILE, "a+")
    logger.write("Completed indexing of reference file %s" % time.strftime("%c"))
    logger.write("in %d seconds.\n" % (end_function_time - start_function_time))
    logger.close()


def run_bwa_mem():
    bwa_command_options = []
    bwa_command_options.append("-t %s" % THREAD_COUNT)
    bwa_command_options.append("-x ont2d")
    bwa_command_options.append("%s" % REFERENCE_FILE)
    bwa_command_options.append("%s" % READS_FILE)

    bwa_command = "bwa mem %s 1> %s 2>> %s" % (' '.join(bwa_command_options), SAM_FILE, LOG_FILE)

    logger = open(LOG_FILE, "a+")
    logger.write("Commencing bwa mem at %s.\n" % time.strftime("%c"))
    logger.write("The command is:\n %s\n" % bwa_command)
    logger.close()

    start_function_time = time.time()
    os.system(bwa_command)
    end_function_time = time.time()

    logger = open(LOG_FILE, "a+")
    logger.write("Completed bwa alignment at %s " % time.strftime("%c"))
    logger.write("In %d seconds.\n" % (end_function_time - start_function_time))
    logger.close()


def run_graphmap():
    graphmap_command_options = []
    graphmap_command_options.append("-r %s" % REFERENCE_FILE)
    graphmap_command_options.append("-d %s" % READS_FILE)
    graphmap_command_options.append("-o %s" % SAM_FILE)
    graphmap_command_options.append("-t %s" % THREAD_COUNT)

    graphmap_command = "graphmap align %s 2>> %s" % (' '.join(graphmap_command_options), LOG_FILE)

    logger = open(LOG_FILE, "a+")
    logger.write("Commencing graphmap at %s.\n" % time.strftime("%c"))
    logger.write("The command is:\n %s\n" % graphmap_command)
    logger.close()

    start_function_time = time.time()
    os.system(graphmap_command)
    end_function_time = time.time()

    logger = open(LOG_FILE, "a+")
    logger.write("Completed graphmap at %s " % time.strftime("%c"))
    logger.write("in %d seconds.\n" % (end_function_time - start_function_time))
    logger.close()


def run_last_index():
    last_index_command = "lastdb %s %s" % (REFERENCE_FILE, REFERENCE_FILE)
    logger = open(LOG_FILE, "a+")
    logger.write("Commencing last index of database at %s.\n" % time.strftime("%c"))
    logger.write("The command is:\n %s\n" % last_index_command)
    logger.close()

    start_function_time = time.time()
    os.system(last_index_command)
    end_function_time = time.time()

    logger = open(LOG_FILE, "a+")
    logger.write("Completed last indexing at %s " % time.strftime("%c"))
    logger.write("in %d seconds.\n" % (end_function_time - start_function_time))


def run_last():
    maf_file = ALIGNER_DIRECTORY + DATE_PREFIX + "_" + RUN_NAME + "_last.maf"
    last_command = "lastal %s %s 1> %s 2>> %s" % (REFERENCE_FILE, READS_FILE, maf_file, LOG_FILE)
    maf_convert_command = "maf-convert.py sam %s 2>> %s" % (maf_file, LOG_FILE)

    logger = open(LOG_FILE, "a+")
    logger.write("Commencing last at %s.\n" % time.strftime("%c"))
    logger.write("The command is:\n %s\n" % last_command)
    logger.close()

    start_function_time = time.time()
    os.system(last_command)
    end_function_time = time.time()

    logger = open(LOG_FILE, "a+")
    logger.write("Completed last alignment at %s " % time.strftime("%c"))
    logger.write("in %d seconds.\n" % (end_function_time - start_function_time))

    # convert last to sam file.
    logger.write("Now converting from maf file to sam file at %s\n" % time.strftime("%c"))
    logger.write("The command is:\n %s\n" % maf_convert_command)
    logger.close()

    start_function_time = time.time()
    os.system(maf_convert_command)
    end_function_time = time.time()

    logger = open(LOG_FILE, "a+")
    logger.write("Completed conversion at %s " % time.strftime("%c"))
    logger.write("in %d seconds.\n" % (end_function_time - start_function_time))
    logger.close()


def convert_sam_to_bam():
    sam_to_bam_command = "samtools view -bS -o %s -@ %d %s 2>> %s" % (BAM_FILE, THREAD_COUNT, SAM_FILE, LOG_FILE)
    sort_bam_file_command = "samtools sort -@ %d %s -o %s 2>> %s" % (THREAD_COUNT, BAM_FILE,
                                                                     SORTED_BAM_FILE, LOG_FILE)
    index_sorted_bam_file_command = "samtools index %s %s 2>> %s" % (SORTED_BAM_FILE, SORTED_BAM_FILE_INDEX, LOG_FILE)

    # Run sam to bam command.
    logger = open(LOG_FILE, "a+")
    logger.write("Commencing conversion of sam to bam at %s.\n" % time.strftime("%c"))
    logger.write("The command is:\n %s\n" % sam_to_bam_command)
    logger.close()

    start_function_time = time.time()
    os.system(sam_to_bam_command)
    end_function_time = time.time()

    logger = open(LOG_FILE, "a+")
    logger.write("Completed conversion of sam to bam at %s " % time.strftime("%c"))
    logger.write("In %d seconds.\n" % (end_function_time - start_function_time))

    # Run sort bam file command
    logger.write("Now sorting bam file at: %s\n" % time.strftime("%c"))
    logger.write("The command is:\n %s\n" % sort_bam_file_command)
    logger.close()

    start_function_time = time.time()
    os.system(sort_bam_file_command)
    end_function_time = time.time()

    logger = open(LOG_FILE, "a+")
    logger.write("Completed sorting of bam file alignment at %s " % time.strftime("%c"))
    logger.write("in %d seconds.\n" % (end_function_time - start_function_time))

    # Run index bam file command.
    logger.write("Now indexing sorted bam file at %s. \n" % time.strftime("%c"))
    logger.write("The command is:\n %s\n" % index_sorted_bam_file_command)
    logger.close()

    start_function_time = time.time()
    os.system(index_sorted_bam_file_command)
    end_function_time = time.time()

    logger = open(LOG_FILE, "a+")
    logger.write("Completed indexing of sorted bam file at %s " % time.strftime("%c"))
    logger.write("In %d seconds.\n" % (end_function_time - start_function_time))
    logger.write("Now indexing sorted bam file at %s. \n" % time.strftime("%c"))
    logger.write("The command is:\n %s\n" % index_sorted_bam_file_command)
    logger.close()


def get_stats():
    stat_prefix = STATS_DIRECTORY + DATE_PREFIX + "_" + RUN_NAME + "_" + ALIGNER
    flagstat_file = stat_prefix + ".flagstat.txt"
    stats_file = stat_prefix + ".stats.txt"

    flagstat_command = "samtools flagstat %s > %s 2>> %s" % (SORTED_BAM_FILE, flagstat_file, LOG_FILE)
    stats_command = "samtools stats %s > %s 2>> %s" % (SORTED_BAM_FILE, stats_file, LOG_FILE)
    plot_bam_stats_command = "plot-bamstats -p %s %s 2>> %s" % (VISUALS_DIRECTORY, stats_file, LOG_FILE)

    logger = open(LOG_FILE, "a+")
    logger.write("Now using flagstat to analyse dataset at %s." % time.strftime("%c"))
    logger.write("The command is:\n %s\n" % flagstat_command)
    logger.close()

    start_function_time = time.time()
    os.system(flagstat_command)
    end_function_time = time.time()

    logger = open(LOG_FILE, "a+")
    logger.write("Completed flagstat analysis at %s " % time.strftime("%c"))
    logger.write("In %d seconds.\n" % (end_function_time - start_function_time))

    logger.write("Now using samtools stats analysis at %s.\n" % time.strftime("%c"))
    logger.write("The command is:\n %s\n" % stats_command)
    logger.close()

    start_function_time = time.time()
    os.system(stats_command)
    end_function_time = time.time()

    logger = open(LOG_FILE, "a+")
    logger.write("Completed stat analysis at %s " % time.strftime("%c"))
    logger.write("In %d seconds.\n" % (end_function_time - start_function_time))


    logger = open(LOG_FILE, "a+")
    logger.write("Now plotting stats output using bamstats at %s." % time.strftime("%c"))
    logger.write("The command is:\n %s\n" % plot_bam_stats_command)
    logger.close()

    start_function_time = time.time()
    os.system(plot_bam_stats_command)
    end_function_time = time.time()

    logger = open(LOG_FILE, "a+")
    logger.write("Completed plotting stats output using bamstats at %s " % time.strftime("%c"))
    logger.write("In %d seconds.\n" % (end_function_time - start_function_time))


def end_log():
    global END_TIME
    END_TIME = time.time()
    logger = open(LOG_FILE, "a+")
    logger.write("Completed sam to bam and analysis pipeline at %s" % time.strftime("%c"))
    logger.write("The total time was %d seconds" % (END_TIME - START_TIME))


def main():
    # Get commandline parameters:
    args = get_commandline_params()

    # Set commandline parameters to respective script variables
    set_commandline_variables(args)

    # Set and create directories
    set_directories()

    # Initilise the log file
    start_log()

    # Concatentate the fasta/fastq files
    concatenate_files()

    # Run aligner
    if ALIGNER == "bwa-mem":
        run_bwa_index()
        run_bwa_mem()
    elif ALIGNER == "graphmap":
        run_graphmap()
    else:
        run_last_index()
        run_last()

    # Convert sam file to bam file.
    convert_sam_to_bam()

    # Get alignment statistics
    get_stats()

    # Write to end log
    end_log()

    # Remove temporary directory
    os.system("rm -rf %s" % TMP_DIRECTORY)


main()
