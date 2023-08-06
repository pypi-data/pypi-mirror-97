#!/usr/bin/python
# encoding=utf8


# 展示如何加载多个窗口
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
        self.ui_mydlg.ShowModal()

def main():
    app = xmlui.load_wx("wx_multiwindow.xml", [MainController])
    app.MainLoop()

if __name__ == '__main__':
    main()
