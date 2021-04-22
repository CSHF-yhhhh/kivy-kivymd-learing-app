from kivy.uix.screenmanager import Screen

from kivy.properties import  StringProperty

from kivy.lang import Builder

KV_FirstInit = open("./FirstInit/FirstInit.kv", "r", encoding="utf-8").read()
Builder.load_string(KV_FirstInit)

class FirstInit(Screen):
    username = StringProperty()
    user_id = StringProperty()
    hint_text = StringProperty()
    def __init__(self,hint_text, back_event, **kwargs):
        """
        说明: 初始化界面的初始化函数
        args{
        }
        return:
        """
        super().__init__(**kwargs)
        self.hint_text = hint_text
        self.back_event = back_event
    
    def Commit(self):
        print(self.ids.input.text)
        self.back_event(self.ids.input.text)
