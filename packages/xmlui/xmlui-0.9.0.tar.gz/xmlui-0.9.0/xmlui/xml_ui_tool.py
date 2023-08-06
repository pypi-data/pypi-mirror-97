#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xml.etree.ElementTree as ET

# 负责解析xml的逻辑过程
class DocParser:
    # xml_root: 要解析的xml节点
    # handle_classes(dict(tag,class)): 注册遇到tag时的处理类
    # defaultHandleClass(): 遇到没有注册的tag时的处理类
    # controllers(dict(name,class)): xml中的controller
    def __init__(self, xml_root, handle_classes, defaultHandleClass, controllers):
        self.xml_root = xml_root
        self.handle_class = handle_classes
        self.defaultHandleClass = defaultHandleClass
        self.controllers = controllers or {}

    def parse(self):
        return self.recursive_parse(None, self.xml_root)

    def recursive_parse(self, handle_parent, xml_element):
        HandleClass = self.handle_class.get(xml_element.tag, None) or self.defaultHandleClass
        handle_obj = HandleClass()

        controller_name = xml_element.get("controller", "").strip()
        if controller_name:
            new_controller = self.controllers[controller_name]()
        else:
            new_controller = None

        controller = new_controller
        if not controller and handle_parent:
            controller = handle_parent.controller
        handle_obj.init(self, handle_parent, xml_element, controller)

        handle_obj.handle()

        name = xml_element.get("name", "").strip()
        if name and handle_obj.get_result() and handle_parent and not hasattr(handle_parent.controller, name):
            setattr(handle_parent.controller or handle_parent.get_result(), name, handle_obj.get_result())

        handle_obj.handle_over()

        if new_controller:
            setattr(handle_obj.get_result(), "controller", new_controller)
            new_controller.node = handle_obj.get_result()
            new_controller.after_load()

        return handle_obj

# 处理一个tag及其属性的基类
class HandleTagBase:
    # parser(DocParser):
    # parent(HandleTagBase): 父处理节点
    # xml_element(): 要解析的节点
    # controller: 这个节点由哪个controller控制
    def init(self, parser, parent, xml_element, controller):
        self.parser = parser
        self.parent = parent
        self.xml_element = xml_element
        self.controller = controller

        # 处理结果
        # 
        # 处理后得到的ui节点
        self.ui = None
        # 处理后得到的非ui节点
        self.custom = None
        # 直接子节点(HandleTagBase)
        self.children = []

    def get_result(self):
        return self.ui or self.custom

    # 向上回溯，直到找到一个ui节点，包括自身
    def get_latest_ui(self):
        handle_obj = self
        while handle_obj and not handle_obj.ui:
            handle_obj = handle_obj.parent
        if handle_obj:
            return handle_obj.ui

    def handle(self):
        self.handle_self()
        self.handle_children()

    def handle_children(self):
        for child in self.xml_element:
            child_handle_obj = self.parser.recursive_parse(self, child)
            self.children.append(child_handle_obj)
            self.after_handle_child(child_handle_obj)

    # 子类应该重写这个类，在这个方法内部设置self.ui或self.custom节点
    def handle_self(self):
        pass

    # 每次解析完一个子节点回调一次
    def after_handle_child(self, child_handle_obj):
        pass

    # 整个节点解析完的回调
    def handle_over(self):
        pass

# 从字符串解析出python值
# attrValue: 
def convert_attr_value(attrValue, globals_dict):
    if not attrValue.strip():
        return attrValue
    else:
        try:
            return eval(attrValue, globals_dict)
        except:
            return attrValue