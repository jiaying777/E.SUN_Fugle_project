#如果是使用RStudio軟體使用者可以執行
#下列兩行指令快速達成視窗清空的工作
rm(list = ls()) #清除RStudio軟體右邊環境視窗變數內容
cat("\014")     #清除RStudio軟體下方Console Window視窗內容


#資料集(dataset)：參考GroupLens is a research lab. 
#                 的MovieLens 100k(十萬筆電影評分資料)
#download the file from the URL
#https://grouplens.org/datasets/movielens/100k/

## step 1. load arules package
#install.packages("arules")
library(arules)

## step 2. Import and transform data

setwd("C:/data/ml-100k/")    # Set working directory. Make c:\data directory and copy csv file to the directory
getwd()             # Get working directory

# import raw data (csv file)
nw_data = read.table(file="u.data", header = F, sep = "" )
class(nw_data)      # "data.frame"
colnames(nw_data) = c("userID","movieNO","rating","time")

# group data by orderID. using column 1(OrderID) and 2(ProductName) only
nw_temp = tapply(nw_data[,2], nw_data[,1], paste)
nw_temp[1]          # get the first row data



nw2 = vector("list", length(nw_temp)) # length(nw_temp)=830
for (i in seq(nw_temp)) names(nw2)[i] = names(nw_temp[i])
for (i in seq(nw_temp)) nw2[[i]] = nw_temp[[i]]
class(nw2)          # "list"



# force data into transactions
nw = as(nw2, "transactions")
class(nw)           # "transactions"


# step 3. analyze data
# generate level plots to visually inspect binary incidence matrices
image(nw) # result - Figure 1 Level plot
summary(nw)

# step 4. find 1-items (L1)
# provides the generic function itemFrequency and the frequency/support for all single items in an objects based on itemMatrix.
itemFrequency(nw, type = "relative") # default: "relative"
itemFrequency(nw, type = "absolute")

# step 5.
# create an item frequency bar plot for inspecting the item frequency distribution for objects based on itemMatrix
itemFrequencyPlot(nw) # result- Figure 2 Item frequency bar plot

# step 6.
# mine association rules
# rules <- apriori(nw) # Mine association rules using default Apriori algorithm
r1 = apriori(nw, parameter = list(supp = 0.3, target = "frequent itemsets")) # set parameters
inspect(r1)

r2 <- apriori(nw, parameter = list(supp = 0.3, conf = 0.8, target = "rules")) # set parameters
inspect(r2)

r2_sorted = sort(r2, by = "lift")
inspect(r2_sorted)


# step7.
# display results
inspect(r1)       # display frequent itemset
inspect(r2[1:5])  # display association
inspect(r2)       # display association

#See you next time.