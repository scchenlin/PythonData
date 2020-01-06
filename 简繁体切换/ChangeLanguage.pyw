# -*- coding: utf-8 -*-
import wx,os
from 简繁体切换.langconv import Converter

def start(event):
    path = path_text.GetValue()
    content_text.SetValue("")
    if str(path).__eq__(""):
        content_text.SetValue("请先设置目录")
        return
    path = path.replace("\\","/")
    lookup(path)

def lookup(path):
    dirs = os.listdir(path)
    for file in dirs:
        tempPath = str(path +"/"+ file)#使用绝对路径
        if os.path.isdir(tempPath):
            lookup(tempPath)
        else:
            if file.__contains__(".xml"):
                change(tempPath)

#开始简繁体切换
def change(file):
    fileStr = ''
    with open(file, "r", encoding="utf-8") as f:  # encoding参数是为了在打开文件时将编码转为utf8
        fileStr = Converter('zh-hant').convert(f.read())
        f.close()
    with open(file, "w", encoding="utf-8") as f:  # encoding参数是为了在打开文件时将编码转为utf8
        f.write(fileStr)
        f.close()
    content_text.AppendText(file + "修改成功\n")

app = wx.App()

frame = wx.Frame(None, title="简繁体切换", pos=(1000, 200), size=(500, 400))

panel = wx.Panel(frame)

path_text = wx.TextCtrl(panel)

open_button = wx.Button(panel, label="开始转换")

open_button.Bind(wx.EVT_BUTTON, start)  # 绑定打开文件事件到open_button按钮上

#save_button = wx.Button(panel, label="保存")

content_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE)

#  wx.TE_MULTILINE可以实现以滚动条方式多行显示文本,若不加此功能文本文档显示为一行


box = wx.BoxSizer()  # 不带参数表示默认实例化一个水平尺寸器

box.Add(path_text, proportion=10, flag=wx.EXPAND | wx.ALL, border=3)  # 添加组件

# proportion：相对比例

# flag：填充的样式和方向,wx.EXPAND为完整填充，wx.ALL为填充的方向

# border：边框

box.Add(open_button, proportion=2, flag=wx.EXPAND | wx.ALL, border=3)  # 添加组件

#box.Add(save_button, proportion=2, flag=wx.EXPAND | wx.ALL, border=3)  # 添加组件

v_box = wx.BoxSizer(wx.VERTICAL)  # wx.VERTICAL参数表示实例化一个垂直尺寸器

v_box.Add(box, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)  # 添加组件

v_box.Add(content_text, proportion=5, flag=wx.EXPAND | wx.ALL, border=3)  # 添加组件

panel.SetSizer(v_box)  # 设置主尺寸器

frame.Show()

app.MainLoop()