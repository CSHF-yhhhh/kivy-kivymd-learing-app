
from kivy.uix.stacklayout import StackLayout
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager
from SortPage.SortPage import SortPage
from kivy.graphics import Color, Rectangle, Line

from kivy.properties import StringProperty, ColorProperty

from kivy.lang import Builder

from Config import record_dict, config
import time

KV_Record = open("./Record/Record.kv", "r", encoding="utf-8").read()
Builder.load_string(KV_Record)



class Buttom_label(MDLabel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Bar(StackLayout):
    bar_name = StringProperty()
    value = 0
    bg_color = ColorProperty()
    def __init__(self,bar_name, value, max_value,bg_color, **kwargs):
        super().__init__(**kwargs)
        self.bar_name = bar_name
        self.value = value / max_value * 0.9
        t = value / max_value
        bg_color[0] = bg_color[0] * t + 0.55
        bg_color[1] = bg_color[1] * t + 0.55
        bg_color[2] = bg_color[2] * t + 0.55
        self.bg_color = bg_color

class BarGraph(ScrollView):
    bar_color = ColorProperty()
    def __init__(self,record, **kwargs):
        super().__init__(**kwargs)
        #绘制图像的方法
        self.record = record
        print(self.bar_color)
        max_count = 0
        for key in record:
            if record[key] > max_count:
                max_count = record[key]
        max_count += 10
        i = 1
        for day in record:
            count = record[day]
            bar = Bar(str(count), count, max_count, self.bar_color.copy())
            i += 1
            self.ids.box.add_widget(bar)
            self.ids.buttom.add_widget(Buttom_label(text = day.replace("月", "-").replace("日", "")))
        self.scroll_x = 1

class Record(ScreenManager):
    title = StringProperty()
    total_days = StringProperty()
    total_nums = StringProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.now_show = None #当前显示的记录
        now = time.localtime()
        self.sort_page = None
        self.max_year = self.year = now.tm_year
        self.max_month = self.month = now.tm_mon
        self.title = "学习记录\n{}年{}月".format(self.year, self.month)

        self.Update()

    def Update(self):
        self.ids.picture.clear_widgets()
        result = config.GetRecord(self.year, self.month)
        self.ids.picture.add_widget(BarGraph(record= result))
        self.total_days = str(record_dict.__len__())
        total_nums = 0
        for key, value in record_dict.items():
            total_nums += value
        self.total_nums = str(total_nums)
    def LastYear(self):
        if self.year - 1 >= 2020:
            self.year -= 1
            self.title = "学习记录\n{}年{}月".format(self.year, self.month)
            self.Update()
    def NextYear(self):
        if self.year + 1 < self.max_year:
            self.year += 1
            self.title = "学习记录\n{}年{}月".format(self.year, self.month)
            self.Update()
        elif self.year + 1 == self.max_year:
            if self.month > self.max_month:
                self.month = self.max_month
            self.year += 1
            self.title = "学习记录\n{}年{}月".format(self.year, self.month)
            self.Update()
            
    def LastMonth(self):
        #上一个月的记录
        if self.month - 1 < 1:#要看上一年
            if self.year - 1 >= 2019:
                #在允许显示的范围内
                self.month = 12
                self.year -= 1
                self.title = "学习记录\n{}年{}月".format(self.year, self.month)
                self.Update()
            else:
                #禁止的范围
                pass
        else:
            self.month -= 1
            self.title = "学习记录\n{}年{}月".format(self.year, self.month)
            self.Update()
    def NextMonth(self):
        #下一个月的记录
            if self.month + 1 > 12:#要看下一个年
                if self.year + 1 <= self.max_year:
                    #在允许显示的范围内
                    self.month = 1
                    self.year += 1
                    self.title = "学习记录\n{}年{}月".format(self.year, self.month)
                    self.Update()
                else:
                    #禁止的范围
                    pass
            elif self.max_year > self.year or self.month + 1 <= self.max_month:
                self.month += 1
                self.title = "学习记录\n{}年{}月".format(self.year, self.month)
                self.Update()

    def ShowSort(self):
        if not self.sort_page:
            self.sort_page = SortPage(self.CloseSort, name = "Sort")
            print(self.sort_page)
            self.add_widget(self.sort_page)
            self.current = "Sort"
    
    def CloseSort(self):
        if self.sort_page:
            self.current = "Main"
            self.remove_widget(self.sort_page)
            del self.sort_page
            self.sort_page = None

