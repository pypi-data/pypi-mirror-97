from . import *
add_note("1.基本使用方法",f"""
h2:1.基本使用方法
h3:1.1基本模板
需要文件：
1.✔shower.py
2.✔img整个文件夹，包括：
	-o.png
	--.png
	x-.png
	x0.png
代码模板：
	from shower import *
	#在这里编程
	run()

h3:1.2一些库方法
导入shower后，我们就可以愉快地进行编程了！
此时，你有两种开教程的选择
1.使用add_note方法
add_note(标签页标题[字符串],内容[转义模板])# [转义模板]将在：2.转义模板用法详细解释
我们这个窗口就是使用的add_note创建的
不过默认的窗口标题为Beautiful_window
修改方式
在add_note的后方加入：
title(你要设置的窗口标题)

2.使用one_page方法
one_page(窗口标题[字符串],内容[转义模板])# [转义模板]将在：2.转义模板用法详细解释
这个就是没有标签页的，只有单独页码
细心的朋友可能会发现这个没有使用title功能因为已经在
one_page方法内部定义了

注意这两种方法只能二选一！！！！！
否则会变成有两个页面！！！！！！！
【除非你就是想要那种效果】

#下一页介绍转义模板
IMG:{where_data("logo.gif")}
""")
add_note("2.转义模板",f"""h2:2.转义模板
h3:2.1字体大小变化
/:h1:nnn [下面为效果]
h1:nnn
/:h2:nnn
h2:nnn
/:h3:nnn
h3:nnn
/:h4:nnn
h4:nnn
/:h5:nnn
h5:nnn
/:h6:nnn【这个为默认字体】
h6:nnn

或者什么都不加默认为h6
h4:但是要注意”:“必须为英文冒号（后面其他转义也是）

/:但你面对例如”下一道题:“这种里面有英文冒号的文本时
/:（且只有一个，超过一个不需要这样做），有两种解决方案:
1.”下一道题：“（把英文的冒号改成中文的）
/:2.”/:下一道题:“（在最前面加上/:）
注意这两种不能混用

h3:2.2增加一些图片
h4:IMG:图片位置 #注意图片位置不能带冒号，下文件与链接同
/:例：IMG:title.png
IMG:{where_data("title.png")}

h3:2.3增加链接和文件
其实这两个语法差不多我就放一起了
放链接：

#注意链接与打开的文件位置不能带冒号
h4:URL:链接[,显示文字]
例1:URL:baidu.com
URL:baidu.com

例2:URL:baidu.com,百度
URL:baidu.com,百度

h4:FILE:打开的文件位置[,显示文字]
例1:FILE:logo.gif
FILE:{where_data("logo.gif")}

例2:FILE:logo.gif,LOGO图片
FILE:{where_data("logo.gif")},LOGO图片

h3:2.3添加tkinter控件[选用]
这个方法还是稍微复杂了一些，需要有一些tkinter功底

h4:用法：WINDOW:tk小控件
例1:WINDOW:Label(text="NICE")
WINDOW:Label(text="NICE")
例2:WINDOW:Button(text="NICE")
WINDOW:Button(text="NICE")

#下一章节介绍字体转色
""")
add_note("3.字体变色",f"""h2:3.字体变色
h3:3.1一些简单的尝试
h6-red:nice
h6-blue:nice
h6-purple:nice
h6-gold:nice
h6-green:nice
h6-lightgreen:nice

h3:3.2具体方法
h4:“（h1-6）“+”-“+”颜色（英文名不带空格）“+:+”文本内容”
例1:h3-red:NICE
h3-red:NICE

例2:h5-gold:NICE
h5-gold:NICE
具体支持的颜色附在这节最末尾

附录1：
IMG:{where_data("颜色表.png")}

""")
add_note("4.音乐文档",f"""h1:音乐相关控件
h6-red:路径中不能加“,”！！！
/:背景音乐->BGM:背景音乐文件名称(建议用ogg或者MP3，wav要用未压缩过的)
例:BGM:bgm.ogg
BGM:{where_data("bgm.ogg")}
这个不会显示但是右键菜单会发现多了一些东西:
·停止
·继续
·调整音量大小

/:点击播放音乐自带器->MUC:音乐名称,(声音大小【1-0的浮点数，默认为1.0】,重复播放次数【整数，默认为1】,显示文件名称)
例：
/:1.MUC:bgm.ogg
MUC:{where_data("bgm.ogg")}
/:2.MUC:bgm.ogg,0.5,1,starlight
MUC:{where_data("bgm.ogg")},0.5,1,starlight

""")
title("展示器教程")
root.geometry(1000,800)
run()
