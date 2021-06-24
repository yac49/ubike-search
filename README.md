# YouBike 搜尋系統

###### 此搜尋系統提供查詢臺北YouBike、Youbike2.0、新北YouBike、桃園YouBike各站點剩餘車數


## 目錄
[專題說明](https://github.com/yu-chen11/ubike-search/blob/main/README.md#%E5%B0%88%E9%A1%8C%E8%AA%AA%E6%98%8E)  
>[設計背景]()  
>[設計目的]()

[專題介紹](https://github.com/yu-chen11/ubike-search/blob/main/README.md#%E5%B0%88%E9%A1%8C%E4%BB%8B%E7%B4%B9)
>[使用說明]()       
>[應用技術]()       
>[素材]()

[程式碼]()      
>[Requirement]()        
>[def功能解釋]()


## 專題說明

### 設計背景

由課程作業 **桃園公共自行車即時服務資料** 發想，當時課程作業成果設計為輸出於consloe，且資料更是只有經過簡單分類，對使用者非常不便。  
因此想設計對使用者較為友善的介面，延伸出增加臺北市、新北市UBike資料API，可查詢各個站點剩餘車數以及連結Google Map查詢站點位置，並以視窗呈現內容。

### 設計目的
1. 改善使用者使用經驗
1. 設計友善使用者的介面
1. 圖像化站點車輛資訊
1. 簡化使用者操作

## 專題介紹

### 使用說明
![使用介面](img_readme/main.png)
1. 選擇查詢的地區
2. 選擇查詢的地點  
系統即會輸出總車位、剩餘車數、站點地區、站點代號、站點地址及上傳資料時間
3. 點擊查看地圖，至Google Map查看站點位置
4. 可點擊更新，更新數據
   
右側腳踏車圖案將會依剩餘車數比例改變顏色，剩餘多為綠色，依數量減少為黃、紅色。

### 應用技術
* requests：下載網頁api資料
* tkinter：設計GUI
* webbbrowser：開啟網頁
* webcrawlercx

### 素材
###### 資料API來源


[YouBike2.0臺北市公共自行車即時資訊](https://data.gov.tw/dataset/137993)  
[新北市公共自行車租賃系統(YouBike)](https://data.ntpc.gov.tw/datasets/71CD1490-A2DF-4198-BEF1-318479775E8A)  
[YouBike臺北市公共自行車即時資訊](https://data.gov.tw/dataset/128706)  
[桃園公共自行車即時服務資料](https://data.tycg.gov.tw/opendata/datalist/datasetMeta?oid=5ca2bfc7-9ace-4719-88ae-4034b9a5a55c)

## 程式碼

### Requirement

```py
import random
import tkinter
from tkinter import *
import requests
import webbrowser
```
#### 資料日期分隔
```py
def dateTrans(date):
    return date[0:4] + '-' + date[4:6] + '-' + date[6:8] + ' ' + date[8:10] + ':' + date[10:12] + ':' + date[12:14]
```
#### 抓取資料並儲存於List
```py
def getTP2():
    r = requests.get(url[1])
    tp2_Data = r.json()
    sna = []
    for d in range (len(tp2_Data)):
        sna.append(tp2_Data[d]['sna'])
        temp=[]
        temp.append(tp2_Data[d]['sno'])
        temp.append(tp2_Data[d]['sna'])
        temp.append(tp2_Data[d]['tot'])
        temp.append(tp2_Data[d]['sbi'])
        temp.append(tp2_Data[d]['sarea'])
        temp.append(tp2_Data[d]['mday'])
        temp.append(tp2_Data[d]['lat'])
        temp.append(tp2_Data[d]['lng'])
        temp.append(tp2_Data[d]['ar'])
        data.append(temp)
    opt2["values"] = sna
```
#### 選擇大地區後更新地點List,設定輸出初始值
```py
def opt1_select(event):
    global map_url
    global rate
    index = opt1.current()
    data.clear()
    if (index == 1):
        getTP2()
    elif (index ==2):
        getTP()
    elif (index ==3):
        getNTP()
    elif (index ==4):
        getTao()
    opt2.current(0)
    code_t.configure(text=data[0][0])
    bike.configure(text=data[0][2])
    emp.configure(text=data[0][3])
    loc_t.configure(text=data[0][4])
    time_t.configure(text=data[0][5])
    addr_t.configure(text=data[0][8])
    rate = int(data[0][3])/int(data[0][2])
    chg()
    map_url = 'https://www.google.com.tw/maps/search/'+str(data[0][6])+','+str(data[0][7])
```
#### 選擇地點後，將資料存於資料List
```py
def opt2_select(event):
    global map_url
    global rate
    index = opt2.current()
    code_t.configure(text=data[index][0])
    bike.configure(text=data[index][2])
    emp.configure(text=data[index][3])
    loc_t.configure(text=data[index][4])
    time_t.configure(text=data[index][5])
    map_url = 'https://www.google.com.tw/maps/search/'+str(data[index][6])+','+str(data[index][7])
    addr_t.configure(text=data[index][8])
    rate = int(data[index][3])/int(data[index][2])
    chg()
```
連結def與選單
```py
opt2.bind('<<ComboboxSelected>>', opt2_select)
```
更新按鈕功能，重新抓取API資料
```py
def update():
    global data
    global map_url
    data.clear()
    index1 = opt1.current()
    if (index1 == 1):
        getTP2()
    elif (index1 ==2):
        getTP()
    elif (index1 ==3):
        getNTP()
    elif (index1 ==4):
        getTao()
    index2 = opt2.current()
    code_t.configure(text=data[index2][0])
    bike.configure(text=data[index2][2])
    emp.configure(text=data[index2][3])
    loc_t.configure(text=data[index2][4])
    time_t.configure(text=data[index2][5])
    map_url = 'https://www.google.com.tw/maps/search/'+str(data[index2][6])+','+str(data[index2][7])
    addr_t.configure(text=data[index2][8])
```
#### 開啟Google Map功能
```py
def map_clicked():
    webbrowser.open(map_url)
map = tk.Button(canvas,text="查看地圖",bg='gray',fg='white',command=map_clicked)
map.place(x=330,y=230,width=260,height=20)
```