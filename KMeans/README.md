# KMeans
[股票分群code](https://github.com/jiaying777/E.SUN_Fugle_project/blob/master/KMeans/Kmeans.ipynb)<br>
## 做法：
利用手軸法、輪廓分析、calinski_harabaz_score判斷分成5群最好，使用KMeans將股票分成五群，並定義每一群的特徵。<br>

    label 0：殖利率偏高、群內標準差大
    label 1：beta係數顯著偏高
    label 2：本益比整體偏高、beta係數顯著次高
    label 3：淨值比顯著偏高
    label 4：各項數值皆偏低
