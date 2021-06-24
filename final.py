import random
import tkinter as tk
from tkinter import PhotoImage
from tkinter.constants import NS, NSEW
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk
import requests
import webbrowser

data=[]
rate = 0

url = ['', #NONE
    'https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json', #Taipei 2.0
    'https://tcgbusfs.blob.core.windows.net/blobyoubike/YouBikeTP.json', #Taipei  
    'https://data.ntpc.gov.tw/api/datasets/71CD1490-A2DF-4198-BEF1-318479775E8A/json?page=0&size=1000', #New taipei city
    'http://data.tycg.gov.tw/api/v1/rest/datastore/a1b4714b-3b75-4ff8-a8f2-cc377e4eaa0f?format=json'] #Taoyuan

map_url =  'https://www.google.com.tw/maps'


window = tk.Tk()
window.title("YouBike查詢系統")
window.geometry("640x300")
window.configure(bg="white")

canvas = tk.Canvas(window,bg="white",width=640,height=300,bd=0,highlightthickness=0)
canvas.pack()


img = PhotoImage(file='img/logo.png')
pic = tk.Label(canvas,image=img)
pic.place(x=60,y=20,width=100,height=40)

ti = tk.Label(canvas,text="YouBike 查詢系統",bg='white', font=('Arial', 24))
ti.place(x=160,y=20,width=320,height=40)

l0c = tk.Label(canvas,text = "要查尋的地區",bg="white",anchor=tk.W)
l0c.place(x=50,y=70,width=200,height=20)

opt1 = ttk.Combobox(window, values=[
                                    '請選擇地區',
                                    '臺北YouBike 2.0',
                                    '臺北YouBike',
                                    '新北YouBike',
                                    '桃園YouBike'])
opt1.pack(pady=10)
opt1.current(0)
opt1.place(x=50,y=90,width=200,height=20)

def dateTrans(date):
    return date[0:4] + '-' + date[4:6] + '-' + date[6:8] + ' ' + date[8:10] + ':' + date[10:12] + ':' + date[12:14]

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

def getTP():
    r = requests.get(url[2])
    tp_Data = r.json()
    tp = tp_Data["retVal"]
    sna = []
    for d in tp.values():
        sna.append(d['sna'])
        temp=[]
        temp.append(d['sno'])
        temp.append(d['sna'])
        temp.append(d['tot'])
        temp.append(d['sbi'])
        temp.append(d['sarea'])
        temp.append(dateTrans(d['mday']))
        temp.append(d['lat'])
        temp.append(d['lng'])
        temp.append(d['ar'])
        data.append(temp)
    opt2["values"] = sna

def getNTP():
    r = requests.get(url[3])
    ntp_Data = r.json()
    sna = []
    for d in range (len(ntp_Data)):
        sna.append(ntp_Data[d]['sna'])
        temp=[]
        temp.append(ntp_Data[d]['sno'])
        temp.append(ntp_Data[d]['sna'])
        temp.append(ntp_Data[d]['tot'])
        temp.append(ntp_Data[d]['sbi'])
        temp.append(ntp_Data[d]['sarea'])
        temp.append(dateTrans(ntp_Data[d]['mday']))
        temp.append(ntp_Data[d]['lat'])
        temp.append(ntp_Data[d]['lng'])
        temp.append(ntp_Data[d]['ar'])
        data.append(temp)
    opt2["values"] = sna

def getTao():
    r = requests.get(url[4])
    tao_Data = r.json()
    tao = tao_Data["result"]["records"]
    sna = []
    for d in range(len(tao)):
        sna.append(tao[d]['sna'])
        temp=[]
        temp.append(tao[d]['sno'])
        temp.append(tao[d]['sna'])
        temp.append(tao[d]['tot'])
        temp.append(tao[d]['sbi'])
        temp.append(tao[d]['sarea'])
        temp.append(dateTrans(tao[d]['mday']))
        temp.append(tao[d]['lat'])
        temp.append(tao[d]['lng'])
        temp.append(tao[d]['ar'])
        data.append(temp)
    opt2["values"] = sna

#選擇大地區系統後，執行get，並設定空格值為default
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

opt1.bind('<<ComboboxSelected>>', opt1_select)

site = tk.Label(canvas,text = "要查尋的地點",bg="white",anchor=tk.W)
site.place(x=50,y=120,width=200,height=20)

opt2 = ttk.Combobox(window, values=[
                                    '請選擇地點'])
opt2.pack(pady=10)
opt2.place(x=50,y=140,width=200,height=20)
opt2.current(0)

#地點選擇後，將資料填入空格
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
    print(rate)
    
    #print(data[index][6])
    #print(data[index][7])
opt2.bind('<<ComboboxSelected>>', opt2_select)

bycicle = PhotoImage(file='img/bycicle.png')
red = PhotoImage(file='img/red_bike.png')
yellow = PhotoImage(file='img/yellow_bike.png')
green = PhotoImage(file='img/green_bike.png')
b_pic = tk.Label(canvas,image=bycicle)
b_pic.place(x=480,y=70,width=100,height=100)
def chg():
    if(rate>=0.7):
        b_pic.configure(image=green)
    elif(rate>=0.4):
        b_pic.configure(image=yellow)
    else:
        b_pic.configure(image=red)

#車位標籤
bike_num = tk.Label(canvas,text="車位",bg='white')
bike_num.place(x=340,y=70,width=90,height=20)

bike = tk.Label(canvas,text="",bg='gray')
bike.place(x=340,y=90,width=90,height=20)
#車數標籤
emp_num = tk.Label(canvas,text="車數",bg='white')
emp_num.place(x=340,y=110,width=90,height=20)

emp = tk.Label(canvas,text="",bg='gray')
emp.place(x=340,y=130,width=90,height=20)

#時間標籤
time_title = tk.Label(canvas,text="時間",bg='white')
time_title.place(x=50,y=170,width=260,height=20)

time_t = tk.Label(canvas,text="",bg='gray')
time_t.place(x=50,y=190,width=260,height=20)
#地區標籤
loc_title = tk.Label(canvas,text="地區",bg='white')
loc_title.place(x=330,y=170,width=120,height=20)

loc_t = tk.Label(canvas,text="",bg='gray')
loc_t.place(x=330,y=190,width=120,height=20)
#代號標籤
code_title = tk.Label(canvas,text="代號",bg='white')
code_title.place(x=470,y=170,width=120,height=20)

code_t = tk.Label(canvas,text="",bg='gray')
code_t.place(x=470,y=190,width=120,height=20)
#地址標籤
addr_title = tk.Label(canvas,text="地址",bg='white')
addr_title.place(x=50,y=210,width=260,height=20)

addr_t = tk.Label(canvas,text="",bg='gray')
addr_t.place(x=50,y=230,width=260,height=20)

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

#更新按鈕
refresh = tk.Button(canvas,text="更新",bg='gray',fg='white',command=update)
refresh.place(x=260,y=90,width=40,height=20)

def map_clicked():
    print(map_url)
    webbrowser.open(map_url)

#查看地圖按鈕
map = tk.Button(canvas,text="查看地圖",bg='gray',fg='white',command=map_clicked)
map.place(x=330,y=230,width=260,height=20)

window.mainloop()