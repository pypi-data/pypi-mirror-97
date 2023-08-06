#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from . import xml_ui_tool

def get_all_handle_class():
    return {k:v for k,v in globals().items() if type(v)==type or type(v).__name__=="classobj"}

def convert_attr_value(value):
    return xml_ui_tool.convert_attr_value(value, {"wx":wx})

class HandleCommonTag(xml_ui_tool.HandleTagBase):
    def handle_self(self):
        iscallfunc = self.check_call_func()
        if iscallfunc:
            return

        self.custom = self.create_custom()
        if self.custom:
            self.apply_all_attrs()
            return

        self.ui = self.create_ui()
        if self.ui:
            self.apply_all_attrs()
            return

    # 优先假设xml_element.tag是一个可执行函数
    def check_call_func(self):
        func = getattr(self.parent, self.xml_element.tag, None)
        if not func:
            func = getattr(self, self.xml_element.tag, None)
        if not func and self.parent:
            func = getattr(self.parent.get_result(), self.xml_element.tag, None)

        if not callable(func):
            return False

        if not self.xml_element.text or not self.xml_element.text.strip():
            func()
        else:
            params = xml_ui_tool.convert_attr_value(self.xml_element.text, {"wx":wx})
            if isinstance(params, tuple):
                func(*params)
            else:
                func(params)

        return True

    def create_custom(self):
        return None

    # 尝试创建ui节点
    def create_ui(self):
        wxClass = getattr(wx, self.xml_element.tag, None)
        if not wxClass:
            return None
        
        args = {}
        self.pick_constructor_arg(args, "id")
        self.pick_constructor_arg(args, "title")
        self.pick_constructor_arg(args, "pos")
        self.pick_constructor_arg(args, "size")
        self.pick_constructor_arg(args, "style")
        self.pick_constructor_arg(args, "label")
        
        ui = wxClass(self.get_latest_ui(), **args)

        return ui

    def apply_all_attrs(self):
        for attrName, attrValue in self.xml_element.items():
            func = getattr(self, "apply_attr_"+attrName, None)
            if func:
                func(xml_ui_tool.convert_attr_value(attrValue, {"wx":wx}))
                continue

            func = getattr(self.get_result(), attrName, None)
            if callable(func):
                func(xml_ui_tool.convert_attr_value(attrValue, {"wx":wx}))

    def pick_constructor_arg(self, args, name):
        attr = self.xml_element.get(name)
        if attr and attr.strip():
            args[name] = xml_ui_tool.convert_attr_value(attr, {"wx":wx})

    def apply_attr_title(self, value):
        self.get_result().SetTitle(value)

    def apply_attr_onclick(self, value):
        if isinstance(self.get_result(), wx.Button):
            bindtype = wx.EVT_BUTTON
            bindfunc = getattr(self.controller, value.strip(), None)
            if bindfunc:
                self.get_latest_evt_handler().Bind(bindtype, bindfunc, None)
        elif isinstance(self.get_result(), wx.MenuItem):
            bindtype = wx.EVT_MENU
            bindfunc = getattr(self.controller, value.strip(), None)
            if bindfunc:
                self.get_latest_evt_handler().Bind(bindtype, bindfunc, id=self.custom.GetId())

    def get_latest_evt_handler(self):
        handle_obj = self
        while handle_obj and not isinstance(handle_obj.get_result(), wx.EvtHandler):
            handle_obj = handle_obj.parent
        if handle_obj:
            return handle_obj.get_result()

    def handle_over(self):
        if type(self.ui) in [wx.Window, wx.Panel, wx.Frame] and not self.ui.GetSizer():
            self.add_default_layout()

    def add_default_layout(self):
        ui_children = filter(lambda c: c.ui, self.children)
        if len(ui_children)==0: return

        one_child = len(ui_children)==1

        orient = wx.VERTICAL if self.xml_element.get("sizer_orient")=="v" else wx.HORIZONTAL

        sizer = wx.BoxSizer(orient)
        for child in self.children:
            if child.ui:
                proportion = 1 if one_child else int(child.xml_element.get("sizer_proportion", "0"))
                flags = wx.EXPAND if one_child else convert_attr_value(child.xml_element.get("sizer_flags", "0"))
                sizer.Add(child.ui, proportion, flags)
        self.ui.SetSizer(sizer)

class App(xml_ui_tool.HandleTagBase):
    def __init__(self):
        self.main_frame = None
    def handle_self(self):
        self.custom = wx.App()
    def after_handle_child(self, child_handle_obj):
        if self.main_frame:
            return

        if child_handle_obj.ui:
            self.main_frame = child_handle_obj.ui
            self.main_frame.Show()

class BoxSizer(xml_ui_tool.HandleTagBase):
    def handle_self(self):
        orient = wx.HORIZONTAL
        if self.xml_element.get("orient", None)=="v":
            orient = wx.VERTICAL

        self.custom = wx.BoxSizer(orient)

        self.proportion = None
        if self.xml_element.get("proportion", "").strip():
            self.proportion = xml_ui_tool.convert_attr_value(self.xml_element.get("proportion"), {"wx":wx})
        if isinstance(self.proportion, int):
            self.proportion = [self.proportion]

        self.flags = None
        if self.xml_element.get("flags", None):
            self.flags = xml_ui_tool.convert_attr_value(self.xml_element.get("flags"), {"wx":wx})
        if isinstance(self.flags, int):
            self.flags = [self.flags]

    def after_handle_child(self, child_handle_obj):
        if child_handle_obj.ui:
            prop = self.proportion[len(self.children)-1] if self.proportion and len(self.proportion)>=len(self.children) else 0
            if not self.flags:
                flag = 0
            elif len(self.flags)>=len(self.children):
                flag = self.flags[len(self.children)-1]
            else:
                flag = self.flags[-1]
            self.custom.Add(child_handle_obj.ui, prop, flag)

    def handle_over(self):
        self.parent.ui.SetSizer(self.custom)
        self.custom.Fit(self.parent.ui)

class SplitterWindow(HandleCommonTag):
    def SetSashPosition(self, attrValue):
        p1, p2 = self.ui.GetChildren()
        if self.ui.GetSplitMode()==wx.SPLIT_HORIZONTAL:
            self.ui.SplitHorizontally(p1, p2, attrValue)
        elif self.ui.GetSplitMode()==wx.SPLIT_VERTICAL:
            self.ui.SplitVertically(p1, p2, attrValue)

class Bind(HandleCommonTag):
    def handle_self(self):
        bindtype = xml_ui_tool.convert_attr_value(self.xml_element.get("type"), {"wx":wx})
        bindfunc = getattr(self.controller, self.xml_element.text.strip(), None)
        if bindfunc:
            self.get_latest_evt_handler().Bind(bindtype, bindfunc, None)

class MenuBar(HandleCommonTag):
    def create_custom(self):
        return wx.MenuBar()
    def after_handle_child(self, child_handle_obj):
        self.custom.Append(child_handle_obj.get_result(), child_handle_obj.label)
    def handle_over(self):
        if self.parent.ui:
            self.parent.ui.SetMenuBar(self.custom)

class Menu(HandleCommonTag):
    def create_custom(self):
        return wx.Menu()
    def after_handle_child(self, child_handle_obj):
        if isinstance(child_handle_obj, Menu):
            self.get_result().AppendSubMenu(child_handle_obj.get_result(), child_handle_obj.label)
        else:
            self.get_result().Append(child_handle_obj.get_result())
    def apply_attr_label(self, value):
        self.label = value

class MenuItem(HandleCommonTag):
    def create_custom(self):
        id = int(self.xml_element.get("id", "-1"))
        text = self.xml_element.get("label",None) or self.xml_element.get("text",None)
        helpString = self.xml_element.get("helpString","")
        kind = convert_attr_value(self.xml_element.get("kind", "wx.ITEM_NORMAL"))
        return wx.MenuItem(None, id, text, helpString, kind)









