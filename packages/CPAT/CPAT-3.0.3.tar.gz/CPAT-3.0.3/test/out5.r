load("Human_logitModel.RData")
test <- read.table(file="out5.ORF_info.tsv",sep="\t",header=T)
test$Coding_prob <- predict(mylogit,newdata=test,type="response")
write.table(test, file="out5.ORF_prob.tsv", quote=F, sep="\t",row.names=FALSE, col.names=TRUE)
