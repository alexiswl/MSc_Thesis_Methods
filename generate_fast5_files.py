#!/usr/bin/env python

import os
import random

# Generate a random set of fast5 files
NUM_FILES = 150
folder = ""
for random_file_index in range(0, NUM_FILES):
    channel = int(random.random()*512 + 0.5)
    read = int(random.random()*5000 + 0.5)
    random_file = "fake_run_ch" + str(channel) + "_" + str(read) + ".fast5"

os.system("touch %s%s" % (folder, random_file))

