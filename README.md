# 玉山證卷-fugleTrade-投資信鴿
- [投資信鴿](#投資信鴿)
  - [問題介紹](#問題介紹-)
  - [主要目標](#主要目標-)
  - [線上測試](#線上測試-)
- [我們的方法](#我們的方法)
  - [item-based](#item-based)
  - [user-based](#user-based)
  - [共現關係](#共現關係)
  - [資料處理](#資料處理)
  


<!---=================================================================================================================================
玉山方面提出的相關資料
-->
# 投資信鴿
## 問題介紹 <img src="https://img.icons8.com/pastel-glyph/64/000000/pen-1.png" weight="30" height="30"/> 
**針對玉山旗下兩個 app ([Fugle富果投資](https://play.google.com/store/apps/details?id=tw.fugle.android.app)、[玉山證券A+行動下單](https://play.google.com/store/apps/details?id=com.esun))，目前推波訊息功能主要是由用戶自己設定條件(如下圖)，所以玉山想發展自動化推波的功能，透過分析客戶行為，去偵測客戶喜好，自動化推波適合的內容給客戶，提升客戶體驗。相對來說，假如客戶收到有意思的資訊，就會點入查看，所以也會增加客戶使用 app 的頻率。**

<div align=center><img width="400" height="300" src="https://i.imgur.com/6LMTpbt.png" alt="玉山證券A+行動下單 app 示意圖"/></div>


## 主要目標 <img src="https://img.icons8.com/plasticine/100/000000/accuracy.png" weight="35" height="35"/> 
一檔股票在「特定條件或情境時」很「聰明」的找到適當的通知時機，⾃自動發出「特定內容」，能夠讓追蹤這檔股票的⽤用⼾戶，覺得這訊息對於他的投資有幫助，甚⾄至刺刺激股票交易的意願。

## 線上測試 <img src="https://img.icons8.com/color/48/000000/test-partial-passed.png" weight="30" height="30"/>
- 質化指標：根據與 mentor 的討論，自動推播提醒的內容要有投資幫助
- 量化指標：自動推播提醒（非顧客自行設定）， 每分鐘不超過 10 次，每週至少一次

<a href="https://icons8.com/icon/103935/development-skill">Development Skill icon by Icons8</a>

>[回目錄](#玉山證卷-fugleTrade-投資信鴿)
<!---=================================================================================================================================
我們作的東西
-->
# 我們的方法
## item-based 
根據公司的殖利率、本益比、股價淨值比、BETA值與現金水位，這5個比率當作公司特徵，並透過使用者的訂閱與觀看清單找出最相近的5間公司進行推薦。

    1. 使用者特徵：使用者訂閱清單中的公司各比率的平均 * 0.7 + 使用者瀏覽紀錄中的公司各比率的平均 * 0.3 
    2. 找出與使用者特徵最相近的公司，並進行推薦
    
**KMeans**
[KMeans](https://github.com/jiaying777/E.SUN_Fugle_project/tree/master/KMeans)：利用上述幾項比率將公司進行分群，但分群效果不好，所以最後不使用。

## user-based 
根據訂閱資料與瀏覽紀律計算出使用者的產業喜好，找出相似喜好的使用者並將其之訂閱清單推薦給使用者。

    1. 使用者特徵：使用者訂閱清單中的公司產業 * 0.7 + 使用者瀏覽紀錄中的公司產業 * 0.3
    2. 利用 KD-Tree 計算出與其歐式距離最相近者
    3. 隨機挑選最相近使用者的訂閱清單中還未訂閱過的公司進行推薦

## 共現關係
整理出各股之間的共現關係，當使用者觀看任何一檔股票時進行推薦，亦即「看過的人也看過」。

## 資料處理
**主要資料：**

    - 公司財務比率：TEJ 抓取
    - 訂閱清單：Fugle 提供
    - 瀏覽紀錄：Fugle 提供
    
資料處理：[資料處理程式及簡介](https://github.com/jiaying777/E.SUN_Fugle_project/tree/master/Data_processing)
（處理過後的資料最後並非全部都有使用）

處理後的資料有使用：
[產業比例](https://github.com/jiaying777/E.SUN_Fugle_project/tree/master/Data_processing#2產業比例判斷使用者較常接觸的公司產業為何)、
[股票共現](https://github.com/jiaying777/E.SUN_Fugle_project/tree/master/Data_processing#5股票共現關係被同一個使用者訂閱或是瀏覽)
<br>

**處理後資料沒使用原因：原本想要將使用者分類，但使用者特徵過少，就算根據將一些特徵抽出來，分類效果也不盡人意，因此最後選擇不使用。**


>[回目錄](#玉山證卷-fugleTrade-投資信鴿)

