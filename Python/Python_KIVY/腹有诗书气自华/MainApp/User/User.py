# -*- encoding: utf-8 -*-
"""
@文件:User.py
@说明: 用户界面
"""

from kivy.lang import Builder

from kivy.uix.screenmanager import ScreenManager
#from kivymd.uix.picker import MDThemePicker
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.boxlayout import BoxLayout

from kivy.properties import StringProperty, NumericProperty


from Config import config_dict, config
from AppData import appdata

import threading

KV_User = open("./User/User.kv", "r", encoding="utf-8").read()
Builder.load_string(KV_User)
""" OneLineListItem:
    bg_color: (1, 1, 1, 1)
    text: "主题颜色搭配设置"
    on_release: root.ChangeThemeColor()
    text_color: app.theme_cls.primary_color
    theme_text_color: "Custom" """

class StudyNum(BoxLayout):
    num = NumericProperty(0)
    def __init__(self,step = 1,max = 999,min = 0,now = 0, **kwargs):
        super().__init__(**kwargs)
        self.num = now if now else min
        self.step = step
        self.max = max
        self.min = min
    def add(self):
        if self.num + self.step <= self.max:
            self.num += self.step
    def sub(self):
        if self.num - self.step >= self.min:
            self.num -= self.step

class User(ScreenManager):
    color = StringProperty()
    accent_palette = StringProperty()
    radius = NumericProperty()
    refresh_home = None
    username = config_dict["username"]
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username = config_dict["username"]
        self.snackbar = Snackbar(duration=1.5)  # 提示窗
        self.dialog = MDDialog(
            size_hint_x=0.8,
            text="确定清除全部由学习记录?",
            buttons=[
                MDFlatButton(
                    text="取消",
                    text_color=config.theme_cls.primary_color,
                    on_release=lambda x: (self.dialog.dismiss()),
                ),
                MDFlatButton(
                    text="确定",
                    text_color=config.theme_cls.primary_color,
                    on_release=lambda x: (
                        self.ClearStudyProcess(),
                        self.dialog.dismiss(),
                    ),
                ),
            ],
        )
        self.dialog.set_normal_height()
        self.studynum = StudyNum(max= 999, min = 5, step=5, now = config_dict["max_learn"])
        self.study_num_dialog = MDDialog(
            size_hint_x=0.9,
            title="每日学习数量",
            type="custom",
            content_cls=self.studynum,
            buttons=[
                MDFlatButton(
                    text="取消",text_color=config.theme_cls.primary_color,on_release=lambda x: (self.study_num_dialog.dismiss()),
                ),
                MDFlatButton(
                    text="确定",text_color=config.theme_cls.primary_color,on_release=lambda x: (
                        self.ChangeStudyNum(),
                    ),
                ),
            ],
        )
        self.study_num_dialog.set_normal_height()

        self.difficulty = StudyNum(step=1, max = 6, min = 1, now = config_dict["difficulty"])
        self.difficulty_dialog = MDDialog(
            size_hint_x=0.9,
            title="挑战难度",
            type="custom",
            content_cls=self.difficulty,
            buttons=[
                MDFlatButton(
                    text="取消",text_color=config.theme_cls.primary_color,on_release=lambda x: (self.difficulty_dialog.dismiss()),
                ),
                MDFlatButton(
                    text="确定",text_color=config.theme_cls.primary_color,on_release=lambda x: (
                        self.ChangeDifficulty(),
                    ),
                ),
            ],
        )
        self.difficulty_dialog.set_normal_height()

        """ self.theme_dialog = MDThemePicker()
        self.theme_dialog.ids.title.text = "主题颜色搭配"
        self.theme_dialog.ids.theme_tab.text = "主题色"
        self.theme_dialog.ids.accent_tab.text = "选中色"
        self.theme_dialog.ids.close_button.text = "保存"
        self.theme_dialog.ids.close_button.on_release = lambda :(self.theme_dialog.dismiss(), self.SaveThemeColor()) """

        """ # 移除色调选择
        self.theme_dialog.ids.tab_panel.tab_bar.layout.remove_widget(
            self.theme_dialog.ids.style_tab.tab_label
        )
        self.theme_dialog.ids.tab_panel.carousel.remove_widget(
            self.theme_dialog.ids.style_tab
        ) """

    def ChangeDifficulty(self):
        num = self.difficulty.num
        print("ChangeDifficulty", num)
        config_dict["difficulty"] = int(num)
        config.SaveConfig()
        self.difficulty_dialog.dismiss()
        self.snackbar.text = "修改挑战难度成功"
        self.snackbar.show()

    def ChangeStudyNum(self):
        text = self.studynum.num
        print("ChangeStudyNum", text)
        if text > 0:
            config_dict["max_learn"] = int(text)
            config.SaveConfig()
            self.refresh_home()
            self.study_num_dialog.dismiss()
            self.snackbar.text = "修改每日学习数量成功"
            self.snackbar.show()
        else:
            self.studynum.ids.input.hint_text = "每日学习个数必须大于0!"
            self.studynum.ids.input.text = ""
            self.studynum.ids.input.error = True

    """ def ChangeThemeColor(self):
        self.theme_dialog.open() """

    def SaveThemeColor(self):#保存主题颜色设置
        config_dict["theme_cls_primary_palette"] = self.color
        config_dict["theme_cls_accent_palette"] = self.accent_palette
        config.SaveConfig()

    def ClearStudyProcess(self):
        def __clear():
            appdata.IsInit(True)
            config.record.clear()
            config.SaveRecord()
            self.snackbar.text = "清除成功"
            self.snackbar.show()

        threading.Thread(target=__clear).start()
