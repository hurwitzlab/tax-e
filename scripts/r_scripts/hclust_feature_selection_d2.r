#install.packages("devtools")
library(devtools) # get from CRAN with install.packages("devtools")
#install_github("ririzarr/rafalib")
library(rafalib)
#install.packages("dplyr")
library(dplyr)
#install.packages("dplyr")
library(dplyr)
#install.packages("RColorBrewer")
library(RColorBrewer) 

#####################################################################
# Hclust 
# using the ward.D2 method
#####################################################################

# get the working directory
dir <- getwd()
# set the working directory
setwd(dir)

## Log transformed data
setwd("../../data/freqs_2/log") 

### All data

# Load data
combined <- as.data.frame(read.csv(file = "all.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
combined <- combined %>% select(-target)
combined <- cbind(targets,combined)

# Perform hierarchical clustering
d_data <- dist(as.matrix(combined))   # find distance matrix 
hc_data <- hclust(d_data, method = "ward.D2")       
targets_chr <- sapply(targets, unlist)

cols <- palette(brewer.pal(11, "Paired"))[as.fumeric(targets_chr)]
cols <- palette(brewer.pal(11, "Paired"))[as.fumeric(targets_chr)]

#dev.off()
#Plot data
mypar(1,1)
myplclust(hc_data, main = "log all data", labels=targets_chr, 
          lab.col=cols, cex=0.5)


### filter GO terms > depth 2

# Load data
combined <- as.data.frame(read.csv(file = "depth_02.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
combined <- combined %>% select(-target)
combined <- cbind(targets,combined)

# Perform hierarchical clustering
d_data <- dist(as.matrix(combined))   # find distance matrix 
hc_data <- hclust(d_data, method = "ward.D2")       
targets_chr <- sapply(targets, unlist)

#Plot data
mypar(1,1)
myplclust(hc_data, main = "log depth > 2", labels=targets_chr, 
          lab.col=cols, cex=0.5)

### filter GO terms > depth 3

# Load data
combined <- as.data.frame(read.csv(file = "depth_03.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
combined <- combined %>% select(-target)
combined <- cbind(targets,combined)

# Perform hierarchical clustering
d_data <- dist(as.matrix(combined))   # find distance matrix 
hc_data <- hclust(d_data, method = "ward.D2")       
targets_chr <- sapply(targets, unlist)

#Plot data
mypar(1,1)
myplclust(hc_data, main = "log depth > 3", labels=targets_chr, 
          lab.col=cols, cex=0.5)


### filter GO terms > depth 4

# Load data
combined <- as.data.frame(read.csv(file = "depth_04.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
combined <- combined %>% select(-target)
combined <- cbind(targets,combined)

# Perform hierarchical clustering
d_data <- dist(as.matrix(combined))   # find distance matrix 
hc_data <- hclust(d_data, method = "ward.D2")       
targets_chr <- sapply(targets, unlist)

#Plot data
mypar(1,1)
myplclust(hc_data, main = "log depth > 4", labels=targets_chr, 
          lab.col=cols, cex=0.5)

### filter GO terms > depth 5

# Load data
combined <- as.data.frame(read.csv(file = "depth_05.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
combined <- combined %>% select(-target)
combined <- cbind(targets,combined)

# Perform hierarchical clustering
d_data <- dist(as.matrix(combined))   # find distance matrix 
hc_data <- hclust(d_data, method = "ward.D2")       
targets_chr <- sapply(targets, unlist)

#Plot data
mypar(1,1)
myplclust(hc_data, main = "log depth > 5", labels=targets_chr, 
          lab.col=cols, cex=0.5)

### filter GO terms > depth 6

# Load data
combined <- as.data.frame(read.csv(file = "depth_06.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
combined <- combined %>% select(-target)
combined <- cbind(targets,combined)

# Perform hierarchical clustering
d_data <- dist(as.matrix(combined))   # find distance matrix 
hc_data <- hclust(d_data, method = "ward.D2")       
targets_chr <- sapply(targets, unlist)

#Plot data
mypar(1,1)
myplclust(hc_data, main = "log depth > 6", labels=targets_chr, 
          lab.col=cols, cex=0.5)

### filter GO terms > depth 7

# Load data
combined <- as.data.frame(read.csv(file = "depth_07.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
combined <- combined %>% select(-target)
combined <- cbind(targets,combined)

# Perform hierarchical clustering
d_data <- dist(as.matrix(combined))   # find distance matrix 
hc_data <- hclust(d_data, method = "ward.D2")       
targets_chr <- sapply(targets, unlist)

#Plot data
mypar(1,1)
myplclust(hc_data, main = "log depth > 7", labels=targets_chr, 
          lab.col=cols, cex=0.5)


### filter GO terms > depth 8

# Load data
combined <- as.data.frame(read.csv(file = "depth_08.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
combined <- combined %>% select(-target)
combined <- cbind(targets,combined)

# Perform hierarchical clustering
d_data <- dist(as.matrix(combined))   # find distance matrix 
hc_data <- hclust(d_data, method = "ward.D2")       
targets_chr <- sapply(targets, unlist)

#Plot data
mypar(1,1)
myplclust(hc_data, main = "log depth > 8", labels=targets_chr, 
          lab.col=cols, cex=0.5)

### filter GO terms > depth 9

# Load data
combined <- as.data.frame(read.csv(file = "depth_09.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
combined <- combined %>% select(-target)
combined <- cbind(targets,combined)

# Perform hierarchical clustering
d_data <- dist(as.matrix(combined))   # find distance matrix 
hc_data <- hclust(d_data, method = "ward.D2")       
targets_chr <- sapply(targets, unlist)

#Plot data
mypar(1,1)
myplclust(hc_data, main = "log depth > 9", labels=targets_chr, 
          lab.col=cols, cex=0.5)

### filter GO terms > depth 10

# Load data
combined <- as.data.frame(read.csv(file = "depth_10.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
combined <- combined %>% select(-target)
combined <- cbind(targets,combined)

# Perform hierarchical clustering
d_data <- dist(as.matrix(combined))   # find distance matrix 
hc_data <- hclust(d_data, method = "ward.D2")       
targets_chr <- sapply(targets, unlist)

#Plot data
mypar(1,1)
myplclust(hc_data, main = "log depth > 10", labels=targets_chr, 
          lab.col=cols, cex=0.5)


#########################################################################

## Term Frequency normalized data
setwd("../tf") 
#setwd("../../data/freqs_2/tf") 

#setwd("/Users/kai/Desktop/software/tax-e/data/freqs_2/tf") #//set the working directory here:

### All data

# Load data
combined <- as.data.frame(read.csv(file = "all.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
combined <- combined %>% select(-target)
combined <- cbind(targets,combined)

# Perform hierarchical clustering
d_data <- dist(as.matrix(combined))   # find distance matrix 
hc_data <- hclust(d_data, method = "ward.D2")       
targets_chr <- sapply(targets, unlist)

#Plot data
mypar(1,1)
myplclust(hc_data, main = "TF all data", labels=targets_chr, 
          lab.col=cols, cex=0.5)


######################################################
#Feature selection for specific GO hierarchy subclasses
#using the log_transformed data

## Log transformed data
#setwd("/Users/kai/Desktop/software/tax-e/data/freqs_2/log") #//set the working directory here:
setwd("../log") 

### alpha-amino acid biosynthetic process
combined <- as.data.frame(read.csv(file = "alpha-amino_acid_biosynthetic_process.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
combined <- combined %>% select(-target)
combined <- cbind(targets,combined)

# Perform hierarchical clustering
d_data <- dist(as.matrix(combined))   # find distance matrix 
hc_data <- hclust(d_data, method = "ward.D2")       
targets_chr <- sapply(targets, unlist)

#Plot data
mypar(1,1)
myplclust(hc_data, main = "alpha-amino acid biosynthetic process", labels=targets_chr, 
          lab.col=cols, cex=0.5)



### ATPase activity
combined <- as.data.frame(read.csv(file = "ATPase_activity.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
combined <- combined %>% select(-target)
combined <- cbind(targets,combined)

# Perform hierarchical clustering
d_data <- dist(as.matrix(combined))   # find distance matrix 
hc_data <- hclust(d_data, method = "ward.D2")       
targets_chr <- sapply(targets, unlist)

#Plot data
mypar(1,1)
myplclust(hc_data, main = "ATPase activity", labels=targets_chr, 
          lab.col=cols, cex=0.5)





### nucleoside_phosphate_metabolic_process
combined <- as.data.frame(read.csv(file = "nucleoside_phosphate_metabolic_process.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
combined <- combined %>% select(-target)
combined <- cbind(targets,combined)

# Perform hierarchical clustering
d_data <- dist(as.matrix(combined))   # find distance matrix 
hc_data <- hclust(d_data, method = "ward.D2")       
targets_chr <- sapply(targets, unlist)

#Plot data
mypar(1,1)
myplclust(hc_data, main = "nucleoside phosphate metabolic process", labels=targets_chr, 
          lab.col=cols, cex=0.5)


### tRNA metabolic process
combined <- as.data.frame(read.csv(file = "tRNA_metabolic_process.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
combined <- combined %>% select(-target)
combined <- cbind(targets,combined)

# Perform hierarchical clustering
d_data <- dist(as.matrix(combined))   # find distance matrix 
hc_data <- hclust(d_data, method = "ward.D2")       
targets_chr <- sapply(targets, unlist)

#Plot data
mypar(1,1)
myplclust(hc_data, main = "tRNA metabolic process", labels=targets_chr, 
          lab.col=cols, cex=0.5)

#########
### translation_assoc
#Having searched GO for many translation associated classes,
# and having retrieved their subclasses and used all of them
#to feature select down we get 99 GO classes as features.  

combined <- as.data.frame(read.csv(file = "translation_assoc.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
combined <- combined %>% select(-target)
combined <- cbind(targets,combined)

# Perform hierarchical clustering
d_data <- dist(as.matrix(combined))   # find distance matrix 
hc_data <- hclust(d_data, method = "ward.D2")       
targets_chr <- sapply(targets, unlist)

#Plot data
mypar(1,1)
myplclust(hc_data, main = "Translation Associated", labels=targets_chr, 
          lab.col=cols, cex=0.5)



### nucleoside-triphosphatase_activity.csv
combined <- as.data.frame(read.csv(file = "nucleoside-triphosphatase_activity.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
combined <- combined %>% select(-target)
combined <- cbind(targets,combined)

# Perform hierarchical clustering
d_data <- dist(as.matrix(combined))   # find distance matrix 
hc_data <- hclust(d_data, method = "ward.D2")       
targets_chr <- sapply(targets, unlist)

#Plot data
mypar(1,1)
myplclust(hc_data, main = "nucleoside-triphosphatase activity", labels=targets_chr, 
          lab.col=cols, cex=0.5)

