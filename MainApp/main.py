# -*- encoding: utf-8 -*-
"""
@文件:main.py
@说明: 主程序
"""

# 字体初始化----------------------------------------
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivymd.font_definitions import theme_font_styles

# 注册字体
font_file = __file__[: __file__.rfind("\\") + 1] + "siyuan.ttf"
LabelBase.register(name="SiYuan", fn_regular=font_file)
theme_font_styles.append("SiYuan")
LabelBase.register(DEFAULT_FONT, "./siyuan.ttf")
# --------------------------------------------------------------------------------

# 设置窗口大小----------------------------------------
from kivy.utils import platform
from kivy.core.window import Window

if platform == "win" or platform == "linux":
    Window.size = (335, 600)
# --------------------------------------------------------------------------------

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.snackbar import Snackbar

from Config import config, config_dict
from kivy.network.urlrequest import UrlRequest
import json

from Home.Home import Home
from User.User import User
from Detail.Detail import Detail
from StudyPage.StudyPage import StudyPage
from Loading.Loading import Loading
from Record.Record import Record
from FinishPage.FinishPage import FinishPage
from Challenge.Challenge import Challenge
from FirstInit.FirstInit import FirstInit
from client.client import server_url
from time import time



class ChengYu(MDApp):
    def build(self):
        self.width = Window.size[0]
        self.spacing = Window.size[0] * 0.02

        self.last_time = 0
        Window.bind(on_keyboard=self.BackEvent)#绑定按下返回键的事件
        # 更改字体设置----------------------------------------
        font = (Window.size[1] ** 2 + Window.size[0] ** 2) ** 0.45 / (
            Window.size[0]
        )  # 动态求字体大小
        self.theme_cls.font_styles["SiYuan"] = [
            "SiYuan",
            16,
            False,
            0.15,
        ]
        for key in self.theme_cls.font_styles:
            if key != "Icon":
                self.theme_cls.font_styles[key][0] = "SiYuan"
                #self.theme_cls.font_styles[key][1] *= font
        config.font = self.theme_cls.font_styles
        print(config.font)
        config.theme_cls = self.theme_cls
        # --------------------------------------------------------------------------------

        # 配置主题颜色----------------------------------------
        # ['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime', 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']
        self.theme_cls.primary_palette = config.config["theme_cls_primary_palette"]
        self.theme_cls.accent_palette = config.config["theme_cls_accent_palette"]
        # --------------------------------------------------------------------------------

        # 界面管理----------------------------------------
        self.screen_manager = ScreenManager()
        self.screen_list = []
        self.main_page = None  # 界面切换界面
        self.record_page = None  # 记录界面
        self.user_page = None  # 用户界面
        self.home_page = None  # 主界面
        self.study_page = None  # 学习界面
        self.detail_page = None  # 详情界面
        self.finishpage = None #学习结束页面
        self.challengepage = None #挑战界面
        self.firstpage = None #第一次使用时输入用户名界面
        self.loading_page = Loading(name="loading")  # 加载页面
        self.screen_manager.add_widget(self.loading_page)
        self.snackbar = Snackbar(duration=1.5)  # 提示窗
        # --------------------------------------------------------------------------------

        # 加载初始页面
        KV_MainPage = open("main.kv", "r", encoding="utf-8").read()
        self.main_page = Builder.load_string(KV_MainPage)

        for i in self.main_page.ids.buttom.ids.tab_manager.screens:
            # i.size_hint = (1, 1)
            i.pos = (0, self.main_page.ids.buttom.ids.tab_bar.height)

        

        self.Home()
        self.main_page.ids.buttom.switch_tab("home")

        self.screen_manager.add_widget(self.main_page)
        self.screen_list.append(self.main_page)
        self.screen_manager.current = "Main"

        if not config_dict["ID"]:
            print(config_dict)
            self.FirstInit()


        return self.screen_manager

    def Home(self):
        # 构造Home界面
        if not self.home_page:
            self.home_page = Home()
            self.main_page.ids.home.add_widget(self.home_page)
        self.home_page.Refresh()

    def User(self):
        # 构造User界面
        if not self.user_page:
            self.user_page = User()
            self.user_page.username = config_dict["username"]
            self.main_page.ids.user.add_widget(self.user_page)
        print(self.user_page.username)

    def Record(self):
        if not self.record_page:
            self.record_page = Record()
            self.main_page.ids.record.add_widget(self.record_page)

    def StartStudy(self):
        if not self.study_page:
            if self.home_page.now_choose != "未选择学习类别":
                self.screen_manager.current = self.loading_page.name
                #def __start():
                self.study_page = StudyPage(self.home_page.now_choose, name = "studypage")
                self.screen_list.append(self.study_page)
                self.screen_manager.add_widget(self.study_page)
                self.screen_manager.current = "studypage"

                #threading.Thread(target=__start).start()

            else:
                self.snackbar.text = "当前未选择学习类别"
                self.snackbar.show()

    def FinishStudy(self):
        '''
        说明: 重StudyPage切回主界面
        args{
            
        }
        return: 
        '''
        
        if self.study_page:
            self.screen_list.remove(self.study_page)
            if self.study_page.has_answer:
                self.ShowFinishPage(self.study_page.contents)
            else:
                self.screen_manager.current = self.main_page.name
            self.screen_manager.remove_widget(self.study_page)
            del self.study_page
            self.study_page = None
            self.home_page.Refresh()

    def StartChallenge(self):
        if not self.challengepage:
            self.screen_manager.current = self.loading_page.name
            #def __start():
            self.challengepage = Challenge(name = "challengepage")
            self.screen_list.append(self.challengepage)
            self.screen_manager.add_widget(self.challengepage)
            self.screen_manager.current = "challengepage"
            #threading.Thread(target= __start).start()
    
    def BackChallenge(self):
        if self.challengepage:
            self.screen_list.remove(self.challengepage)
            self.screen_manager.current = self.main_page.name
            self.screen_manager.remove_widget(self.challengepage)
            del self.challengepage
            self.challengepage = None

    def FinishChallenge(self):
        '''
        说明: 从ChallengePage切回主界面
        args{
            
        }
        return: 
        '''
        
        if self.challengepage:
            self.screen_list.remove(self.challengepage)
            self.ShowFinishPage(self.challengepage.contents)
            self.screen_manager.remove_widget(self.challengepage)
            del self.challengepage
            self.challengepage = None 

    def ShowFinishPage(self, contents):
        if not self.finishpage:
            self.screen_manager.current = self.loading_page.name
            #def __start():
            self.finishpage = FinishPage(contents, name = "finish")
            self.screen_list.append(self.finishpage)
            self.screen_manager.add_widget(self.finishpage)
            self.screen_manager.current = "finish"
            #threading.Thread(target=__start).start()

    def ColseFinishPage(self):
        if self.finishpage:
            self.screen_list.remove(self.finishpage)
            self.home_page.Refresh()
            self.screen_manager.current = self.main_page.name
            self.screen_manager.remove_widget(self.finishpage)
            del self.finishpage
            self.finishpage = None
            
    def ShowDetail(self, content):
        if content and not self.detail_page:
            self.screen_manager.current = self.loading_page.name
            self.detail_page = Detail(content, name="detail")
            self.screen_manager.add_widget(self.detail_page)
            self.screen_list.append(self.detail_page)
            self.screen_manager.current = "detail"

    def CloseDetail(self):
        if self.detail_page:
            self.screen_list.remove(self.detail_page)
            self.screen_manager.current = self.screen_list[-1].name
            self.screen_manager.remove_widget(self.detail_page)
            del self.detail_page
            self.detail_page = None

    def FirstInit(self, text = "输入用户名后开始学习"):
        if not self.firstpage:
            self.firstpage = FirstInit(name = "First",hint_text=text, back_event=self.ChangeUsername)
            self.screen_manager.add_widget(self.firstpage)
            self.screen_list.append(self.firstpage)
            self.screen_manager.current = "First"
    
    def ChangeUsername(self, name):

        if not config_dict["ID"]:
            def s(req, result):
                json_data = result
                data = json.loads(json_data)
                if data["id"]:
                    config_dict["ID"] = data["id"]
                config_dict["username"] = name
                config.SaveConfig()
                self.CloseFirstPage()
            UrlRequest(server_url + "/register/?username={}".format(name), s)
        else:
            def s(req, result):
                json_data = result
                config_dict["username"] = name
                data = json.loads(json_data)
                print(data)
                config.SaveConfig()
                self.CloseFirstPage()
            UrlRequest(server_url + "/update/?id={}&username={}".format(config_dict["ID"], name), s)

    def CloseFirstPage(self):
        if self.firstpage:
            self.screen_list.remove(self.firstpage)
            self.screen_manager.current = self.main_page.name
            self.screen_manager.remove_widget(self.firstpage)
            del self.firstpage
            self.firstpage = None

    def BackEvent(self, window, key, *args):
        # 按下返回键事件
        
        t = time()
        if key == 27:
            print(t, "-", self.last_time, "-", t - self.last_time)
            if t - self.last_time < 2:
                self.stop()
                
            else:
                self.last_time = t
                self.snackbar.text = "按两次返回键退出"
                self.snackbar.show()
                return True

import bugs
bugs.fixBugs()#在app运行前添加这两条语句
ChengYu().run()