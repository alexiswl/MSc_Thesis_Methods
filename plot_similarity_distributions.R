#!/usr/bin/env Rscript

main_directory = "/data/Bioinfo/bioinfo-proj-alexis/2016_08_2016_08_16_E_COLI_R9/waterman/"
# Intracomparison test
fwd_rev_fasta_failed <- read.table(paste(main_directory, "intracomparison/fwd_rev/failed_quality_waterman_stats"))
twod_rev_fasta_failed <- read.table(paste(main_directory, "intracomparison/2d_rev/failed_quality_waterman_stats"))
twod_fwd_fasta_failed <- read.table(paste(main_directory, "intracomparison/2d_fwd/failed_quality_waterman_stats"))

fwd_rev_fasta_pass <- read.table(paste(main_directory, "intracomparison/fwd_rev/pass_waterman_stats"))
twod_rev_fasta_pass <- read.table(paste(main_directory, "intracomparison/2d_rev/pass_waterman_stats"))
twod_fwd_fasta_pass <- read.table(paste(main_directory, "intracomparison/2d_fwd/pass_waterman_stats"))

names(fwd_rev_fasta_failed) <- c("Filename", "Alignment_Score", "Similarity", "Identity")
names(twod_rev_fasta_failed) <-  c("Filename", "Alignment_Score", "Similarity", "Identity")
names(twod_fwd_fasta_failed) <- c("Filename", "Alignment_Score", "Similarity", "Identity")

names(fwd_rev_fasta_pass) <- c("Filename", "Alignment_Score", "Similarity", "Identity")
names(twod_rev_fasta_pass) <-  c("Filename", "Alignment_Score", "Similarity", "Identity")
names(twod_fwd_fasta_pass) <- c("Filename", "Alignment_Score", "Similarity", "Identity")

png("nanonet2d_similarity.png", type = "cairo")
plot(density(as.numeric(sub("%", "", fwd_rev_fasta_pass$Similarity)), from = 0, to = 100), ylim=c(0,0.1), col = "blue",
main = "Distribution of Similarity Scores", xlab = "Similarity Percentage")
lines(density(as.numeric(sub("%", "", twod_rev_fasta_pass$Similarity))), col = "green")
lines(density(as.numeric(sub("%", "", twod_fwd_fasta_pass$Similarity))), col = "red")
lines(density(as.numeric(sub("%", "", fwd_rev_fasta_failed$Similarity))), col = "blue", lty = "2")
lines(density(as.numeric(sub("%", "", twod_rev_fasta_failed$Similarity))), col = "green", lty = "2")
lines(density(as.numeric(sub("%", "", twod_fwd_fasta_failed$Similarity))), col = "red", lty = "2")

legend_labels = c("2d vs fwd (pass)", "2d vs rev (pass)", "fwd vs rev (pass)",
                  "2d vs fwd (failed)", "2d vs rev (failed)", "fwd vs rev (rev)")

legend("topleft",legend=legend_labels, col = rep(c("red","green","blue"),2), lty = rep(c(1,2), each = 2))
dev.off()

# Cross comparison test 2d
cross_2d = read.table(paste(main_directory, "cross_comparison/2D_waterman_stats"))
names(cross_2d) <- c("Read_name", "Alignment_Score", "Identity", "Similarity")

png("2D_comparison_local_vs_cloud", type="cairo")
hist(as.numeric(sub("%", "", cross_2d$Identity)), main = "Histogram of Similarity between Local and Cloud Basecalling - 1D")
dev.off()

# Cross comparison test 1d
cross_1d = read.table(paste(main_directory, "cross_comparison/1D_waterman_stats"))
names(cross_1d) <- c("Read_name", "Alignment_Score", "Identity", "Similarity")

png("1D_comparison_local_vs_cloud", type="cairo")
hist(as.numeric(sub("%", "", cross_1d$Identity)), main = "Histogram of Similarity between Local and Cloud Basecalling - 1D")
dev.off()

