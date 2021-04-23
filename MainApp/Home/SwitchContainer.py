# -*- encoding: utf-8 -*-
'''
@文件:SwitchContainer.py
@说明:轮播控件
'''

from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock
from kivy.lang import Builder


KV = '''
<SwitchContainer>:
    canvas.before:
        Color:
            rgba: (1, 1, 1, 1)
        RoundedRectangle:
            size: self.size
            pos: self.pos
            source: "appPicture/paper.jpg"
'''
Builder.load_string(KV)
class SwitchContainer(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #管理器
        self.screen_manager = ScreenManager()
        self.add_widget(self.screen_manager)
        self.page_list = []

        #事件循环
        self.event = Clock.schedule_interval(self.Start, 5)

    def AddPage(self, page_name, page):
        '''
        说明: 添加一个页面来显示
        args{
            page_name: 屏幕的名字
            page:要显示的内容(控件,非Screen)
        }
        return: 
        '''
        
        screen = Screen(name = page_name)
        screen.add_widget(page)
        self.page_list.append(page_name)
        self.screen_manager.add_widget(screen)
        self.screen_manager.current = page_name
        
    def DeletePage(self, page_name):
        '''
        说明: 
        args{
            page_name: 要移除的屏幕的名字
        }
        return: 
        '''
        
        if self.screen_manager.has_screen(page_name):
            page = self.screen_manager.get_screen(page_name)
            self.screen_manager.remove_widget(page)
            self.page_list.remove(page_name)
    def DeleteAll(self):
        '''
        说明: 移除全部屏幕
        args{
            
        }
        return: 
        '''
        
        while len(self.page_list):
            self.DeletePage(self.page_list[0])
    def Start(self, *args):
        '''
        说明: 循环事件
        args{
            
        }
        return: 
        '''
        
        if len(self.page_list) > 1:
            index = (self.page_list.index(self.screen_manager.current) + 1) % len(self.page_list)
            self.screen_manager.current = self.page_list[index]