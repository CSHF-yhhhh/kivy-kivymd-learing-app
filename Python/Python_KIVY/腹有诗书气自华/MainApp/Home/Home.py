# -*- encoding: utf-8 -*-
"""
@文件:Home.py
@说明:Home页面,
"""

import threading
from kivy.lang import Builder

from kivy.uix.screenmanager import ScreenManager
from Home.SwitchContainer import SwitchContainer

from kivymd.uix.list import TwoLineListItem
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarIconListItem

from kivy.properties import StringProperty, NumericProperty

from random import randint


from Config import config_dict, config, record_dict
from AppData import appdata

# 加载KV
KV_Home = open("./Home/Home.kv", "r", encoding="utf-8").read()
Builder.load_string(KV_Home)


class ItemConfirm(OneLineAvatarIconListItem):
    divider = None

    def __init__(self, active=False, **kwargs):
        super().__init__(**kwargs)
        self.ids.check.active = active

    def set_icon(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False


class MyTwoLine(TwoLineListItem):
    text_one = StringProperty()
    text_two = StringProperty()

    def __init__(self, content, **kwargs):
        self.content = content
        self.text_one = content["内容"] if content["内容"] else ""
        self.text_two = content["含义"] if content["含义"] else ""
        super().__init__(**kwargs)


class Home(ScreenManager):
    now_choose = StringProperty("未选择学习类别")  # 当前的学习类别
    total_num = NumericProperty(0)  # 总的学习内容个数
    has_study_num = NumericProperty(0)  # 已经学习的内容个数
    yesterday_num = NumericProperty(0)  # 昨日学习个数
    today_num = NumericProperty(0)  # 今日学习个数
    need_learn = NumericProperty(0)  # 需要学习的个数

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        appdata.IsInit()
        self.choose_category = (
            config_dict["choose_category"]
            if config_dict["choose_category"]
            else "未选择学习类别"
        )
        
        self.ChangeCategory()
        # 构建弹窗
        items = []
        for category in config_dict["all_category"]:
            items.append(
                ItemConfirm(
                    active=(category == config_dict["choose_category"]),
                    text=category,
                    on_release=self.CategorySelected,
                )
            )
        self.choose_category_dialog = MDDialog(
            size_hint=(0.9, None),
            title="选择学习类别",
            type="confirmation",
            items=items,
            buttons=[
                MDFlatButton(
                    text="取消",
                    text_color=config.theme_cls.primary_color,
                    on_release=lambda x: self.choose_category_dialog.dismiss(),
                ),
                MDFlatButton(
                    text="确定",
                    text_color=config.theme_cls.primary_color,
                    on_release=lambda x: (
                        self.choose_category_dialog.dismiss(),
                        self.ChangeCategory(),
                    ),
                ),
            ],
        )
        self.choose_category_dialog.set_normal_height()
        self.need_learn = (
            config_dict["max_learn"] - self.today_num
            if config_dict["max_learn"] - self.today_num > 0
            else 0
        )

        self.GetSwitch()

    def SetValue(self, **kw):
        """
        说明: 界面接口,修改界面显示内容
        args{
            now_choose: 学习类别(标题)
            total_num: 总的学习内容个数
            has_study_num: 已经学习的内容个数
            yesterday_num: 昨日学习内容个数
            today_num: 今日学习个数
        }
        return:
        """
        for key, value in kw.items():
            if key == "now_choose":
                self.now_choose = value
            elif key == "total_num":
                self.total_num = value
                self.process_value = (self.has_study_num / self.total_num) * 100
            elif key == "has_study_num":
                self.has_study_num = value
                self.process_value = (value / self.total_num) * 100
            elif key == "yesterday_num":
                self.yesterday_num = value
            elif key == "today_num":
                self.today_num = value
                self.need_learn = (
                    config_dict["max_learn"] - self.today_num
                    if config_dict["max_learn"] - self.today_num > 0
                    else 0
                )

    def GetSwitch(self):
        # 构造轮播图内容
        self.ids.switch.DeleteAll()
        max_table = len(config_dict["all_category"])

        if max_table:
            self.contents = {}  # 存储学习内容
            used = []
            for i in range(5):
                appdata.ChangeSheet(
                    config_dict["all_category"][randint(0, max_table - 1)],
                )
                content = appdata.MergeData(
                    appdata.SelectIndex(), appdata.SelectRand(1)
                )
                if len(content):
                    for index, c in content.items():
                        if c["内容"] not in used:
                            widget = MyTwoLine(c)
                            self.ids.switch.AddPage(c["内容"], widget)
                            used.append(c["内容"])
        else:
            widget = MDLabel(text="未选择学习类别", font_style="H6", halign="center")
            self.ids.switch.AddPage("未选择学习类别", widget)

    def ChanegCategory_DialogOpen(self):
        """
        说明: 打开选择学习类型的弹窗
        args{

        }
        return:
        """

        self.choose_category_dialog.open()

    def CategorySelected(self, instance):
        """
        说明: 选择学习类别中列表条目响应事件
        args{

        }
        return:
        """

        self.choose_category = instance.text
        print(self.choose_category)

    def ChangeCategory(self):
        """
        说明: 改变当前学习类别,将self.choose_category赋值给self.now_choose
        args{

        }
        return:
        """
        if self.choose_category:
            # 修改数据并保存
            config_dict["choose_category"] = self.now_choose = self.choose_category
            config.SaveConfig()
            # --------------------------待完成
            self.Refresh()

    def Refresh(self):
        yesterday = config.Yesterday()
        yesterday_num = record_dict[yesterday] if yesterday in record_dict else 0
        today = config.Today()
        today_num = record_dict[today] if today in record_dict else 0
        if not appdata.ChangeSheet("user_" + self.now_choose):
            self.SetValue(yesterday_num = yesterday_num, today_num = today_num)
            return
        process = appdata.SelectIndex(2)[2:4]
        total_num, has_study_num = process
        total_num = int(total_num)
        has_study_num = int(has_study_num)
        if has_study_num > total_num:
            has_study_num = total_num
        
        self.SetValue(total_num = total_num, has_study_num = has_study_num, yesterday_num = yesterday_num, today_num = today_num)


    