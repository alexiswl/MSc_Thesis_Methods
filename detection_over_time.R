#!/usr/bin/env Rscript

args = commandArgs(trailingOnly = TRUE)

# This program enquires how many species are produced over time.

summary_table = read.table(args[1])

library(plyr)

names(summary_table) = c("Taxid", "Freq")

summary_table_count = count(summary_table, vars="Taxid")

total_alignments = sum(summary_table_count$freq)

threshold = 6 + total_alignments/1000

print(nrow(summary_table_count[summary_table_count$freq > threshold, ]))

