#从微软bing网站下载壁纸并修改本地壁纸
----------
2016-09-12更新
今天发现windows聚焦壁纸更好看，所以就想把这个壁纸也扒下来，放在一个文件夹内，然后幻灯片放映。

查阅了资料。这些图片都放在：

C:\用户\当前电脑登录的账户\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets

目录下。

只要使用python，移动文件，加上'.jpg'就可以了。

其中：
从Bing首页扒下来的壁纸用'.bmp'后缀名，聚焦壁纸用'.jpg'后缀名。

要注意，每次copy聚焦壁纸时，要把以前的jpg壁纸删除。


---------

某日，安装完win10后发现，自带的壁纸真漂亮。

去bing网站搜索了一下，发现bing网站页面壁纸也挺好看。

于是，萌生了将bing网站壁纸拔下来的冲动。

由于好久不动爬虫了，花了一下午的时间才把这个小程序写完。

----------
**测试环境:**
 - win10
 - python3.5.2

**必须的python组件**
 - [requests][1]
 - win32Api [download][2]

----------
python主要代码：
```
# -*- coding: UTF-8 -*-
import requests
import os
import datetime
import win32gui,win32con,win32api
import shutil  #文件复制


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

if __name__ == '__main__':
	downloadWallpapers()
	sourceDir = 'c:\\Users\\jiao\\AppData\\Local\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\Assets'
	targetDir = 'f:\\MyProject\\Interest\\BingWallPapersJioa\\Bing'
	moveFocusToWallpapersDIR(sourceDir, targetDir)
	changeName(targetDir)
```

 


  [1]: http://cn.python-requests.org/zh_CN/latest/
  [2]: https://sourceforge.net/projects/pywin32/files/pywin32/