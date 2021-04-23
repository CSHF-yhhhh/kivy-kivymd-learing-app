
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout

import threading
from kivy.properties import StringProperty
from kivy.network.urlrequest import UrlRequest
import json
from Config import config_dict, record_dict
from kivy.lang import Builder
from client.client import server_url

KV_SortPage = open("./SortPage/SortPage.kv", "r", encoding="utf-8").read()
Builder.load_string(KV_SortPage)


class Row(MDBoxLayout):
    text_1 = StringProperty()
    text_2 = StringProperty()
    text_3 = StringProperty()
    def __init__(self,text_1 = '', text_2 ='', text_3 = '', **kw):
        super().__init__(**kw)
        self.text_1 = text_1
        self.text_2 = text_2
        self.text_3 = text_3

class Show(MDBoxLayout):
    back_event = None
    def __init__(self,row_data, **kw):
        super().__init__(**kw)
        #self.ids.box.add_widget(Row("排名","名称","学习数量"))
        for row in row_data:
            print(row)
            self.ids.box.add_widget(Row(str(row[0]),str(row[1]),str(row[2])))
        

class SortPage(Screen):
    text = StringProperty()
    def __init__(self, close_event, **kw):
        super().__init__(**kw)
        self.close_event = close_event
        self.total_nums = 0
        for key, value in record_dict.items():
            self.total_nums += int(value)
        threading.Thread(target=self.Refresh).start()
    def Refresh(self):
        try:
            self.sort_list = None
            self.my_sort = None
            def get_my_sort(req, result):
                self.my_sort = json.loads(result)
                if len(self.my_sort) and len(self.sort_list):
                    row_data = []
                    for key, line in self.sort_list.items():
                        t = (key, line[0], line[1])
                        row_data.append(t)
                    self.text = "当前排名:{}".format(self.my_sort.popitem()[0])
                    self.execl = Show(row_data = row_data)
                    self.ids.box.clear_widgets()
                    self.ids.box.add_widget(self.execl)
            def get_sort(req, result):
                self.sort_list = json.loads(result)
                UrlRequest(server_url + "/id/?id={}".format(int(config_dict["ID"])), get_my_sort)
            
            UrlRequest(server_url + "/update/?id={}&num={}".format(int(config_dict["ID"]), int(self.total_nums)))
            UrlRequest(server_url + "/top/?top=100", get_sort)
            

            """ def p(req, result):
                print(result)
            r = UrlRequest(server_url + "/top/?top=20", p)
            print(r)
            sort_list =  json.loads(requests.get(server_url + "/top/?top=20").text)
            my_sort = json.loads(requests.get(server_url + "/id/?id={}".format(int(config_dict["ID"]))).text)
            if len(my_sort) and len(sort_list):
                row_data = []
                for key, line in sort_list.items():
                    t = (key, line[0], line[1])
                    row_data.append(t)
                self.text = "当前排名:{}".format(my_sort.popitem()[0])
                self.execl = Show(row_data = row_data)
                self.ids.box.clear_widgets()
                self.ids.box.add_widget(self.execl) """
                
            
        except Exception as e:
            self.close_event()
            raise e
        
