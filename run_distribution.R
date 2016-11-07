#!/usr/bin/env Rscript

args = commandArgs(trailingOnly = TRUE)

input_table = args[1]
RUN_NAME = args[2]

all_data <- read.table(input_table, header = TRUE)
# Remove X from column name.
new_all_data_names <- gsub("^X", "", names(all_data))
names(all_data) <- new_all_data_names
calibration_strands = grepl("Calibration*", names(all_data))
calibration_data <- all_data[,calibration_strands]
run_data <- all_data[,!calibration_strands]
calibration_data_names <- gsub("^Calibration_strand_detected.", "", names(calibration_data))
names(calibration_data) <- calibration_data_names
calibration_data_names = c("2D basecall not performed", "2D failed quality filters", "Passed quality")
calibration_data <- cbind(calibration_data$`2D_basecall_not_performed`,
calibration_data$`2D_failed_quality_filters`,
calibration_data$Passed_quality)
colours = c("red3", "darkorange", "darkolivegreen3")

# Produce the calibration strand plot.
png("calibration_plot.png")
bp <- barplot(as.numeric(calibration_data), xlab = "", ylab = "Number of Reads", col = colours,
main = paste(c("Distribution of calibration strands in ", RUN_NAME)))
text(bp, par("usr")[3], cex=0.8, labels = calibration_data_names, adj = c(0.5,2), xpd = TRUE)
dev.off()

# Reorder by column name
run_data_names <- c("Unknown error","Corrupted files","No template data", "1D basecalled not performed",
                    "No complement data", "2D basecall not performed", "2D failed quality filters", "pass")
run_data <- cbind(run_data$Unknown_error, run_data$Corrupted_files, run_data$No_template_data,
                  run_data$`1D_basecall_not_performed`, run_data$No_complement_data,
                  run_data$`2D_basecall_not_performed`, run_data$`2D_failed_quality_filters`, run_data$pass)
run_data <- as.data.frame(run_data)
names(run_data) <- run_data_names

# Create plot
colours = c(rep("red3", 5), rep("darkorange", 2), "darkolivegreen3")
png("overall_plot.png")
bp <- barplot(as.numeric(run_data), col = colours, ylab = "Number of Reads", main =
paste(c("Distribution of output in "), RUN_NAME))
text(bp, par("usr")[3], cex=0.5, labels = run_data_names, adj = c(1.1,1.1), srt=45, xpd = TRUE)
dev.off()
