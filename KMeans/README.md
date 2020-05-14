# KMeans
[股票分群code](https://github.com/jiaying777/E.SUN_Fugle_project/blob/master/KMeans/Kmeans.ipynb)<br>
[股票分群結果.csv](https://github.com/jiaying777/E.SUN_Fugle_project/blob/master/KMeans/stock_kmesns.csv)

## 資料
上市上櫃股票：
* 殖利率
* 本益比
* 淨值比
* Beta

## 做法
### 分群判斷

* 手軸法：找出轉折處
* 輪廓係數法：找出分數最高的
* calinski harabaz score：找出分數最高的

👉 結論為分5群 

### 訓練模型

- 使用KMenas將資料作分群，並設`n_clusters = 5`。<br>
- 完成分群後再找出每群的特徵，並固定質心，以避免每次訓練出來的分群不同。

<img src='https://github.com/jiaying777/FinTech/blob/master/KMeans/特徵.png'>
<img src='https://github.com/jiaying777/FinTech/blob/master/KMeans/stock_Kmeans.png' width=80%>

### 分群特徵

    label 0：殖利率偏高、群內標準差大
    label 1：beta係數顯著偏高
    label 2：本益比整體偏高、beta係數顯著次高
    label 3：淨值比顯著偏高
    label 4：各項數值皆偏低
    
<img src='https://github.com/jiaying777/FinTech/blob/master/KMeans/殖利率_.png'>
<img src='https://github.com/jiaying777/FinTech/blob/master/KMeans/本益比_.png'>
<img src='https://github.com/jiaying777/FinTech/blob/master/KMeans/淨值比_.png'>
<img src='https://github.com/jiaying777/FinTech/blob/master/KMeans/beta_.png'>
