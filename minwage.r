require(ggplot2)

#setwd('~/Desktop/r scripts')

#reads in poverty series and makes index into colnames
df.poverty <- read.csv('data/state2yrpovrate1993-2010.csv',na.strings = 'NA')
rownames(df.poverty) <- df.poverty[,'X']
df.poverty <- df.poverty[colnames(df.poverty)[colnames(df.poverty)!='X']]

#reads in minwage series and makes index into colnames
df.minwage <- read.csv('data/minwage.csv',na.strings = '...',sep = '\t')
rownames(df.minwage) <- df.minwage[,'State.or.other.jurisdiction']
df.minwage <- df.minwage[colnames(df.minwage)[colnames(df.minwage)!='State.or.other.jurisdiction']]

#Fills in NAs with federal minwage
for(col in colnames(df.minwage)){
    df.minwage[col][is.na(df.minwage[col])] <- df.minwage['FLSA',col]
}

#fixes labeling discrepancy
rownames(df.minwage)[rownames(df.minwage) == 'District of Columbia'] <- 'D.C.'
rownames(df.minwage)[rownames(df.minwage) == 'FLSA'] <- 'U.S.'

#constrains columns to same range
colnames(df.poverty) <- seq(1994,2004,1)
colnames(df.minwage) <- c('1988','1991','1992','1994','1996','1997','1998','2000','2001','2002','2003','2004','2005','2006')
df.minwage <- df.minwage[,c('1994','1996','1997','1998','2000','2001','2002','2003')]

#makes column names distinguishable
#colnames(df.poverty) <- paste('p.',colnames(df.poverty))
#colnames(df.minwage) <- paste('mw.',colnames(df.minwage))

#joins two dataframes and removes memory storage of df.minwage
#df.poverty <- cbind(df.poverty,df.minwage)
#rm(df.minwage)


#returns years with different minimum wages from previous year
get.vlines <- function(col){
  #sets up comparison vector
  lagged <- append(df.minwage[col,],NA,after = 0)[1:8]
  return(which(df.minwage[col,] > lagged))

}

makeggplots <- function(locale = 'U.S.') {
#write it from scratch because this isn't working.
  
  vlines <- get.vlines(locale)
  cols <- colnames(df.poverty)
  
  pl <- ggplot(aes(x = cols[1:11],y = df.poverty[locale,1:11]))
  pl <- pl + geom_point()
  
#  ggsave(filename=paste('plots/',locale,'.png'),height=6)
}

