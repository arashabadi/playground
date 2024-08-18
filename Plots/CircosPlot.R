# Install required packages
#install.packages("readxl")
#install.packages("circlize")
#install.packages("ComplexHeatmap")
library(readxl)
library(circlize)
library(ComplexHeatmap)

# Set the working directory
dir <- "E:/0Projects/CircosPlot"
setwd(dir)

# Set scipen to a high value to prevent scientific notation
set.seed(42)
options(scipen = 999)

# Read the Excel file
DEL <- as.data.frame(read_excel("NEW v5_complete.xlsx", sheet = 2))
DUP <- as.data.frame(read_excel("NEW v5_complete.xlsx", sheet = 3)) 
INV <- as.data.frame(read_excel("NEW v5_complete.xlsx", sheet = 4)) 
OTHER <- as.data.frame(read_excel("NEW v5_complete.xlsx", sheet = 5)) 
TRA <- as.data.frame(read_excel("NEW v5_complete.xlsx", sheet = 6))

# Define colors for each sample type
sample_colors <- c("ALL" = "#0080FF", "AML" = "#00994C", "CLL" = "#FF0000",
                   "MDS" = "#CC00CC", "Prenatal" = "#404040")

# Define shapes for each technology type
tech_shapes <- c("SOC" = 17, "SOC&OGM" = 16, "OGM" = 15) # 16: circle, 17: triangle, 18: square

# GENERATE the plot
pdf("plot_with_legends.pdf", width = 20 , height = 20)

# Initialize circos plot with extra space for legends
circos.par("start.degree" = 90,
           "gap.degree" = c(rep(2,23),3),
           "canvas.xlim" = c(-1.5, 1.5),
           "canvas.ylim" = c(-1.5, 1.5))


circos.initializeWithIdeogram(species = "hg19")

# Add genomic tracks with points colored by type and shaped by tech
circos.genomicTrackPlotRegion(DEL, 
  panel.fun = function(region, value, ...) {
  col <- sample_colors[value$type]
  pch <- tech_shapes[value$tech]
  circos.genomicPoints(region, value, col = col, pch = pch, cex = 0.8, ...)},
  track.height = 0.08, # Set the track height
  ylim = c(0, 1),
  bg.border = NA,   # No border
  bg.col = "gray95" # Light gray background
  )


DUP <- na.omit(DUP)
circos.genomicTrackPlotRegion(DUP, 
  panel.fun = function(region, value, ...) {
  col <- sample_colors[value$type]
  pch <- tech_shapes[value$tech]
  circos.genomicPoints(region, value, col = col, pch = pch, cex = 0.8, ...)},
  track.height = 0.08, # Set the track height
  ylim = c(0, 1),
  bg.border = NA,   # No border
  bg.col = "gray96" # Light gray background
)

circos.genomicTrackPlotRegion(INV, 
  panel.fun = function(region, value, ...) {
  col <- sample_colors[value$type]
  pch <- tech_shapes[value$tech]
  circos.genomicPoints(region, value, col = col, pch = pch, cex = 0.8, ...)},
  track.height = 0.08, # Set the track height
  ylim = c(0, 1),
  bg.border = NA,   # No border
  bg.col = "gray97" # Light gray background
)

circos.genomicTrackPlotRegion(OTHER, panel.fun = function(region, value, ...) {
  col <- sample_colors[value$type]
  pch <- tech_shapes[value$tech]
  circos.genomicPoints(region, value, col = col, pch = pch, cex = 0.8, ...)},
  track.height = 0.08, # Set the track height
  ylim = c(0, 1),
  bg.border = NA,   # No border
  bg.col = "gray98" # Light gray background
)

TRA <- na.omit(TRA)
for (i in 1:nrow(TRA)) {
  type <- TRA$type[i]
  tech <- TRA$tech[i]
  col <- sample_colors[type]
  lty_map <- c("SOC&OGM" = 1, "SOC" = 2, "OGM" = 3) # 1: solid, 2: dashed, 3: dotted
  lty <- lty_map[tech]
  
  circos.link(
    sector.index1 = TRA$from_chr[i], point1 = c(TRA$from_start[i], TRA$from_end[i]),
    sector.index2 = TRA$to_chr[i], point2 = c(TRA$to_start[i], TRA$to_end[i]),
    col = col, lty = lty , lwd = 1.5 #, border = NA
  )
}

# Add track labels in the gap (4 degrees) vertically
track_labels <- c("DELETION", "DUPLICATION", "INVERSION", "OTHER")
#track_labels <- c("DELETION", "DUPLICATION", "INVERSION", "OTHER", "TRANSLOCATION")
track_y_positions <- c(5, 3.5, 2, 0.5)

for (i in seq_along(track_labels)) {
  circos.text(x = 25, y = track_y_positions[i], labels = track_labels[i], 
              sector.index = "chr1", facing = "clockwise", niceFacing = TRUE,
              adj = c(0.5, -1), cex = 0.7, font = 2)
}

# Clear circos plot
circos.clear()

# Create legends
sample_legend <- Legend(at = names(sample_colors), 
                        type = "points", 
                        legend_gp = gpar(col = sample_colors),
                        title = "Sample Types")

tech_legend <- Legend(at = names(tech_shapes), 
                      type = "points", 
                      legend_gp = gpar(col = "black"), 
                      pch = tech_shapes,
                      title = "Technology Types")

line_types <- c("SOC&OGM" = "solid", "SOC" = "dashed", "OGM" = "dotted")

line_legend <- Legend(at = names(line_types), 
                      type = "lines", 
                      legend_gp = gpar(lty = c(1, 2, 3), col = "black"),
                      title = "Line Types")

# Draw legends
pushViewport(viewport(x = 1.35, y = 1.11, just = c("right", "top")))
draw(sample_legend)
upViewport()

pushViewport(viewport(x = 1.355, y = 1.05, just = c("right", "top")))
draw(tech_legend)
upViewport()

pushViewport(viewport(x = 1.35, y = 1, just = c("right", "top")))
draw(line_legend)
upViewport()

dev.off()

