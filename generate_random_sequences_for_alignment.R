#!/usr/bin/env Rscript

file1 = "reads1"
nucleotides = c("A","C","G","T")
file2 = "reads2"
for (i in 1:200){
  read_number = i
  read_line = paste(">read_", i, sep="")
  sequence_1 <- paste(sample(nucleotides, size=2000, replace=TRUE), collapse="")
  write(read_line, file1, append=TRUE)
  write(sequence_1, file1, append=TRUE)

  sequence_2 <- paste(sample(nucleotides, size=2000, replace=TRUE), collapse="")
  write(read_line, file2, append=TRUE)
  write(sequence_2, file2, append=TRUE)
}
