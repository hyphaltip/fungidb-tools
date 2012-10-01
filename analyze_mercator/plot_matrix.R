inp<-read.table("jason.tsv",header=T,sep="\t",row.names=1)
inp <- 1 - inp;
dat<-as.matrix(inp)

rd<-dist(dat)
rc<-hclust(rd)
cd<-dist(t(dat))
cc<-hclust(cd)

pdf("heatmap_synteny.pdf")
heatmap(dat, Rowv=as.dendrogram(rc), Colv=as.dendrogram(cc),scale="none")
