#!/usr/bin/env Rscript

args = commandArgs(trailingOnly = TRUE)

# This program produces run metrics such as:
# How many pores produced pass reads.
# A plot of the 'half-life' of each pore.

input_table = args[1]
run_name = args[2]
output_table = paste(run_name, ".mux_summary.txt", sep = "")
ouptut_plot = paste(run_name, ".pore_quality.png", sep = "")

mux <- read.table(input_table)

levels(mux) = 1:512
table_mux <- table(mux)

channels_with_reads = rownames(table_mux)
j = 1

all_channels_by_mux = matrix(, nrow = 512, ncol = 4)

for (i in 1:512){
  if (j > length(channels_with_reads)){
    # Don't want to go through next statement
  }
  else if(i == as.integer(channels_with_reads[j])){
    all_channels_by_mux[i,] = table_mux[j,]
    j = j + 1
    next
  }
  # Otherwise a dud channel
  dud_channel = matrix(c(0,0,0,0), 1, 4)
  all_channels_by_mux[i,] = dud_channel
}

channels_with_four_pores = sum(apply(all_channels_by_mux > 0, 1, sum) == 4)
channels_with_three_pores = sum(apply(all_channels_by_mux > 0, 1, sum) == 3) + channels_with_four_pores
channels_with_two_pores = sum(apply(all_channels_by_mux > 0, 1, sum) == 2) + channels_with_three_pores
channels_with_one_pore = sum(apply(all_channels_by_mux > 0, 1, sum) == 1) + channels_with_two_pores

sink(output_table)
print(paste("The total number of pores with pass reads is: ",sum(all_channels_by_mux > 0)))
print(paste("The total number of channels with one pore producing pass reads is ", channels_with_one_pore))
print(paste("The total number of channels with two pores producing pass reads is ", channels_with_two_pores))
print(paste("The total number of channels with three pores producing pass reads is ", channels_with_three_pores))
print(paste("The total number of channels with four pores producing pass reads is ", channels_with_four_pores))
print(paste("This can be seen as a histogram in ", hist_file))
sink()

hist(apply(all_channels_by_mux != 0 , 1,sum), breaks=c(-0.5, 0.5,1.5,2.5,3.5,4.5))

loghist <- function(x, ..., breaks="Sturges", main = paste("Histogram of", xname), xlab = xname, ylab = "Frequency") {
  xname = paste(deparse(substitute(x), 500), collapse="\n")
  h = hist(x, breaks=breaks, plot=FALSE)
  plot(h$breaks, c(NA,h$counts), type='S', main=main, xlab=xlab, ylab=ylab, axes=FALSE, ...)
  axis(1)
  axis(2)
  lines(h$breaks, c(h$counts,NA), type='s')
  lines(h$breaks, c(NA,h$counts), type='h')
  lines(h$breaks, c(h$counts,NA), type='h')
  lines(h$breaks, rep(0,length(h$breaks)), type='S')
  invisible(h)
}

png(output_plot, type = "cairo")
loghist(all_channels_by_mux,  main = paste("Pore Quality Distribution of", run_name),
        xlab = "Pass produced by pore", ylab = "Number of pores")
dev.off()
