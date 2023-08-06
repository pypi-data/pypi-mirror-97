#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.tix as tix

from . import xml_ui_tool

def CreateApp(xmlui):
    parser = xml_ui_tool.ElementParser(HandleCommonTag, xmlui)
    for parseTagName,parseTagClass in globals().items():
        if type(parseTagClass)==type:
            parser.regist_tag_handle(parseTagName, parseTagClass)
    return parser.parse(xmlui.xml_root, None).ui

class App(xml_ui_tool.HandleBase):
    def handle_self(self):
        self.ui = tix.Tk()

class HandleCommonTag(xml_ui_tool.HandleBase):
    def handle_self(self):
        tkClass = getattr(tix, self.xml_element.tag, None)
        if not tkClass:
            tkClass = getattr(ttk, self.xml_element.tag)
        if not tkClass:
            tkClass = getattr(tk, self.xml_element.tag)

        if not tkClass:
            return None

        self.ui = tkClass(self.ui_parent)

        options = {key:value for key,value in self.xml_element.items() if key in self.ui.keys()}
        if "text" in self.ui.keys() and self.xml_element.text and self.xml_element.text.strip():
            options["text"] = self.xml_element.text.strip()
        self.ui.config(options)

        pack_keys = ["anchor", "expand", "fill", "ipadx", "ipady", "padx", "pady", "side"]
        options = {key:value for key,value in self.xml_element.items() if key in pack_keys}
        self.ui.pack(options)

    def apply_attr_child_layout(self, attrValue):
        if attr_value=="row":
            for i, child in enumerate(self.ui.winfo_children()):
                child.grid(row=i, column=0)
        elif attr_value=="col":
            for i, child in enumerate(self.ui.winfo_children()):
                child.grid(row=0, column=i)

class PanedWindow(HandleCommonTag):
    def handle_over(self):
        for child in self.ui.winfo_children():
            self.ui.add(child)
