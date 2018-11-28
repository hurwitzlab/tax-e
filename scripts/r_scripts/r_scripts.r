packages <- c("vegan", "ggplot2", "dplyr", "tidyr")
if (length(setdiff(packages, rownames(installed.packages()))) > 0) {
  install.packages(setdiff(packages, rownames(installed.packages())))  
}

library(vegan)
library(ggplot2)
library(dplyr)
library(tidyr)

#data filtering:
setwd("/Users/kai/Desktop/software/tax-e/data/freqs") #//set the working directory here:
  
#####################################################################
# log transformed data
combined <- as.data.frame(read.csv(file = "d1_subsample_log_all.csv",header = TRUE))
combined <- combined %>% select(-sample)
targets <- combined %>% select(target)
combined <- combined %>% select(-target)
combined <- cbind(targets,combined)

# pcoa on d1_subsample_log_all.csv
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
#legend('topright', legend=unique(colors_vec), col=unique(my.pcoa$points), pch = 16)

######################################################################
# workflow for hclust, kmeans and heatmap using
# example tissue gene expession data
# from https://genomicsclass.github.io/book/pages/clustering_and_heatmaps.html

# source("https://bioconductor.org/biocLite.R")
# biocLite("tissuesGeneExpression")
# biocLite("remotes")
# library(BiocInstaller)
# biocLite("genomicsclass/tissuesGeneExpression")
# library(tissuesGeneExpression)
# data(tissuesGeneExpression)

#hierarchical clustering
#install.packages("devtools")
library(devtools) # get from CRAN with install.packages("devtools")
install_github("ririzarr/rafalib")
library(rafalib)

#########################
# in my example targets is equivalent to tissue and combined to e.
#compute the distance between each sample:
d_data <- dist(as.matrix(combined))   # find distance matrix 
hc_data <- hclust(d_data, method = "ward.D2")       # apply hirarchical clustering 
targets_chr <- sapply(targets, unlist)

mypar(1,1)
myplclust(hc_data, labels=targets_chr, lab.col=as.fumeric(targets_chr), cex=0.5)

# cut the tree to look at the individual clusters
hclusters <- cutree(hc_data, h=110)
table(true=targets_chr, cluster=hclusters)

#We can also ask cutree to give us back a given number of clusters. The function then automatically finds the height that results in the requested number of clusters:

hclusters <- cutree(hc_data, k=6)
table(true=targets_chr, cluster=hclusters)

#### 
# tf (term freq) data
combined_tf <- as.data.frame(read.csv(file = "d1_subsample_tf_all.csv",header = TRUE))
combined_tf <- combined_tf %>% select(-sample)
targets <- combined_tf %>% select(target)
combined_tf <- combined_tf %>% select(-target)
combined_tf <- cbind(targets,combined_tf)

#compute the distance between each sample:
d_data <- dist(as.matrix(combined_tf))   # find distance matrix 
hc_data <- hclust(d_data, method = "ward.D")       # apply hirarchical clustering 
targets_chr <- sapply(targets, unlist)

mypar(1,1)
myplclust(hc_data, labels=targets_chr, lab.col=as.fumeric(targets_chr), cex=0.5)





# Heatmap
setwd("/Users/kai/Desktop/software/tax-e/scripts/r_scripts")

library(RColorBrewer) 
hmcol <- colorRampPalette(brewer.pal(9, "GnBu"))(100)

#source("https://bioconductor.org/biocLite.R")
#biocLite("genefilter")

#install.packages(genefilter)
library(genefilter)
#install.packages("gplots")
library(gplots) ##Available from CRAN

#rv <- rowVars(e)
#idx <- order(-rv)[1:40]


combined <- as.data.frame(read.csv(file = "d1_subsample_log_all_trans.csv",header = TRUE,row.names = 1))
c <- as.matrix(combined)

rv_data <- rowVars(c)
idx_data <- order(-rv_data )[1:60]

cols <- palette(brewer.pal(8, "Dark2"))[as.fumeric(targets_chr)]
head(cbind(colnames(c),cols))

hclust.ward <- function(c) hclust(c, method="ward.D2")

full <- heatmap.2(c[idx_data,], labCol=targets_chr,
                  trace="none", ColSideColors=cols, 
                  col=hmcol, hclustfun=hclust.ward )



row_dend <- cut(full[["rowDendrogram"]], h = 0)
row_dend$lower

col_dend <- cut(full[["colDendrogram"]], h= 100)
col_dend$lower


#####
# tf heatmap
combined <- as.data.frame(read.csv(file = "d1_subsample_tf_all_trans.csv",header = TRUE,row.names = 1))
c <- as.matrix(combined)

rv_data <- rowVars(c)
idx_data <- order(-rv_data )[1:60]
#install.packages("gplots")
#library(gplots) ##Available from CRAN

cols <- palette(brewer.pal(8, "Dark2"))[as.fumeric(targets_chr)]
head(cbind(colnames(c),cols))

hclust.ward <- function(c) hclust(c, method="ward.D2")

full_tf <- heatmap.2(c[idx_data,], labCol=targets_chr,
                  trace="none", ColSideColors=cols, 
                  col=hmcol, hclustfun=hclust.ward )
