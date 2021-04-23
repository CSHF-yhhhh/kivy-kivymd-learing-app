from sys import argv
from kivy.lang import Builder

from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.snackbar import Snackbar

from kivy.properties import StringProperty, NumericProperty, ColorProperty

from Config import config

KV_Detail = open("./Detail/Detail.kv", "r", encoding="utf-8").read()
Builder.load_string(KV_Detail)


class Content(MDBoxLayout):
    """
    每一种内容的容器,一个文本显示框
    """

    text = StringProperty()
    color = ColorProperty()
    halign = StringProperty("auto")
    font_style = StringProperty("Subtitle1")
    def __init__(self, text,font_style = "Subtitle1",color = (0,0,0,1), halign = "left",  **kwargs):
        super().__init__(**kwargs)
        self.text = str(text)
        self.font_style = font_style
        self.color = color
        self.halign = halign
        
        #self.ids.label.height = self.ids.label.texture_size[1]
        

class Picture(MDGridLayout):
    source = StringProperty()
    def __init__(self, source, **kwargs):
        super().__init__(**kwargs)
        self.source = source

        """ label = MDLabel(
            markup=True,
            text="[size={}][相关图片]: [/size]".format(int(config.font["Subtitle1"][1])),
            size_hint=(1, 0.15),
        )
        image = Image(source=source, size_hint=(1, 0.85))
        self.adaptive_height = True
        self.add_widget(label)
        self.add_widget(image)
        self.height = image.height + label.height """


class Detail(Screen):
    title = StringProperty()

    def __init__(self, content, **kwargs):
        """
        说明: 详情界面
        args{
            content:要显示的内容字典(如果key为图片则会显示图片)
            allow_show_list:允许显示的key
            back_event: 界面返回事件
        }
        return:
        """
        self.content = content
        self.copy = None
        self.snackbar = Snackbar(duration=1.5)  #提示窗
        super().__init__(**kwargs)
        
        # 添加标题,和基础相关信息
        self.ids.boxs.add_widget(
            Content(
                text = "[b]{}[/b]".format(content["内容"]),font_style="H6", halign="center"
            )
        )
        self.ids.boxs.add_widget(
            Content(
                text="[拼音]:[/font_family]{}\n[含义]:\n[i]{}[/i]".format(
                    content["拼音"],
                    content["含义"],
                ),
            )
        )
        if "例句" in content and content["例句"]:
            self.ids.boxs.add_widget(
                Content(
                    text="[例句]:[i]{}[/i]".format(
                        content["例句"]
                    )
                )
            )
        if "图片" in content and content["图片"]:
            self.ids.boxs.add_widget(Picture(source=content["图片"]))

        show_list = ["近义词", "反义词"]
        text = ""
        for name in show_list:
            if name in content and content[name]:
                ts = content[name].split(" ")
                cc = ""
                for s in ts:
                    if s:
                        cc += "[u]{}[/u]  ".format(s)
                text += "[{}]:\n[i]{}[/i]\n".format(name, cc)
        
        if text:
            if text[-1] == "\n":
                text = text[:-1]
            self.ids.boxs.add_widget(
                Content(
                    text="{}".format(
                        text)
                    )
                )
        show_list = [ "出处", "相关典故"]
        text = ""
        for name in show_list:
            if name in content and content[name]:
                text += "[{}]:\n[i]{}[/i]\n".format(name, content[name].replace("\t", ""))
        
        if text:
            if text[-1] == "\n":
                text = text[:-1]
            self.ids.boxs.add_widget(
                Content(
                    text="{}".format(
                        text)
                    )
                )

    def CopyToClipboard(self):
        if not self.copy:
            self.copy = TextInput()
        data = self.content["内容"] + "\n"
        show_list = ["拼音", "含义", "例句", "出处", "相关典故", "近义词", "反义词"]
        for show in show_list:
            if show in self.content and self.content[show]:
                data += "{}：{}\n".format(show, self.content[show])
        self.copy.copy(data)
        self.snackbar.text = "复制成功"
        self.snackbar.show()