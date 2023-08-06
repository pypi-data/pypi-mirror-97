# xmlui

* 使用wxPython开发ui的时候，可以手写ui界面，也可以使用wxFormBuilder。但是：
  * 手写ui界面代码太多，并且写起来很麻烦
  * 使用wxFormBuilder等可视化工具，需要维护额外的工程文件。
* 这个项目借鉴了html的书写方式，用**易手写**的xml描述ui结构，在.py文件中处理业务逻辑。
* 环境依赖
  * python==2.x
  * wxPython==4.1.0

# 安装

```
pip install xmlui
```

# 使用

## 1.使用xml描述UI结构

* wx_simple.xml

```xml
<App>
	<Frame controller="MainController">
		<Button name="ui_mybtn" label="按钮1" onclick="OnClickButton"></Button>
	</Frame>
</App>
```

## 2.编写代码，显示界面

```python
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
```
# 原理
* xml中的每个tag标签都可以创建一类对象
    1. 普通的wx对象，例如本例中的wx.App,wx.Frame,wx.Button等，及其他wx命名空间下的继承于wx.Window的对象。
    2. 绑定事件(见下面的例子)：`<Bind type="wx.EVT_BUTTON">OnClickButton</Bind>`
    3. 创建布局器，只支持BoxSizer(见下面的例子)
    4. 创建菜单，支持应用程序菜单和右键菜单两种，使用方式见sample/wx_menu.py。
* 可以在代码中定义一个控制类，并在xml中使用。本例中为MainController，这个类有下面的成员：
  * `xmlui.Controller.node`：对应的xml中的节点，这个例子里是Frame的实例。
  * `after_load`：整个节点加载完的回调函数
  * controller属性可以加在xml中的任意节点上，并支持嵌套。
* 更复杂的例子可以参考sample目录下的内容

# xml所支持的配置内容

## 直接拼普通的界面

例如wx.Frame，wx.Button，wx.StaticText，wx.TextEntry等，都可以使用这样的配置方式

```xml
<App>
	<Frame id="1000" style="wx.BORDER_SUNKEN">
        <StaticText label="姓名"></StaticText>
		<Button label="提交"></Button>
	</Frame>
</App>
```

其中支持以下可选参数：

* id：窗口id
* title：窗口标题，关键字也可以为label
* pos：窗口位置
* size：窗口大小
* style：窗口的风格

**注意**：这些参数会被传递到wx.Window的构造函数中，如果参数不正确，会导致wx内部抛出异常。例如给wx.Button传递title参数是不可以的，只能传递label参数。

## 只支持BoxSizer布局

举例如下：

```xml
<App>
    <Frame controller="MainController">
        <BoxSizer orient="v" proportion="0,1,0" flags="wx.EXPAND,wx.EXPAND,wx.EXPAND">
            <Panel></Panel>
            <Panel></Panel>
            <Panel></Panel>
        </BoxSizer>
    </Frame>
</App>
```

BoxSizer支持以下可选参数：

* orient：布局方向。"v"代表垂直，"h"代表水平。默认为"h"
* proportion：每个面板的拉伸比例
* flags：每个面板的额外标志

## 绑定事件

只有继承于wx.Window的类，才能绑定事件

```xml
<App>
	<Frame>
		<Button label="提交">
            <Bind type="wx.EVT_BUTTON">OnClickButton</Bind>
        </Button>
	</Frame>
</App>
```

有些事件有onxxx简写形式，包括

* wx.Button的点击事件: `<Button label="提交" onclick="OnClickButton">`
* wx.MenuItem的点击事件: `<MenuItem onclick="OnMenuItem1"></MenuItem>`

## 同时加载多个窗口

```xml
<App controller="MainController">
	<Frame name="main_frame">
		<Button name="ui_mybtn" label="按钮1" onclick="OnClickButton"></Button>
	</Frame>
	<Dialog title="my dialog" name="ui_mydlg"></Dialog>
</App>
```

```python
class MainController(xmlui.Controller):
    def OnClickButton(self, evt):
        self.ui_mydlg.ShowModal()
```

* 这个例子里有两个窗口，其中main_frame是一开始就显示出来的，ui_mydlg是需要用代码控制显示出来的。

