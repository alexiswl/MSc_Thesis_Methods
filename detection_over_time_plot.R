#!/usr/bin/env Rscript

library(lubridate)

args = commandArgs(trailingOnly = TRUE)

# This program takes the species classified over time table and produces a plot.
# All of the tables need to be manipulated first

initial_table = read.table(args[1])
run_name = args[2]
# Split second variable into two variables
V2_split <- strsplit(as.character(initial_table$V2), " ")

total_reads_matched = array(0, dim=c(0,length(c)))
species_matched = array(0, dim=c(0,length(c)))

for (i in 1:length(c)){
    species_matched[i] = V2_split[[i]][1]
    total_reads_matched[i] = V2_split[[i]][2]
}

species_matched = as.numeric(species_matched) - 2
time = substr(as.character(initial_table$V1), 1, nchar(as.character(initial_table$V1))-3)

final_table = data.frame(time, species_matched, total_reads_matched)
pdf("species_over_time")
with(final_table, plot(time, species_matched, xlab = "Time (seconds)"), ylab = "Species Detected",
main = paste("Species Detected over Time ", run_name), type="l")
dev.off()

pdf("alignments_over_time")
with(final_table, plot(time, total_reads_matched, xlab = "Time (seconds)"), ylab = "Number of Alignments",
main = paste("Total Alignments over Time ", run_name), type="l")
dev.off()
