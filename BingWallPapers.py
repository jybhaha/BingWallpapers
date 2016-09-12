# -*- coding: UTF-8 -*-
import requests
import os
import datetime
import win32gui,win32con,win32api
import shutil  #文件复制
import re
from PIL import Image


def downloadWallpapers():
	dt = datetime.datetime.now()
	cd = str(dt.year) + '0' + str(dt.month) + str(dt.day)
	os.makedirs('Bing', exist_ok=True)
	url = 'http://www.bing.com/'
	soup = requests.get(url)
	p = 13 + soup.text.find("g_img=")

	image_url = ''
	while soup.text[p] != "'" and soup.text[p] != '"':
		image_url = image_url + soup.text[p]
		p = p + 1

	res = requests.get(image_url)

	with open(os.path.join('Bing', cd + '.bmp'), 'wb') as file:
		file.write(res.content)


def changeWallPapers():
	# 更换壁纸
	k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
	j = win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "2")  # 2拉伸适应桌面,0桌面居中
	l = win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
	n = win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, os.getcwd() + '.\Bing' + chr(92) + cd + '.bmp',
									  1 + 2)

def moveFocusToWallpapersDIR(sourceDir, targetDir):
	for files in os.listdir(sourceDir):
		sourceFile = os.path.join(sourceDir, files)
		if os.path.getsize(sourceFile) > 300000:
			shutil.copy(sourceFile, targetDir)

def changeName(targetDir):
	#重命名之前先保存，防止出错
	for files in os.listdir(targetDir):
		targetFile = os.path.join(targetDir, files)
		if os.path.splitext(targetFile)[-1] == '.jpg':
			os.remove(targetFile)

	for files in os.listdir(targetDir):
		targetFile = os.path.join(targetDir, files)
		if os.path.splitext(targetFile)[-1] == '.bmp':
			continue
		else:
			os.rename(targetFile, targetFile + '.jpg')


def deleteWrongPicture(targetDir):#find the wrong Wallpapers
	for files in os.listdir(targetDir):
		targetFile = os.path.join(targetDir, files)
		img = Image.open(targetFile)
		patern=re.compile(r"\d+")
		#删除横板壁纸，不然桌面拉伸太难看
		if patern.findall(str(img.size))[0] < patern.findall(str(img.size))[1]:
			img.close()#先关闭文件，不然下面删除失败
			os.remove(targetFile)

if __name__ == '__main__':
	downloadWallpapers()
	sourceDir = 'c:\\Users\\jiao\\AppData\\Local\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\Assets'
	targetDir = 'f:\\MyProject\\Interest\\BingWallPapersJioa\\Bing'
	moveFocusToWallpapersDIR(sourceDir, targetDir)
	changeName(targetDir)
	deleteWrongPicture(targetDir)





