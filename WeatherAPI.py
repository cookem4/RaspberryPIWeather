import requests
import json
import tkinter as tk
import io
import base64
import time
import pytz
from datetime import datetime
from urllib.request import urlopen
#response = requests.get("http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID=dd7993542a0c3122f0b36bc94a648bf5")


def moreInfoCallBack():
    global moreInfo
    if(moreInfo):
        moreInfo=False
        widgetlist[1].place(x=250,y=-20)
        widgetlist[2].config(text="More Info")
        widgetlist[2].place(x=220, y=320)
        widgetlist[2].config(width=320)
        widgetlist[2].config(height=15)
        widgetlist[2].pack()
        widgetlist[0].config(font=("Ariel", 40))
        widgetlist[0].config(text=data["name"] + "\n" +  data["weather"][0]["main"] + "\n" +  str("{:.1f}".format(data["main"]["temp"]-273.15) + "°"))
    else:
        moreInfo=True
        widgetlist[2].config(text="Less Info")
        widgetlist[2].place(x=220, y=320)
        widgetlist[2].config(width=320)
        widgetlist[2].config(height=15)
        widgetlist[2].config(font=("Ariel", 20))
        widgetlist[2].pack()
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

        widgetlist[0].config(font=("Ariel", 26))
        widgetlist[0].config(text="Humidity: " + str(data["main"]["humidity"]) + "%"+"\n" + "Wind Speed: " + str("{:.1f}".format(data["wind"]["speed"] * 3.6)) + " km/h" + "\n" + "Cloud Coverage: " + str(data["clouds"]["all"]) + "%" + "\n" + "Sunrise: " + sunrisetime  + "\n" + "Sunset: " + sunsettime )
        widgetlist[1].place(x=1000, y=-1000)


def mainScreen(root):
    response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Hamilton&APPID=dd7993542a0c3122f0b36bc94a648bf5")
    global data
    data = response.json()
    print(data)
    image_url = "http://openweathermap.org/img/w/" + data["weather"][0]["icon"] + ".png"
    image_byt = urlopen(image_url).read()
    image_b64 = base64.encodestring(image_byt)
    
    root.geometry("480x320")
    widgetlist.append(tk.Label(root, text = data["name"] + "\n" +  data["weather"][0]["main"] + "\n" +  str("{:.1f}".format(data["main"]["temp"]-273.15) + "°"),justify="left", anchor='w',width=320))
    widgetlist[0].config(font=("Ariel", 40))
    photo=tk.PhotoImage(data=image_b64)
    photo = photo.zoom(5,5)
    widgetlist[0].pack()
    widgetlist.append(tk.Label(root, image=photo))
    widgetlist[1].image = photo
    widgetlist[1].place(x=250,y=-20)
    widgetlist.append(tk.Button(root, text="More Info", command = moreInfoCallBack, height=15, width=320))
    widgetlist[2].place(x=220, y=320)
    widgetlist[2].config(font=("Ariel", 20))
    widgetlist[2].pack()
    root.mainloop()
data = None
moreInfo = False
widgetlist = [] 
root = tk.Tk()
mainScreen(root)
