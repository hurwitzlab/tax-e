library(vegan)
library(ggplot2)
library(dplyr)
library(tidyr)


#####################################################################

## Log transformed data
setwd("/Users/kai/Desktop/software/tax-e/data/freqs_1/log") #//set the working directory here:

### All data

# Load data
combined <- as.data.frame(read.csv(file = "all.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
combined <- combined %>% select(-target)
combined <- cbind(targets,combined)

# doing pcoa on my data
my.dis <- vegdist(decostand(combined[,-1],"hellinger")) 
my.pcoa <- cmdscale(my.dis, eig = TRUE)

with(combined, levels(target))
colors_vec <-palette(rainbow(8))
#try to fix it from here https://www.fromthebottomoftheheap.net/2012/04/11/customising-vegans-ordination-plots/
#get the species names
my.pcoa$species <- wascores(my.pcoa$points, combined[,-1], expand = TRUE)

#plot the figure
fig <- ordiplot(my.pcoa, type = "none")
#text(fig, "species", col="#d43e24", cex=0.9)
points(fig, "sites", col=colors_vec,  cex=1, pch=19)



### filter GO terms =< depth 4

# Load data
combined <- as.data.frame(read.csv(file = "depth_04.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
combined <- combined %>% select(-target)
combined <- cbind(targets,combined)

# doing pcoa on my data
my.dis <- vegdist(decostand(combined[,-1],"hellinger")) 
my.pcoa <- cmdscale(my.dis, eig = TRUE)

with(combined, levels(target))
colors_vec <-palette(rainbow(8))
#try to fix it from here https://www.fromthebottomoftheheap.net/2012/04/11/customising-vegans-ordination-plots/
#get the species names
my.pcoa$species <- wascores(my.pcoa$points, combined[,-1], expand = TRUE)

#plot the figure
fig <- ordiplot(my.pcoa, type = "none")
#text(fig, "species", col="#d43e24", cex=0.9)
points(fig, "sites", col=colors_vec,  cex=1, pch=19)


### filter GO terms =< depth 7

# Load data
combined <- as.data.frame(read.csv(file = "depth_07.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
combined <- combined %>% select(-target)
combined <- cbind(targets,combined)

# doing pcoa on my data
my.dis <- vegdist(decostand(combined[,-1],"hellinger")) 
my.pcoa <- cmdscale(my.dis, eig = TRUE)

with(combined, levels(target))
colors_vec <-palette(rainbow(8))
#try to fix it from here https://www.fromthebottomoftheheap.net/2012/04/11/customising-vegans-ordination-plots/
#get the species names
my.pcoa$species <- wascores(my.pcoa$points, combined[,-1], expand = TRUE)

#plot the figure
fig <- ordiplot(my.pcoa, type = "none")
#text(fig, "species", col="#d43e24", cex=0.9)
points(fig, "sites", col=colors_vec,  cex=1, pch=19)

