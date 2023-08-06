#!/usr/bin/python
# encoding=utf8


# 最简单的示例窗口
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

    def OnClickButton(self, evt):
        wx.MessageBox(self.ui_mybtn.GetLabel())

def main():
    app = xmlui.load_wx("wx_simple.xml", [MainController])
    app.MainLoop()

if __name__ == '__main__':
    main()
