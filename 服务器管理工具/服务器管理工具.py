#encoding: utf-8
import wx,socket,os,json


###本脚本需要修改之参数############
game1 = "192.168.2.136(魔魂之刃内网测试服)"
game2 = "192.168.2.138(洛神曲内网测试服)"
games = {game2.decode('utf8'):'192.168.2.138', game1.decode('utf8'):'192.168.2.136'}
###################################
mychoice = ""
title = "络舒科技内网测试服管理工具"
start_label = "启动服务器"
stop_label = "关闭服务器"
check_server_start = "检查启动"
check_server_stop= "检查关闭"
fast_shutdown = "强制关闭"
# update_java = "java更新"
reset_date = "修改系统时间"
date_name = "eg:2017-11-16 10:00:00"

def send_socket(ServerIp, SendMsg):
    bufsize = 81920
    addr = (ServerIp, 1002)
    if ServerIp :
        try:
            SendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            SendSocket.connect(addr)
            SendSocket.send(SendMsg)
            data = SendSocket.recv(bufsize)
            if not len(data):
                return "No result form" + ServerIp + "back"
            SendSocket.close()
            return data
        except:
            return '{"code":"-5","codemessage":"connect server error"}'
        finally:
            SendSocket.close()
    else:
        return "Please choice your games first!!!!"


class Mywin(wx.Frame):
    def __init__(self, parent, title):
        super(Mywin, self).__init__(parent, title=title, size=(792, 335))

        panel = wx.Panel(self)

        self.choice = wx.Choice(panel, choices=games.keys())
        self.choice.Bind(wx.EVT_CHOICE, self.OnChoice)


        self.startButton = wx.Button(panel, label=start_label.decode('utf8'))
        self.startButton.Bind(wx.EVT_BUTTON, self.start)

        self.stopButton = wx.Button(panel, label=stop_label.decode('utf8'))
        self.stopButton.Bind(wx.EVT_BUTTON, self.stop)

        self.checkSartButton = wx.Button(panel, label=check_server_start.decode('utf8'))
        self.checkSartButton.Bind(wx.EVT_BUTTON, self.checkstart)

        self.checkStopButton = wx.Button(panel, label=check_server_stop.decode('utf8'))
        self.checkStopButton.Bind(wx.EVT_BUTTON, self.checkstop)

        self.shutdownserver = wx.Button(panel, label=fast_shutdown.decode('utf8'))
        self.shutdownserver.Bind(wx.EVT_BUTTON, self.shutdown)

        # self.updatejavaButton = wx.Button(panel, label=update_java.decode('utf8'))
        # self.updatejavaButton.Bind(wx.EVT_BUTTON, self.updatejava)

        self.resetdateButton = wx.Button(panel, label=reset_date.decode('utf8'))
        self.resetdateButton.Bind(wx.EVT_BUTTON, self.ressetdate)

        self.datename = wx.TextCtrl(panel, value=date_name.decode('utf8'))
        self.contents = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.HSCROLL)

        hbox = wx.BoxSizer()
        hbox.Add(self.choice, proportion=0, flag=wx.LEFT, border=5)
        hbox.Add(self.startButton, proportion=0, flag=wx.LEFT, border=5)
        hbox.Add(self.stopButton, proportion=0, flag=wx.LEFT, border=5)
        hbox.Add(self.checkSartButton, proportion=0, flag=wx.LEFT, border=5)
        hbox.Add(self.checkStopButton, proportion=0, flag=wx.LEFT, border=5)
        hbox.Add(self.shutdownserver, proportion=0, flag=wx.LEFT, border=5)
        #hbox.Add(self.updatejavaButton, proportion=0, flag=wx.LEFT, border=5)

        tbox = wx.BoxSizer()
        tbox.Add(self.datename, proportion=1, flag=wx.EXPAND, border=5)
        tbox.Add(self.resetdateButton, proportion=0, flag=wx.LEFT, border=5)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        vbox.Add(tbox, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        vbox.Add(self.contents, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=10)

        panel.SetSizer(vbox)

        self.Centre()
        self.Show()

    def OnChoice(self, event):
        global mychoice
        mychoice = games[self.choice.GetString(self.choice.GetSelection())]


    def start(self, event):
        msg = "start_server"
        result = send_socket(mychoice, msg)
        self.contents.SetValue(result)

    def stop(self, event):
        msg = "stop_server"
        result = send_socket(mychoice, msg)
        self.contents.SetValue(result)

    def checkstart(self, event):
        msg = "check_start"
        result = send_socket(mychoice, msg)
        self.contents.SetValue(result)

    def checkstop(self, event):
        msg = "check_stop"
        result = send_socket(mychoice, msg)
        self.contents.SetValue(result)

    def shutdown(self, event):
        msg = "shutdown_force"
        result = send_socket(mychoice, msg)
        self.contents.SetValue(result)

    # def updatejava(self, event):
    #     msg = "update_java"
    #     result = send_socket(mychoice, msg)
    #     self.contents.SetValue(result)

    def ressetdate(self, event):
        time = self.datename.GetValue()
        msg = "reset_date?%s" % (time)
        msg = str(msg)
        result = send_socket(mychoice, msg)
        self.contents.SetValue(result)


app = wx.App(redirect=True, filename="app.log")
Mywin(None, title.decode('utf8'))
app.MainLoop()
