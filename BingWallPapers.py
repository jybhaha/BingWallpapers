# -*- coding: UTF-8 -*-
import requests
import os
import datetime
import win32gui,win32con,win32api


dt = datetime.datetime.now()
cd = str(dt.year)+'0'+str(dt.month)+str(dt.day)
os.makedirs('Bing',exist_ok=True)
url = 'http://www.bing.com/'
soup = requests.get(url)
p=13+soup.text.find("g_img=")

image_url=''
while soup.text[p]!="'" and soup.text[p]!='"':
	image_url=image_url+soup.text[p]
	p=p+1

res = requests.get(image_url)


with open(os.path.join('Bing',cd+'.bmp'),'wb') as file:
    file.write(res.content)

#更换壁纸
print(os.getcwd()+'\Bing'+chr(92)+cd+'.bmp" ')
k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
j = win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "2") #2拉伸适应桌面,0桌面居中
l = win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
n = win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,os.getcwd()+'.\Bing'+chr(92)+cd+'.bmp', 1+2)