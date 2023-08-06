#!/usr/bin/python
# encoding=utf8


# 演示使用默认的BoxSizer
# 
# 开发环境：
#   python: 2.7
#   wxPython: 4.1.0

import sys
sys.path.append("../..")

import xmlui
import wx

class MainController(xmlui.Controller):
    def __init__(self):
        pass

    def after_load(self):
        pass

    def OnClickSubmit(self, evt):
    	s = u"用户名:"+self.ui_name.GetValue()+"\n"
    	s += u"密码:"+self.ui_pass.GetValue()+"\n"
        wx.MessageBox(s)

def main():
    app = xmlui.load_wx("wx_defaultlayout.xml", [MainController])
    app.MainLoop()

if __name__ == '__main__':
    main()
