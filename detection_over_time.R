#!/usr/bin/env R

args = commandArgs(trailingOnly = TRUE)

# This program enquires how many species are produced over time.

summary_table = read.table(args[1])

library(plyr)

names(summary_table) = c("Taxid", "Freq")

summary_table_count = count(summary_table, vars="Taxid")

print length(summary_summary_table_count[summary_table_count$freq > 7, ])

