#!/usr/bin/python
# -*- coding: UTF-8 -*-

from . import xml_ui_tool
import xml.etree.ElementTree as ET

class Controller:
    def __init__(self):
        # node: 存储对应tag的处理结果
        self.node = None

    def after_load(self):
        pass

def load_wx(file_or_xmlstring, controllers):
    if "<" in file_or_xmlstring or ">" in file_or_xmlstring:
        xml_root = ET.fromstring(file_or_xmlstring)
    else:
        xml_doc = ET.parse(file_or_xmlstring)
        xml_root = xml_doc.getroot()

    from . import xml_wx

    handle_class = xml_wx.get_all_handle_class()

    if isinstance(controllers, list):
        controllers = {clas.__name__:clas for clas in controllers}
    elif controllers:
        controllers = {controllers.__name__:controllers}
    else:
        controllers = {}

    parser = xml_ui_tool.DocParser(xml_root, handle_class, xml_wx.HandleCommonTag, controllers)
    handle_app = parser.parse()
    return handle_app.get_result()
