"""
package:
    获取放置于里面的静态文件
args:
    filename:文件名
"""

def where_data(filename):
    import os
    basepath = os.path.abspath(__file__)
    folder = os.path.dirname(basepath)
    data_path = os.path.join(folder, filename)
    return data_path
import pygame.mixer
pygame.mixer.init()
from tkinter.ttk import Notebook
from tkinter.simpledialog import *
from tkinter import *
from tkinter import messagebox
import os, time
from tkinter.scrolledtext import ScrolledText as Text

note_it=0
ziti = 'fixed'
#classes
if 1:
	class Imgbutton(object):
		def __init__(self, root, width=100, img="", text="", command="", **arg):
			import tkinter as tk
			import PIL.Image
			import PIL.ImageTk
			self.width = width
			if type(width) == type((1, 2, 3, 4)):
				self.img = PIL.ImageTk.PhotoImage(
					PIL.Image.open(where_data(img)).resize(
						width,
						PIL.Image.ANTIALIAS
					)
				)
			else:
				self.img = PIL.ImageTk.PhotoImage(
					PIL.Image.open(where_data(img)).resize(
						(width, width),
						PIL.Image.ANTIALIAS
					)
				)
			self.command = command
			self.Frame = tk.Frame(root)
			self.Label = tk.Label(self.Frame, text=text, image=self.img, compound="top", **arg)

			self.Label.pack(fill="both", expand=True)

			self.Label.bind("<Button-1>", self.click)

		# def command(self,*event):
		#     self.com()
		def click(self, *w):
			self.command()

		def configure(self, **arg):
			self.Label.configure(**arg)

		def pack(self, *k, **K):
			self.Frame.pack(*k, **K)

		def bind(self, k, command):
			self.Label.bind(k, command)

		def reload(self, img):
			import tkinter as tk
			import PIL.Image
			import PIL.ImageTk
			width = self.width
			self.img = PIL.ImageTk.PhotoImage(
				PIL.Image.open(where_data(img)).resize(
					(width, width),
					PIL.Image.ANTIALIAS
				)
			)
			self.Label.configure(image=self.img)

	class Beautiwindow(Tk):
		def geometry(self, ww,wh):
			if 1:
				self.update()
				self.attributes("-alpha", 0.01)
				self.update()
				self.sw = self.winfo_screenwidth()  # 严子昱水印
				# 得到屏幕宽度#严子昱水印
				self.sh = self.winfo_screenheight()  # 严子昱水印
				# 得到屏幕高度#严子昱水印
				self.ww = ww # 严子昱水印
				self.wh = wh # 严子昱水印
				# 窗口宽高为100#严子昱水印
				self.x = (self.sw - self.ww) / 2  # 严子昱水印
				self.y = (self.sh - self.wh) / 2  # 严子昱水印
				super().geometry("%dx%d+%d+%d" % (self.ww, self.wh, self.x, self.y))  # 严子昱水印
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.attributes('-alpha', 0.01)
			self.update()
			# 初步
			if 1:
				if os.name == "nt":
					niubi = True
				else:
					niubi = False
				if niubi:
					self.attributes('-topmost', True)  # 严子昱水印
				if niubi:
					self.overrideredirect(True)  # 严子昱水印
			# 绑定部分业务逻辑及移动屏幕的逻辑
			if 1:
				self.update()
				self.attributes("-alpha", 1)
				self.protocol("WM_DELETE_WINDOW", self.DELETED_WINDOW)  # 严子昱水印
				self.bind('<Escape>', self.DELETED_WINDOW)
				self.update()
				self.sw = self.winfo_screenwidth()  # 严子昱水印
				# 得到屏幕宽度#严子昱水印
				self.sh = self.winfo_screenheight()  # 严子昱水印
				# 得到屏幕高度#严子昱水印
				self.ww = 800  # 严子昱水印
				self.wh = 500  # 严子昱水印
				# 窗口宽高为100#严子昱水印
				self.x = (self.sw - self.ww) / 2  # 严子昱水印
				self.y = (self.sh - self.wh) / 2  # 严子昱水印
				super().geometry("%dx%d+%d+%d" % (self.ww, self.wh, self.x, self.y))  # 严子昱水印

			# 复杂一些
			if 1:
				self.vt = Frame(self)
				self._title = Label(self.vt,text="Beautiful_TK")
				self.vt_x = Imgbutton(self.vt, 25, "img/xo.png", text="", command=self.DELETED_WINDOW)
				self.vt__ = Imgbutton(self.vt, 25, "img/-o.png", text="", command=self.i)
				# self.gi
				# vtT = Imgbutton(title, (550, 30), "img/title.gif", text="", command=nothing)
				# bind vt_x
				self.vt_x.bind("<Enter>", self.cx)
				self.vt_x.bind("<Leave>", self.lx)
				#
				self.vt__.bind("<Enter>", self.c_)
				self.vt__.bind("<Leave>", self.l_)
				# vtT.pack(fill=X, side=RIGHT)

				########
				# def aaaa(*w):
				# 	print_info()

				# vt_T = Imgbutton(title, (60, 30), "img/ico.png", text="", command=aaaa)
				self.vt_x.pack(side=RIGHT)
				self.vt__.pack(side=RIGHT)
				# vt_T.pack(side=LEFT)
				self._title.pack(fill=X, side=LEFT)

				self.vt.pack(side=TOP, fill=X)
				self.update()
			# 绑定移动逻辑
			if 1:
				self.vt.bind("<B1-Motion>", self._move_window)
				self.vt.bind("<ButtonRelease-1>", self._xiufu_move)
				self.vt.bind("<Button-1>", self._xiufu_move_2)
		# 开始制造
		# overs hack
		def i(self):
			self.attributes("-alpha", 0.01)
			self.attributes('-topmost', 0)
			self.overrideredirect(False)
			self.iconify()
			self.bind('<Map>', self.i_2)

		# self.iconbitmap("ico.ico")
		def i_2(self, event, *w):
			# root.withdraw()
			self.attributes('-topmost', True)

			# help(event)
			# init()

			self.overrideredirect(True)
			time.sleep(0.1)
			self.attributes("-alpha", 1)
			# time.sleep(0.01)
			self.unbind('<Map>')

		# root.deiconify()
		def nothing(self, *w):
			pass

		def cx(self, *w):
			# print("?")
			# pop()
			self.vt_x.reload("img/x-.png")

		def c_(self, *w):
			# print("?")
			self.vt__.reload("img/--.png")

		def lx(self, *w):

			self.vt_x.reload("img/xo.png")

		def l_(self, *w):
			# pop()
			self.vt__.reload("img/-o.png")

		def HIDDEN_WINDOW(self, *evnet):
			self.attributes('-alpha', 0.1)
			if os.name == "nt":
				niubi = True
			else:
				niubi = False
			# if niubi:
			# 	self.attributes('-topmost', False)  # 严子昱水印
			if niubi:
				self.overrideredirect(0)

			self.iconify()
			self.bind("<Enter>", self.SHOW_AGAIN)

		def SHOW_AGAIN(self, *event):
			# self.()
			self.overrideredirect(1)
			self.focus_get()
			self.unbind("<Enter>")
			self.attributes('-alpha', 1)

		def DELETED_WINDOW(self, *args, **kwargs):
			get = messagebox.askokcancel("", "确认退出吗？")  # 严子昱水印
			if get:  # 严子昱水印
				sys.exit()  # 严子昱水印

		def _move_window(self, *event):

			# print(event)
			# print(nx,ny)
			click_x, click_y = event[0].x_root, event[0].y_root
			# print(f"click x{click_x}|click y{click_y}-ex,ey={nx}{ny}")
			# tx=click_x-x
			# ty=click_y-y
			self.nx = click_x - self.tx
			self.ny = click_y - self.ty
			# x,y=nx,ny
			# print(nx,ny)
			super().geometry("%dx%d+%d+%d" % (self.ww, self.wh, self.nx, self.ny))

		def _xiufu_move(self, *event):
			# self.x, y, ww, wh, tx, ty
			try:
				self.x, self.y = self.nx, self.ny
			except:
				# print("err")
				pass

		def _xiufu_move_2(self, *event):

			click_x, click_y = event[0].x_root, event[0].y_root
			# print(f"click x{click_x}|click y{click_y}-ex,ey={nx}{ny}")
			self.tx = click_x - self.x
			self.ty = click_y - self.y

		def center(root):
			# root=tk.Tk()
			root.update()
			sw = root.winfo_screenwidth()
			sh = root.winfo_screenheight()
			ww = root.winfo_width()
			wh = root.winfo_height()
			x = (sw - ww) / 2
			y = (sh - wh) / 2
			root.geometry("%dx%d+%d+%d" % (ww, wh, x, y))

		def jitter(root, times=3):
			import time
			root.update()
			root.focus_get()
			root.attributes('-topmost', True)
			time.sleep(0.1)
			root.update()
			ww = root.winfo_width()
			wh = root.winfo_height()
			wx = root.x
			wy = root.y

			for x in range(times):
				for y in (1, 2, 3, 4):
					root.update()
					if y == 1: wx += 10
					if y == 2: wy += 10
					if y == 3: wx -= 10
					if y == 4: wy -= 10
					root.geometry("%dx%d+%d+%d" % (ww, wh, wx, wy))
					# print("%dx%d+%d+%d" % (ww, wh, wx, wy))
					time.sleep(0.05)
			# root.attributes('-topmost', False)
			return True

		def title(self,text=""):
			super().title(text)
			self._title.config(text=text)

	class Bgm(object):
		def __init__(self):
			self.playing = 1
			self.getting = 0
		def get(self,filename,a=0.7,times=-1):
			try:
				self.bgm=pygame.mixer.Sound(filename)
			except:
				print(filename)
			self.bgm.set_volume(a)
			self.bgm.play(times)
			self.volume=a
			self.playing = 1
			self.getting = 1

		def updata(self):
			self.bgm.set_volume(self.volume)

		def lower(self):
			self.volume -= 0.1
			if self.volume > 0:
				self.volume = 0
			self.updata()

		def upper(self):
			self.volume -= 0.1
			if self.volume > 0:
				self.volume = 0
			self.updata()

		def set_volume(self,num):
			self.volume = num
			self.updata()

		def stop(self):
			self.bgm.fadeout(1)
			self.playing = False

		def play(self):
			self.bgm.play()
			self.playing = True

	class Musicbtn(Frame):
		def __init__(self,obj,file,a=1,times=1,title=""):
			super().__init__(obj)
			self.music=Bgm()
			self.music.get(filename=file,a=a,times=times);self.music.stop()
			self.picture = ["img\music\pause.png","img\music\play.png"]
			self.non = 0
			if title==None:
				title=file
			self.btn = Imgbutton(self,width=60,text=title,img="img\music\pause.png",command=self.click)
			self.btn.pack()

		def click(self,*event):
			self.non = not self.non
			self.updata()

		def updata(self):
			if self.non:
				self.music.play()
			else:
				self.music.stop()
			self.btn.reload(self.picture[int(self.non)])
root = Beautiwindow()
# root.attributes("-alpha", 0.01)
bgm=Bgm()
note = Notebook(root)
data_cache = []
frame_cache = []
music_cache=[]
#menu(pop)
if 1:
	def pop_up(event):
		popmenu.post(event.x_root, event.y_root)
	popmenu = Menu(root,tearoff=0)
	root.bind('<Button-3>',pop_up)
	popmenu.add_command(label='退出',command=root.DELETED_WINDOW)


#静态方法
if 1:
	def insert_music_btn(obj,file,a:float=1,times:int=1,title=None):
		lb=Musicbtn(obj,file=file,a=float(a),times=int(times),title=title)
		insert_window(obj,lb)

	def insert_music(file,a=1):
		def set_loud():
			z=askinteger('设置背景音乐声音', "输入声音大小（100-0的整数）")/100
			if z>1:
				z=1
			elif z<1:
				z=0
			bgm.set_volume(z)
		bgm.get(file,a)
		popmenu.add_command(label='关闭背景音乐',command=bgm.stop)
		popmenu.add_command(label='播放背景音乐', command=bgm.play)
		popmenu.add_command(label='设置背景音乐声音', command=set_loud)

	def AC(z):
		for x in [f"h{x}" for x in range(1, 7)]:
			if z in x:
				return 1
		return 0

	def add_tag(obj):
		color=[x.split(" ") for x in '''#FFB6C1 LightPink 浅粉红
,#FFC0CB Pink 粉红
,#DC143C Crimson 深红/猩红
,#FFF0F5 LavenderBlush 淡紫红
,#DB7093 PaleVioletRed 弱紫罗兰红
,#FF69B4 HotPink 热情的粉红
,#FF1493 DeepPink 深粉红
,#C71585 MediumVioletRed 中紫罗兰红
,#DA70D6 Orchid 暗紫色/兰花紫
,#D8BFD8 Thistle 蓟色
,#DDA0DD Plum 洋李色/李子紫
,#EE82EE Violet 紫罗兰
,#FF00FF Magenta 洋红/玫瑰红
,#FF00FF Fuchsia 紫红/灯笼海棠
,#8B008B DarkMagenta 深洋红
,#800080 Purple 紫色
,#BA55D3 MediumOrchid 中兰花紫
,#9400D3 DarkViolet 暗紫罗兰
,#9932CC DarkOrchid 暗兰花紫
,#4B0082 Indigo 靛青/紫兰色
,#8A2BE2 BlueViolet 蓝紫罗兰
,#9370DB MediumPurple 中紫色
,#7B68EE MediumSlateBlue 中暗蓝色/中板岩蓝
,#6A5ACD SlateBlue 石蓝色/板岩蓝
,#483D8B DarkSlateBlue 暗灰蓝色/暗板岩蓝
,#E6E6FA Lavender 淡紫色/熏衣草淡紫
,#F8F8FF GhostWhite 幽灵白
,#0000FF Blue 纯蓝
,#0000CD MediumBlue 中蓝色
,#191970 MidnightBlue 午夜蓝
,#00008B DarkBlue 暗蓝色
,#000080 Navy 海军蓝
,#4169E1 RoyalBlue 皇家蓝/宝蓝
,#6495ED CornflowerBlue 矢车菊蓝
,#B0C4DE LightSteelBlue 亮钢蓝
,#778899 LightSlateGray 亮蓝灰/亮石板灰
,#708090 SlateGray 灰石色/石板灰
,#1E90FF DodgerBlue 闪兰色/道奇蓝
,#F0F8FF AliceBlue 爱丽丝蓝
,#4682B4 SteelBlue 钢蓝/铁青
,#87CEFA LightSkyBlue 亮天蓝色
,#87CEEB SkyBlue 天蓝色
,#00BFFF DeepSkyBlue 深天蓝
,#ADD8E6 LightBlue 亮蓝
,#B0E0E6 PowderBlue 粉蓝色/火药青
,#5F9EA0 CadetBlue 军兰色/军服蓝
,#F0FFFF Azure 蔚蓝色
,#E0FFFF LightCyan 淡青色
,#AFEEEE PaleTurquoise 弱绿宝石
,#00FFFF Cyan 青色
,#00FFFF Aqua 浅绿色/水色
,#00CED1 DarkTurquoise 暗绿宝石
,#2F4F4F DarkSlateGray 暗瓦灰色/暗石板灰
,#008B8B DarkCyan 暗青色
,#008080 Teal 水鸭色
,#48D1CC MediumTurquoise 中绿宝石
,#20B2AA LightSeaGreen 浅海洋绿
,#40E0D0 Turquoise 绿宝石
,#7FFFD4 Aquamarine 宝石碧绿
,#66CDAA MediumAquamarine 中宝石碧绿
,#00FA9A MediumSpringGreen 中春绿色
,#F5FFFA MintCream 薄荷奶油
,#00FF7F SpringGreen 春绿色
,#3CB371 MediumSeaGreen 中海洋绿
,#2E8B57 SeaGreen 海洋绿
,#F0FFF0 Honeydew 蜜色/蜜瓜色
,#90EE90 LightGreen 淡绿色
,#98FB98 PaleGreen 弱绿色
,#8FBC8F DarkSeaGreen 暗海洋绿
,#32CD32 LimeGreen 闪光深绿
,#00FF00 Lime 闪光绿
,#228B22 ForestGreen 森林绿
,#008000 Green 纯绿
,#006400 DarkGreen 暗绿色
,#7FFF00 Chartreuse 黄绿色/查特酒绿
,#7CFC00 LawnGreen 草绿色/草坪绿
,#ADFF2F GreenYellow 绿黄色
,#556B2F DarkOliveGreen 暗橄榄绿
,#9ACD32 YellowGreen 黄绿色
,#6B8E23 OliveDrab 橄榄褐色
,#F5F5DC Beige 米色/灰棕色
,#FAFAD2 LightGoldenrodYellow 亮菊黄
,#FFFFF0 Ivory 象牙色
,#FFFFE0 LightYellow 浅黄色
,#FFFF00 Yellow 纯黄
,#808000 Olive 橄榄
,#BDB76B DarkKhaki 暗黄褐色/深卡叽布
,#FFFACD LemonChiffon 柠檬绸
,#EEE8AA PaleGoldenrod 灰菊黄/苍麒麟色
,#F0E68C Khaki 黄褐色/卡叽布
,#FFD700 Gold 金色
,#FFF8DC Cornsilk 玉米丝色
,#DAA520 Goldenrod 金菊黄
,#B8860B DarkGoldenrod 暗金菊黄
,#FFFAF0 FloralWhite 花的白色
,#FDF5E6 OldLace 老花色/旧蕾丝
,#F5DEB3 Wheat 浅黄色/小麦色
,#FFE4B5 Moccasin 鹿皮色/鹿皮靴
,#FFA500 Orange 橙色
,#FFEFD5 PapayaWhip 番木色/番木瓜
,#FFEBCD BlanchedAlmond 白杏色
,#FFDEAD NavajoWhite 纳瓦白/土著白
,#FAEBD7 AntiqueWhite 古董白
,#D2B48C Tan 茶色
,#DEB887 BurlyWood 硬木色
,#FFE4C4 Bisque 陶坯黄
,#FF8C00 DarkOrange 深橙色
,#FAF0E6 Linen 亚麻布
,#CD853F Peru 秘鲁色
,#FFDAB9 PeachPuff 桃肉色
,#F4A460 SandyBrown 沙棕色
,#D2691E Chocolate 巧克力色
,#8B4513 SaddleBrown 重褐色/马鞍棕色
,#FFF5EE Seashell 海贝壳
,#A0522D Sienna 黄土赭色
,#FFA07A LightSalmon 浅鲑鱼肉色
,#FF7F50 Coral 珊瑚
,#FF4500 OrangeRed 橙红色
,#E9967A DarkSalmon 深鲜肉/鲑鱼色
,#FF6347 Tomato 番茄红
,#FFE4E1 MistyRose 浅玫瑰色/薄雾玫瑰
,#FA8072 Salmon 鲜肉/鲑鱼色
,#FFFAFA Snow 雪白色
,#F08080 LightCoral 淡珊瑚色
,#BC8F8F RosyBrown 玫瑰棕色
,#CD5C5C IndianRed 印度红
,#FF0000 Red 纯红
,#A52A2A Brown 棕色
,#B22222 FireBrick 火砖色/耐火砖
,#8B0000 DarkRed 深红色
,#800000 Maroon 栗色
,#FFFFFF White 纯白
,#F5F5F5 WhiteSmoke 白烟
,#DCDCDC Gainsboro 淡灰色
,#D3D3D3 LightGrey 浅灰色
,#C0C0C0 Silver 银灰色
,#A9A9A9 DarkGray 深灰色
,#808080 Gray 灰色
,#696969 DimGray 暗淡灰
,#000000 Black 纯黑'''.lower().split("\n,")]
		# print(color)
		if 1:

			font = f"'{ziti}'"
			dic = {
				1: 27,
				2: 23,
				3: 22,
				4: 21,
				5: 20,
				6: 18
			}

			for x in range(5):
				obj.tag_config(f"H{x + 1}",font=(font, dic[x + 1], "bold"))
			for y in color:
				for x in range(6):
					obj.tag_config(f"H{x + 1}-{y[1].upper()}",foreground=f"{y[0]}",font=(font, dic[x + 1], "bold"))
					# print(f"H{x + 1}-{y[1]}")
					# except:
					# 	print(y[1])
					# 	print(f'obj.tag_config("H{x + 1}{y[1]}",fg="{y[0]}",font=({font}, {dic[x + 1]}, "bold"))')
			obj.tag_config("H6", font=(ziti, 18, 'normal'))

	def insert_img(obj, name):
		lengh = len(data_cache)
		z = PhotoImage(file=name)
		data_cache.append(z)
		obj.image_create(END, image=data_cache[lengh])
		obj.insert(END, "\n")

	def insert_window(obj, n):
		lengh = len(data_cache)
		data_cache.append(n)
		obj.window_create(END, window=data_cache[lengh])
		obj.insert(END, "\n")

	def to_url(url):
		import webbrowser
		webbrowser.open(url)

	def insert_http(obj, url, name=False):
		global ziti
		if name == False:
			name = url

		z = Label(obj, text=name, bg="white", fg="blue", cursor="arrow",font=(ziti, 18, "normal"))

		def open(*w):
			to_url(url)
			z.config(fg="purple")

		def inin(*w):
			z.config(font=(ziti, 18, "normal", "underline"))

		def out(*w):
			z.config(font=(ziti, 18, "normal"))

		z.bind("<Button-1>", open)
		z.bind("<Enter>", inin)
		z.bind("<Leave>", out)
		insert_window(obj,z)

	def insert_file(obj, url, name=False):
		global ziti
		if name == False:
			name = url

		z = Label(obj, text=name, bg="white", fg="blue", cursor="arrow", font=(ziti, 18, "normal"))

		def open(*w):
			import os
			os.startfile(url)
			z.config(fg="purple")

		def inin(*w):
			z.config(font=(ziti, 18, "normal", "underline"))

		def out(*w):
			z.config(font=(ziti, 18, "normal"))

		z.bind("<Button-1>", open)
		z.bind("<Enter>", inin)
		z.bind("<Leave>", out)
		insert_window(obj, z)

def parser(text_n, obj):
	v=[]
	for x in text_n.split("\n"):
		z = (x + "\n").split(":")
		if len(z) == 1:
			v.append(["H6", z[0]])
		elif len(z) == 2 or AC(z[0]):
			# print(z)
			v.append([z[0], ":".join(z[1:])])
		elif len(z) != 2 and z[0]=="MUC" or z[0]=="BGM" or z[0]=="IMG" or z[0]=="FILE":
			v.append([z[0],":".join(z[1:])])
		elif z[0] == "/":
			v.append(["H6", ":".join(z[1:])])
		else:
			# print(z)
			v.append(["H6", ":".join(z)])
	for x in v:
		if x[0] == "IMG":
			insert_img(obj, x[1].replace("\n", ""))
		elif x[0] == "BGM":
			insert_music(*x[1].replace("\n", "").split(","))
		elif x[0] == "URL":
			v = x[1].replace("\n", "").split(",")
			insert_http(obj, *v)
			del v
		elif x[0] == "MUC":
			insert_music_btn(obj,*x[1].replace("\n", "").split(","))

		elif x[0] == "WINDOW":
			insert_window(obj, eval(x[1]))

		elif x[0] == "FILE":
			v = x[1].replace("\n", "").split(",")
			insert_file(obj, *v)
			del v
		else:
			obj.insert("end", x[1], x[0].upper())

def add_note(title="", text_n=""):
	global note,ziti,note_it
	note_it=True
	v = []
	frame = Frame(note)
	# frame_cache.append(frame)
	# frame_lengh = len(frame_cache) - 1
	
	text = Text(frame)
	add_tag(text)

	# render
	parser(text_n, text)

	text.pack(fill=BOTH, expand=True)
	frame.pack(fill=BOTH, expand=True)
	text.config(state=DISABLED)
	note.add(frame, text=title)

def one_page(title="", text_n=""):
	global ziti
	frame = Frame(root)
	root.title(title)
	text = Text(frame)
	add_tag(text)
	parser(text_n,text)

	text.pack(fill=BOTH, expand=True)
	frame.pack(fill=BOTH, expand=True)
	text.config(state=DISABLED)

def run():
	if note_it:note.pack(fill=BOTH,expand=True)
	root.attributes("-alpha", 1)
	root.mainloop()
def title(text):
	root.title(text)
def win_size(x,y):
	root.geometry(x,y)




