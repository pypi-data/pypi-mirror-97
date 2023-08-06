#!/usr/bin/python
# encoding=utf8


# 演示如何添加菜单
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

    def OnMenuItem1(self, evt):
    	wx.MessageBox("OnMenuItem1")
    def OnMenuItem2(self, evt):
    	self.node.PopupMenu(self.ui_popup)

    def OnMenuPopup(self, evt):
        wx.MessageBox("popup")

def main():
    app = xmlui.load_wx("wx_menu.xml", [MainController])
    app.MainLoop()

if __name__ == '__main__':
    main()
