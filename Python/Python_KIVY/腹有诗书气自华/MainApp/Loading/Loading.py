from kivy.lang import Builder

from kivy.uix.screenmanager import Screen


KV_Loading = open("./Loading/Loading.kv", "r", encoding="utf-8").read()
Builder.load_string(KV_Loading)
class Loading(Screen):
    '''Loading'''