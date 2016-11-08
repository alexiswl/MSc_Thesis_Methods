#!/usr/bin/env Rscript

args = commandArgs(trailingOnly = TRUE)

run_distribution_table = args[1]
nanonet2d_distribution_table = args[2]
RUN_NAME = args[3]

metrichor_data <- read.table(run_distribution_table, header = TRUE, sep = "\t")
nanonet_data <- read.table(nanonet2d_distribution_table, header = TRUE, sep = "\t")

# Remove X from column name.
metrichor_column_names <- gsub("^X", "", names(metrichor_data))
nanonet_column_names <- gsub("^X", "", names(nanonet_data))
names(metrichor_data) <- metrichor_column_names
names(nanonet_data) <- nanonet_column_names
calibration_strand_columns = grepl("Calibration*", names(metrichor_data))
metrichor_calibration_data <- metrichor_data[,calibration_strand_columns]
nanonet_calibration_data <- nanonet_data[,calibration_strand_columns]
metrichor_sample_data <- metrichor_data[,!calibration_strand_columns]
nanonet_sample_data <- nanonet_data[,!calibration_strand_columns]

metrichor_calibration_data_names <- gsub("^Calibration_strand_detected.", "", names(metrichor_calibration_data))
nanonet_calibration_data_names <- gsub("^Calibration_strand_detected.", "", names(nanonet_calibration_data))
names(metrichor_calibration_data) <- metrichor_calibration_data_names
names(nanonet_calibration_data) <- nanonet_calibration_data_names

calibration_data_names = c("2D basecall not performed", "2D failed quality filters", "Passed quality")
metrichor_calibration_data <- cbind(metrichor_calibration_data$`2D_basecall_not_performed`,
                                    metrichor_calibration_data$`2D_failed_quality_filters`,
                                    metrichor_calibration_data$Passed_quality)
nanonet_calibration_data <- cbind(nanonet_calibration_data$`2D_basecall_not_performed`,
                                  nanonet_calibration_data$`2D_failed_quality_filters`,
                                  nanonet_calibration_data$Passed_quality)


colours = c("darkolivegreen3", "red3")

# Produce the calibration strand plot.
metrichor_calibration_data_num <- as.numeric(metrichor_calibration_data)
nanonet_calibration_data_num <- as.numeric(nanonet_calibration_data)
diff_calibration_data <- metrichor_calibration_data_num - nanonet_calibration_data_num
matrix_for_plot <- matrix(c(nanonet_calibration_data_num, diff_calibration_data), nrow=2, byrow=TRUE)

png("nanonet_vs_metrichor_calibration_plot.png", type = "cairo")
bp <- barplot(matrix_for_plot, xlab = "", ylab = "Number of Reads", col = colours,
              main = paste(c("Distribution of 2D Local Basecalling in ", RUN_NAME, " (calibration strands)")))
text(bp, par("usr")[3], cex=0.8, labels = calibration_data_names, adj = c(0.5,2), xpd = TRUE)
legend("topleft", legend = c("Local 2D basecalling performed", "Metrichor"),
       col = colours, pch = 15)
dev.off()

# Reorder sample data by column name
sample_data_names <- c("Unknown error","Corrupted files","No template data", "1D basecall not performed",
                    "No complement data", "2D basecall not performed", "2D failed quality filters", "pass")

metrichor_sample_data <- cbind(metrichor_sample_data$Unknown_error, metrichor_sample_data$Corrupted_files,
                               metrichor_sample_data$No_template_data, metrichor_sample_data$`1D_basecall_not_performed`,
                               metrichor_sample_data$No_complement_data, metrichor_sample_data$`2D_basecall_not_performed`,
                               metrichor_sample_data$`2D_failed_quality_filters`, metrichor_sample_data$pass)

nanonet_sample_data <- cbind(nanonet_sample_data$Unknown_error, nanonet_sample_data$Corrupted_files,
                             nanonet_sample_data$No_template_data, nanonet_sample_data$`1D_basecall_not_performed`,
                             nanonet_sample_data$No_complement_data, nanonet_sample_data$`2D_basecall_not_performed`,
                             nanonet_sample_data$`2D_failed_quality_filters`, nanonet_sample_data$pass)

metrichor_sample_data <- as.data.frame(metrichor_sample_data)
nanonet_sample_data <- as.data.frame(nanonet_sample_data)
names(metrichor_sample_data) <- sample_data_names
names(nanonet_sample_data) <- sample_data_names

# Create plot
metrichor_sample_data_num <- as.numeric(metrichor_sample_data)
nanonet_sample_data_num <- as.numeric(nanonet_sample_data)

diff_sample_data <- metrichor_sample_data_num - nanonet_sample_data_num
matrix_for_plot <- matrix(c(nanonet_sample_data_num, diff_sample_data),
                          nrow=2, byrow=TRUE)

label_cex = c(rep(0.7, 3), 0.55, 0.7, 0.6, 0.7, 1)
png("nanonet_vs_metrichor_sample_data.png", type = "cairo")
bp <- barplot(matrix_for_plot, col = colours, ylab = "Number of Reads", main =
                paste(c("Distribution of 2D Local Basecalling in ", RUN_NAME)))
text(bp, par("usr")[3], cex=label_cex, labels = sample_data_names, adj = c(1.1,1.1), srt=45, xpd = TRUE)
legend("topleft", legend = c("Local 2D basecalling performed", "Metrichor"),
       col = colours, pch = 15)
dev.off()