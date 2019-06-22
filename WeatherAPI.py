import requests
import json
import tkinter as tk
import io
import base64
import time
import pytz
import shutil
from datetime import datetime
from urllib.request import urlopen
from PIL import ImageTk, Image
import threading
from tkinter import font
import matplotlib
from pandas import DataFrame
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
#response = requests.get("http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID=dd7993542a0c3122f0b36bc94a648bf5")
#Vane Key: dd7993542a0c3122f0b36bc94a648bf5
#Vane Api Call: https://sat.owm.io/sql/8/71/93?select=b4,b3,b2&order=best&appid=dd7993542a0c3122f0b36bc94a648bf5
#Planet.com API key: 19a82d078e5542ff9d6188721d6e95bd

def plot():
    global forecast
    if(not(forecast)):
        forecast = True
        widgetlist[0].place(x=1000, y=1000)
        widgetlist[1].place(x=1000, y=1000)
        widgetlist[2].place(x=1000, y=1000)
        widgetlist[3].place(x=1000, y=1000)
        widgetlist[6].config(text="Back")
        widgetlist[6].place(x=0, y=270)
        widgetlist[6].config(width=30)

        #Display plot
        global forecastData
        global forecastTime
        Data1 = { 'Temperature (C)': forecastData}
        df1 = DataFrame(Data1, columns = ['Time', 'Temperature (C)'], index = forecastTime)
        df1.index.name="Number of Hours in Future"
        f = plt.Figure(figsize=(4.75,2.7), dpi=100)
        ax1 = f.add_subplot(111)
        line=FigureCanvasTkAgg(f, root)
        plotwidget = line.get_tk_widget()
        plotwidget.place(x=0, y=0)
        widgetlist.append(plotwidget)
        df1.plot(kind='line', ax=ax1, legend = False, color='r', marker='o', fontsize=10)
        ax1.set_title('Temperature vs Future Time')
        ax1.set(xlabel="Hours In Future", ylabel="Temperature (C)")
    else:
        forecast = False
        widgetlist[7].destroy()
        del widgetlist[-1]
        widgetlist[1].place(x=215,y=0)
        widgetlist[2].config(text="More Info")
        widgetlist[1].configure(bg="#51b4f0")
        widgetlist[2].place(x=0, y=270)
        widgetlist[2].config(width=9)
        widgetlist[2].config(height=1)
        widgetlist[0].place(x=0, y=0)
        widgetlist[0].config(font=("Arial", 45))
        widgetlist[0].config(text=data["name"] + "\n" +  data["weather"][0]["main"] + "\n" +  str("{:.1f}".format(data["main"]["temp"]-273.15) + "°"))
        widgetlist[3].config(text="Map")
        widgetlist[3].place(x=162, y=270)
        widgetlist[3].config(width=9)
        widgetlist[3].config(font=("Arial", 20))
        widgetlist[6].config(text="Forecast")
        widgetlist[6].config(width=9)
        widgetlist[6].place(x=320, y=270)


def  showWeatherMap():
    global weatherMap
    if(not(weatherMap)):
        weatherMap = True
        widgetlist[1].place(x=1000, y=1000)
        widgetlist[3].config(text="Back")
        widgetlist[3].config(width=30)
        widgetlist[3].place(x=0, y=270)
        widgetlist[4].place(x=0,y=0)
        widgetlist[2].place(x=1000, y=1000)
        widgetlist[5].place(x=275, y=0)
        widgetlist[6].place(x=1000, y=1000)

    else:
        weatherMap=False
        widgetlist[5].place(x=1000, y=1000)
        widgetlist[4].place(x=1000,y=1000)
        widgetlist[1].place(x=215,y=0)
        widgetlist[2].config(width=9)
        widgetlist[3].config(width=9)
        widgetlist[2].config(text="More Info")
        widgetlist[1].configure(bg="#51b4f0")
        widgetlist[2].place(x=0, y=270)
        widgetlist[0].config(font=("Arial", 45))
        widgetlist[0].config(text=data["name"] + "\n" +  data["weather"][0]["main"] + "\n" +  str("{:.1f}".format(data["main"]["temp"]-273.15) + "°"))
        widgetlist[3].config(text="Map")
        widgetlist[6].config(width=9)
        widgetlist[3].place(x=162, y=270)
        widgetlist[6].place(x=320, y=270)
        widgetlist[6].config(text="Forecast")

def moreInfoCallBack():
    global moreInfo
    if(moreInfo):
        moreInfo=False
        widgetlist[1].place(x=215,y=0)
        widgetlist[1].configure(bg="#51b4f0")
        widgetlist[2].config(text="More Info")
        widgetlist[2].place(x=0, y=270)
        widgetlist[0].config(font=("Arial", 45))
        widgetlist[0].config(text=data["name"] + "\n" +  data["weather"][0]["main"] + "\n" +  str("{:.1f}".format(data["main"]["temp"]-273.15) + "°"))
        widgetlist[3].place(x=162, y=270)
        widgetlist[3].config(font=("Arial", 20))
        widgetlist[6].place(x=320, y=270)
        widgetlist[2].config(width=9)
        widgetlist[3].config(width=9)
        widgetlist[6].config(width=9)
        widgetlist[6].config(text="Forecast")
    else:
        moreInfo=True
        widgetlist[2].config(text="Less Info")
        widgetlist[2].place(x=0, y=270)
        widgetlist[2].config(width=30)
        widgetlist[6].place(x=1000, y=1000)
        widgetlist[2].config(height=1)
        widgetlist[2].config(font=("Arial",20))
        sunrisetime = time.strftime('%Y-%m-%d %H:%M', time.localtime(data["sys"]["sunrise"]))
        sunsettime = time.strftime('%Y-%m-%d %H:%M', time.localtime(data["sys"]["sunset"]))
        gmt = pytz.timezone('UTC')
        eastern = pytz.timezone('EST')
        fmt = "%Y-%m-%d %H:%M"
        date = datetime.strptime(sunrisetime, fmt)
        dategmt = gmt.localize(date)
        dateest = dategmt.astimezone(eastern)
        sunrisetime = dateest.strftime("%H:%M")

        date = datetime.strptime(sunsettime, fmt)
        dategmt = gmt.localize(date)
        dateest = dategmt.astimezone(eastern)
        sunsettime = dateest.strftime("%H:%M")

        widgetlist[0].config(font=("Arial", 31))
        widgetlist[0].config(text="Humidity: " + str(data["main"]["humidity"]) + "%"+"\n" + "Wind Speed: " + str("{:.1f}".format(data["wind"]["speed"] * 3.6)) + " km/h" + "\n" + "Cloud Coverage: " + str(data["clouds"]["all"]) + "%" + "\n" + "Sunrise: " + sunrisetime  + "\n" + "Sunset: " + sunsettime )
        widgetlist[1].place(x=1000, y=-1000)
        widgetlist[3].place(x=1000, y=210)
        widgetlist[3].config(font=("Arial", 20))




def mainScreen(root):

    global url3
    response = requests.get(url3)
    global data
    data = response.json()

    image_url = "http://openweathermap.org/img/w/" + data["weather"][0]["icon"] + ".png"
    image_byt = urlopen(image_url).read()
    image_b64 = base64.encodestring(image_byt)
    
    root.geometry("480x320-0-25")
    widgetlist.append(tk.Label(root, text = data["name"] + "\n" +  data["weather"][0]["main"] + "\n" +  str("{:.1f}".format(data["main"]["temp"]-273.15) + "°"),justify="left", anchor='w',width=320))
    widgetlist[0].config(font=("Arial", 45))
    widgetlist[0].place(x=0,y=0)
    widgetlist[0].configure(bg="#51b4f0")
    photo=tk.PhotoImage(data=image_b64)
    photo = photo.zoom(5,5)
    widgetlist.append(tk.Label(root, image=photo))
    widgetlist[1].image = photo
    widgetlist[1].place(x=215,y=0)
    widgetlist[1].configure(bg="#51b4f0")
    widgetlist.append(tk.Button(root, text="More Info", command = moreInfoCallBack, height=1, width=9))
    widgetlist[2].place(x=0, y=270)
    widgetlist[2].config(font=("Arial", 20))
    widgetlist[2].configure(bg="#51b4f0")

    widgetlist.append(tk.Button(root, text="Map", command = showWeatherMap, height=1, width=9))
    widgetlist[3].place(x=162, y=270)
    widgetlist[3].config(font=("Arial", 20))
    widgetlist[3].configure(bg="#51b4f0")

    global url1    
    response = requests.get(url1, stream=True)
    with open("22.png", 'wb') as f:
            shutil.copyfileobj(response.raw,f)
    del response
    im = Image.open("22.png")
    im.save("satMap.png")
    
    global url2   
    response = requests.get(url2, stream=True)
    with open("22.png", 'wb') as f:
           shutil.copyfileobj(response.raw,f)
    del response
    im = Image.open("22.png")
    im.save("weatherLayer.png")


    bg = Image.open("satMap.png")
    fg = Image.open("weatherLayer.png")
    bg.paste(fg, (0,0), fg)
    bg.save("merged.png")


    weatherLayer=ImageTk.PhotoImage(Image.open("merged.png"))
    widgetlist.append(tk.Label(root, image=weatherLayer))
    widgetlist[4].image=weatherLayer
    widgetlist[4].place(x=1000,y=1000) 
   
    response = requests.get("http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID=dd7993542a0c3122f0b36bc94a648bf5")
    data2 = response.json()
    timeStr = data2["list"][7]["dt"]
    temp = str("{:.1f}".format(data2["list"][7]["main"]["temp"]-273.15) + "°")
    forecast = data2["list"][7]["weather"][0]["main"]
    timeStrFormatted = time.strftime('%Y-%m-%d %H:%M', time.localtime(timeStr))

    gmt = pytz.timezone('UTC')
    eastern = pytz.timezone('EST')
    fmt = "%Y-%m-%d %H:%M"
    date = datetime.strptime(timeStrFormatted, fmt)
    dategmt = gmt.localize(date)
    dateest = dategmt.astimezone(eastern)
    forecastTime1 = dateest.strftime("%m-%d %H:%M")


    widgetlist.append(tk.Label(root, text="In 24 hours:" + "\n" + forecastTime1 + "\n" + forecast + "\n" + temp , justify="right", anchor='w',width=100))
    widgetlist[5].place(x=1000, y=1000)
    widgetlist[5].config(font=("Piboto", 25))
    widgetlist[5].configure(bg="#51b4f0")
    global forecastData
    global forecastTime
    for i in range(8):
        forecastData.append(float(data2["list"][i]["main"]["temp"])-273.15)
        forecastTime.append(3*(i+1))

    widgetlist.append(tk.Button(root, text="Forecast", command = plot, height=1, width=9))
    widgetlist[6].place(x=320, y=270)
    widgetlist[6].configure(font=("Arial", 20))
    widgetlist[6].configure(bg="#51b4f0")

    root.mainloop()
def updateThread():
    global widgetlist
    global url1
    global url2
    global url3
    global url4
    global data
    i = 0
    while(True):
        i = i+1
        if(len(widgetlist)>4):
            print(i)
            response = requests.get(url3)
            data = response.json()
            image_url = "http://openweathermap.org/img/w/" + data["weather"][0]["icon"] + ".png"
            image_byt = urlopen(image_url).read()
            image_b64 = base64.encodestring(image_byt)

            widgetlist[0].config(text = data["name"] + "\n" +  data["weather"][0]["main"] + "\n" +  str("{:.1f}".format(data["main"]["temp"]-273.15) + "°"))

            photo=tk.PhotoImage(data=image_b64)
            photo = photo.zoom(5,5)
            widgetlist[1].image = photo

            
            response = requests.get(url1, stream=True)
            with open("22.png", 'wb') as f:
                shutil.copyfileobj(response.raw,f)
            del response
            im = Image.open("22.png")
            im.save("satMap.png")
       
            response = requests.get(url2, stream=True)
            with open("22.png", 'wb') as f:
                shutil.copyfileobj(response.raw,f)
            del response
            im = Image.open("22.png")
            im.save("weatherLayer.png")


            bg = Image.open("satMap.png")
            fg = Image.open("weatherLayer.png")
            bg.paste(fg, (0,0), fg)
            bg.save("merged.png")

            weatherLayer=ImageTk.PhotoImage(Image.open("merged.png"))
            widgetlist[4].image=weatherLayer

            response = requests.get("http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID=dd7993542a0c3122f0b36bc94a648bf5")
            data2 = response.json()
            timeStr = data2["list"][7]["dt"]
            temp = str("{:.1f}".format(data2["list"][7]["main"]["temp"]-273.15) + "°")
            forecast = data2["list"][7]["weather"][0]["main"]
            timeStrFormatted = time.strftime('%Y-%m-%d %H:%M', time.localtime(timeStr))

            gmt = pytz.timezone('UTC')
            eastern = pytz.timezone('EST')
            fmt = "%Y-%m-%d %H:%M"
            date = datetime.strptime(timeStrFormatted, fmt)
            dategmt = gmt.localize(date)
            dateest = dategmt.astimezone(eastern)
            forecastTime = dateest.strftime("%m-%d %H:%M")


            widgetlist[5].config(text="In 24 hours:" + "\n" + forecastTime + "\n" + forecast + "\n" + temp , justify="right", anchor='w')

            global forecastData
            global forecastTime
            forecastData = []
            forecastTime = []
            for i in range(8):
                forecastData.append(float(data2["list"][i]["main"]["temp"])-273.15)
                print(forecastTime)
                forecastTime.append(3*(i+1))

        time.sleep(120)
data = None
moreInfo = False
weatherMap=False
forecast = False
forecastData= []
forecastTime = []
#Testing other API call
url1 = "https://sat.owm.io/sql/6/17/23?select=b4,b3,b2&order=best&appid=dd7993542a0c3122f0b36bc94a648bf5"
url2 = "http://tile.openweathermap.org/map/precipitation_new/6/17/23.png?appid=dd7993542a0c3122f0b36bc94a648bf5"
url3 = "http://api.openweathermap.org/data/2.5/weather?lat=43.2665&lon=-79.9569&APPID=dd7993542a0c3122f0b36bc94a648bf5"
url4 = "http://tile.openweathermap.org/map/clouds_new/6/17/23.png?appid=dd7993542a0c3122f0b36bc94a648bf5"
widgetlist = [] 
root = tk.Tk()
root.configure(bg="#51b4f0")
myThread = threading.Thread(target=updateThread, args = ())
myThread.start()
mainScreen(root)
