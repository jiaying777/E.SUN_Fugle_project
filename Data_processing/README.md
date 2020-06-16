# UDF
## 資料處理：
### 1.瀏覽次數：可以從看同一檔股票的頻繁次數→ 推測使用者的個性
[veiws.py](https://github.com/jiaying777/E.SUN_Fugle_project/blob/master/user-defined%20features/views.py)

    計算每個使用者觀看各股的次數，可以將此當作一個使用者特徵。

**使用資料：瀏覽紀錄**
<br>
<br>

### 2.產業比例：判斷使用者較常接觸的公司產業為何
[user_industry.py](https://github.com/jiaying777/E.SUN_Fugle_project/blob/master/Data_processing/user-defined%20features/user_industry.py)

    - 計算 (訂閱資料的各公司產業 * 0.7 + 瀏覽紀錄的各公司產業 * 0.3)的產業百分比。
    - 最後可得出使用者的產業權重比例，可當作特徵使用。


**使用資料：訂閱資料、瀏覽紀錄**
<br>
<br>

### 3.喜好產業：從訂閱資料中找出使用者較喜歡的產業
[user_subscribe.py](https://github.com/jiaying777/E.SUN_Fugle_project/blob/master/Data_processing/user-defined%20features/user_subscribe.py)

    - 統計訂閱資料中的產業次數，並將前 3 喜歡的產業抽取出來當作特徵。


**使用資料：**[產業比例](https://github.com/jiaying777/E.SUN_Fugle_project/tree/master/Data_processing#2產業比例判斷使用者較常接觸的公司產業為何)
<br>
<br>

### 4.喜好卡片：使用者習慣看的卡片
[prefer_card.py](https://github.com/jiaying777/E.SUN_Fugle_project/blob/master/Data_processing/user-defined%20features/prefer_card.py)

    - 從懶紀錄中可得出每位使用者習慣觀看哪些卡片資訊，可當作使用者特徵。
    
**使用資料：瀏覽資料**
<br>
<br>

### 5.股票共現關係：被同一個使用者訂閱或是瀏覽
[subscribe_recommend.py](https://github.com/jiaying777/E.SUN_Fugle_project/blob/084ed791512e9e72c23188680327cebf43c44b38/Data_processing/user-defined%20features/data_processing.py#L24)

    - 訂閱共現：出現在同一個使用者的訂閱清單中。 

[views_recommend.py](https://github.com/jiaying777/E.SUN_Fugle_project/blob/084ed791512e9e72c23188680327cebf43c44b38/Data_processing/user-defined%20features/data_processing.py#L45)

    - 瀏覽共現：被同一個使用者瀏覽過（資料較沒有價值。

**使用資料：訂閱資料、** [瀏覽次數](https://github.com/jiaying777/E.SUN_Fugle_project/tree/master/Data_processing#1瀏覽次數可以從看同一檔股票的頻繁次數-推測使用者的個性)
<br>
<br>


## to_do
- [x] 瀏覽資料: 可以從看同一檔股票的頻繁次數
- [x] 瀏覽資料: 可以從 cardName 自訂的多寡推斷用戶特性
- [x] 瀏覽資料: 可以從 cardName 內容推斷使用者較關注的資訊面向
- [x] 訂閱資料: 觀察個群體的組成和用戶自訂義的群組推斷用戶習慣
- [x] 訂閱資料: 關注股票相關產業比例，推斷用戶較愛的產業 
