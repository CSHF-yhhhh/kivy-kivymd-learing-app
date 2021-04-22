# -*- encoding: utf-8 -*-
'''
@文件:FinishPage.py
@说明: 
'''
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import OneLineAvatarListItem
from kivy.properties import ColorProperty

from kivy.lang import Builder

KV_FinishPage = open("./FinishPage/FinishPage.kv", "r", encoding="utf-8").read()
Builder.load_string(KV_FinishPage)

class Item(OneLineAvatarListItem):
    def __init__(self,content, **kwargs):
        super().__init__(**kwargs)
        self.content = content
        self.text = content["内容"]


class FinishPage(Screen):
    primary_color = ColorProperty()
    def __init__(self,contents, **kw):
        super().__init__(**kw)
        
        for index, content in contents.items():

            item = Item(content)
            if "has_answer" in content:
                self.ids.boxs.add_widget(item)