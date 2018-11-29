# Heatmap
#install.packages("dplyr")
library(dplyr)
#install.packages("RColorBrewer")
library(RColorBrewer) 
#install.packages(genefilter)
library(genefilter)
#install.packages("gplots")
library(gplots) ##Available from CRAN

#install_github("ririzarr/rafalib")
library(rafalib)

# get the working directory
dir <- getwd()
# set the working directory
setwd(dir)

## Log transformed data
setwd("../../data/freqs_1/log") 

### All data
combined <- as.data.frame(read.csv(file = "all.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
targets_chr <- sapply(targets, unlist)

#set the heatmap colors
hmcol <- colorRampPalette(brewer.pal(9, "GnBu"))(100)

combined <- as.data.frame(read.csv(file = "all_tr.csv",header = TRUE,row.names = 1))
c <- as.matrix(combined)
rv_data <- rowVars(c)
idx_data <- order(-rv_data )[1:60]
cols <- palette(brewer.pal(8, "Dark2"))[as.fumeric(targets_chr)]
hclust.ward <- function(c) hclust(c, method="ward.D2")
full <- heatmap.2(c[idx_data,], labCol=targets_chr,
                  trace="none", ColSideColors=cols,
                  col=hmcol, hclustfun=hclust.ward )


### filter GO terms > depth 8
combined <- as.data.frame(read.csv(file = "depth_08.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
targets_chr <- sapply(targets, unlist)

combined <- as.data.frame(read.csv(file = "depth_08_tr.csv",header = TRUE,row.names = 1))
c <- as.matrix(combined)
rv_data <- rowVars(c)
idx_data <- order(-rv_data )[1:25]
cols <- palette(brewer.pal(8, "Dark2"))[as.fumeric(targets_chr)]
hclust.ward <- function(c) hclust(c, method="ward.D2")
full <- heatmap.2(c[idx_data,], labCol=targets_chr,
                  trace="none", ColSideColors=cols,
                  col=hmcol, hclustfun=hclust.ward )


### filter GO terms > depth 10
combined <- as.data.frame(read.csv(file = "depth_10.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
targets_chr <- sapply(targets, unlist)
combined <- as.data.frame(read.csv(file = "depth_10_tr.csv",header = TRUE,row.names = 1))
c <- as.matrix(combined)
rv_data <- rowVars(c)
idx_data <- order(-rv_data )[1:25] #also looks ok with top 30 GO terms
cols <- palette(brewer.pal(8, "Dark2"))[as.fumeric(targets_chr)]
hclust.ward <- function(c) hclust(c, method="ward.D2")



mypar(1,1)
full <- heatmap.2(c[idx_data,], labCol=targets_chr,
                  trace="none", ColSideColors=cols, 
                  col=hmcol, hclustfun=hclust.ward )

#########################################################################


## Term Frequency normalized data
setwd("../tf") 

### All data
combined <- as.data.frame(read.csv(file = "all.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
targets_chr <- sapply(targets, unlist)

combined <- as.data.frame(read.csv(file = "all_tr.csv",header = TRUE,row.names = 1))
c <- as.matrix(combined)
rv_data <- rowVars(c)
idx_data <- order(-rv_data )[1:25]
cols <- palette(brewer.pal(8, "Dark2"))[as.fumeric(targets_chr)]
hclust.ward <- function(c) hclust(c, method="ward.D2")
full <- heatmap.2(c[idx_data,], labCol=targets_chr,
                  trace="none", ColSideColors=cols,
                  col=hmcol, hclustfun=hclust.ward )


### filter GO terms > depth 8
combined <- as.data.frame(read.csv(file = "depth_08.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
targets_chr <- sapply(targets, unlist)

combined <- as.data.frame(read.csv(file = "depth_08_tr.csv",header = TRUE,row.names = 1))
c <- as.matrix(combined)
rv_data <- rowVars(c)
idx_data <- order(-rv_data )[1:60]
cols <- palette(brewer.pal(8, "Dark2"))[as.fumeric(targets_chr)]
hclust.ward <- function(c) hclust(c, method="ward.D2")
full <- heatmap.2(c[idx_data,], labCol=targets_chr,
                  trace="none", ColSideColors=cols,
                  col=hmcol, hclustfun=hclust.ward )


### filter GO terms > depth 10
combined <- as.data.frame(read.csv(file = "depth_10.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
targets_chr <- sapply(targets, unlist)

combined <- as.data.frame(read.csv(file = "depth_10_tr.csv",header = TRUE,row.names = 1))
c <- as.matrix(combined)
rv_data <- rowVars(c)
idx_data <- order(-rv_data )[1:25] #also looks ok with top 30 GO terms
cols <- palette(brewer.pal(8, "Dark2"))[as.fumeric(targets_chr)]
hclust.ward <- function(c) hclust(c, method="ward.D2")

mypar(1,1)
full <- heatmap.2(c[idx_data,], labCol=targets_chr,
                  trace="none", ColSideColors=cols, 
                  col=hmcol, hclustfun=hclust.ward )



#########################################################################



## -Log Term Frequency normalized data (nlog_tf)
setwd("../nlog_tf") 

#setwd("/Users/kai/Desktop/software/tax-e/data/freqs_1/nlog_tf") 


### filter GO terms > depth 10
combined <- as.data.frame(read.csv(file = "depth_10.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
targets_chr <- sapply(targets, unlist)

combined <- as.data.frame(read.csv(file = "depth_10_tr.csv",header = TRUE,row.names = 1))
c <- as.matrix(combined)
rv_data <- rowVars(c)
idx_data <- order(-rv_data )[1:25] #also looks ok with top 30 GO terms
cols <- palette(brewer.pal(8, "Dark2"))[as.fumeric(targets_chr)]
hclust.ward <- function(c) hclust(c, method="ward.D2")

mypar(1,1)
full <- heatmap.2(c[idx_data,], labCol=targets_chr,
                  trace="none", ColSideColors=cols, 
                  col=hmcol, hclustfun=hclust.ward )


#########################################################################


## augmented frequency normalized data (aug_freq)
setwd("../aug_freq") 

### filter GO terms > depth 10
combined <- as.data.frame(read.csv(file = "depth_10.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
targets_chr <- sapply(targets, unlist)

combined <- as.data.frame(read.csv(file = "depth_10_tr.csv",header = TRUE,row.names = 1))
c <- as.matrix(combined)
rv_data <- rowVars(c)
idx_data <- order(-rv_data )[1:25] #also looks ok with top 30 GO terms
cols <- palette(brewer.pal(8, "Dark2"))[as.fumeric(targets_chr)]
hclust.ward <- function(c) hclust(c, method="ward.D2")

mypar(1,1)
full <- heatmap.2(c[idx_data,], labCol=targets_chr,
                  trace="none", ColSideColors=cols, 
                  col=hmcol, hclustfun=hclust.ward )


############## making a legend
# labels <- unique(unlist(targets_chr))
# colors_vect <- unique(unlist(cols))
# legend('top',  labels, lty=c(1,1), lwd=c(2.5,2.5),col=colors_vect)




######################################################
#Feature selection for specific GO hierarchy subclasses
#using the log_transformed data


## Log transformed data
setwd("../log") 

## alpha-amino acid biosynthetic process
combined <- as.data.frame(read.csv(file = "alpha-amino_acid_biosynthetic_process.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
targets_chr <- sapply(targets, unlist)

combined <- as.data.frame(read.csv(file = "alpha-amino_acid_biosynthetic_process_tr.csv",header = TRUE,row.names = 1))
c <- as.matrix(combined)
rv_data <- rowVars(c)
idx_data <- order(-rv_data )[1:21]
cols <- palette(brewer.pal(8, "Dark2"))[as.fumeric(targets_chr)]
hclust.ward <- function(c) hclust(c, method="ward.D2")
mypar(1,1)
full <- heatmap.2(c[idx_data,], labCol=targets_chr,
                  trace="none", ColSideColors=cols,
                  col=hmcol, hclustfun=hclust.ward )



## ATPase activity
combined <- as.data.frame(read.csv(file = "ATPase_activity.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
targets_chr <- sapply(targets, unlist)

combined <- as.data.frame(read.csv(file = "ATPase_activity_tr.csv",header = TRUE,row.names = 1))
c <- as.matrix(combined)
rv_data <- rowVars(c)
idx_data <- order(-rv_data )[1:19]
cols <- palette(brewer.pal(8, "Dark2"))[as.fumeric(targets_chr)]
hclust.ward <- function(c) hclust(c, method="ward.D2")
mypar(1,1)
full <- heatmap.2(c[idx_data,], labCol=targets_chr,
                  trace="none", ColSideColors=cols,
                  col=hmcol, hclustfun=hclust.ward )


## nucleoside phosphate metabolic process
combined <- as.data.frame(read.csv(file = "nucleoside_phosphate_metabolic_process.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
targets_chr <- sapply(targets, unlist)

combined <- as.data.frame(read.csv(file = "nucleoside_phosphate_metabolic_process_tr.csv",header = TRUE,row.names = 1))
c <- as.matrix(combined)
rv_data <- rowVars(c)
idx_data <- order(-rv_data )[1:40]
cols <- palette(brewer.pal(8, "Dark2"))[as.fumeric(targets_chr)]
hclust.ward <- function(c) hclust(c, method="ward.D2")
mypar(1,1)
full <- heatmap.2(c[idx_data,], labCol=targets_chr,
                  trace="none", ColSideColors=cols,
                  col=hmcol, hclustfun=hclust.ward )

## tRNA metabolic process
combined <- as.data.frame(read.csv(file = "tRNA_metabolic_process.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
targets_chr <- sapply(targets, unlist)

combined <- as.data.frame(read.csv(file = "tRNA_metabolic_process_tr.csv",header = TRUE,row.names = 1))
c <- as.matrix(combined)
rv_data <- rowVars(c)
idx_data <- order(-rv_data )[1:31]
cols <- palette(brewer.pal(8, "Dark2"))[as.fumeric(targets_chr)]
hclust.ward <- function(c) hclust(c, method="ward.D2")
mypar(1,1)
full <- heatmap.2(c[idx_data,], labCol=targets_chr,
                  trace="none", ColSideColors=cols,
                  col=hmcol, hclustfun=hclust.ward )


#########
### translation_assoc
#Having searched GO for many translation associated classes,
# and having retrieved their subclasses and used all of them
#to feature select down we get 99 GO classes as features.  

combined <- as.data.frame(read.csv(file = "translation_assoc.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
targets_chr <- sapply(targets, unlist)

combined <- as.data.frame(read.csv(file = "translation_assoc_tr.csv",header = TRUE,row.names = 1))
c <- as.matrix(combined)
rv_data <- rowVars(c)
idx_data <- order(-rv_data )[1:99]
cols <- palette(brewer.pal(8, "Dark2"))[as.fumeric(targets_chr)]
hclust.ward <- function(c) hclust(c, method="ward.D2")
mypar(1,1)
full <- heatmap.2(c[idx_data,], labCol=targets_chr,
                  trace="none", ColSideColors=cols,
                  col=hmcol, hclustfun=hclust.ward )

# To get the sample labels
#carpet <- full$carpet
#li <- rownames(carpet)
#lis <- sapply(li, unlist)
#View(li)
### again with column labels as the sample EBI numbers
# combined <- as.data.frame(read.csv(file = "translation_assoc.csv",header = TRUE))
# combined <- combined %>% select(-target)
# targets <- combined %>% select(samples)
# targets_chr <- sapply(targets, unlist)
# 
# combined <- as.data.frame(read.csv(file = "translation_assoc_tr_2.csv",header = TRUE,row.names = 1))
# c <- as.matrix(combined)
# rv_data <- rowVars(c)
# idx_data <- order(-rv_data )[1:99]
# cols <- palette(brewer.pal(8, "Dark2"))[as.fumeric(targets_chr)]
# hclust.ward <- function(c) hclust(c, method="ward.D2")
# mypar(1,1)
# full <- heatmap.2(c[idx_data,], labCol=targets_chr,
#                   trace="none", ColSideColors=cols,
#                   col=hmcol, hclustfun=hclust.ward,
#                   colCol=cols)
# 
# carpet <- full$carpet
# li <- rownames(carpet)
# lis <- sapply(li, unlist)
# View(li)