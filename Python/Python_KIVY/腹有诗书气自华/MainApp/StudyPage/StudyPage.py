# -*- encoding: utf-8 -*-
"""
@文件:StudyPage.py
@说明: 
"""

import threading
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from kivy.uix.label import Label

from random import randint
from kivy.properties import NumericProperty, StringProperty, ColorProperty

from AppData import appdata
from Config import config, config_dict
from kivy.lang import Builder

KV_StudyPage = open("./StudyPage/StudyPage.kv", "r", encoding="utf-8").read()
Builder.load_string(KV_StudyPage)


class Question(Screen):
    """
    问题模块
    """
    text = StringProperty()
    cols = NumericProperty(2)  # 答案选项有几列


class AnswerButton(Label):
    """答案按钮类"""

    bg_color = ColorProperty()  # 背景颜色绑定的变量
    pic = StringProperty()
    fg_color = ColorProperty()  # 背景颜色绑定的变量

    def __init__(self, click_event, **kwargs):
        """
        说明:
        args{
            click_event: 控件点击事件
        }
        return:
        """

        super().__init__(**kwargs)
        self.click_event = click_event
        self.bg_color = config.theme_cls.primary_color
        self.fg_color = self.bg_color
        self.flag = True
        self.click_flag = False

    # 一下是方法的重构
    def on_touch_down(self, touch):
        """
        说明: 按下事件
        args{

        }
        return:
        """

        if self.collide_point(touch.x, touch.y):  # 判断是否点击的本控件
            self.fg_color = self.bg_color = config.theme_cls.primary_dark  # 改变背景颜色
            self.click_flag = True
        else:
            return super().on_touch_down(touch)  # 点击的不是本控件,返回事件继续递归

    def on_touch_up(self, touch):
        """
        说明: 松开事件
        args{

        }
        return:
        """

        if self.collide_point(touch.x, touch.y) and self.click_flag:  # 判断是否点击的本控件
            self.fg_color = self.bg_color = config.theme_cls.primary_color  # 改变背景颜色
            self.click_event(self)  # 如果点击的是本控件,则响应事件
        else:
            if self.click_flag:
                self.fg_color = self.bg_color = config.theme_cls.primary_color
                self.click_flag = False
            return super().on_touch_down(touch)  # 点击的不是本控件,返回事件继续递归

        
    
    def on_error_click(self):
        #回答错误事件
        if self.flag:
            self.flag = False
        else:
            return
        #self.bg_color = (0.95, 0.11, 0.11, 1)
        self.pic = "./appPicture/close.png"
        self.fg_color = (1,1,1,1)
        def change(*args):
            self.pic = ""
            #self.bg_color = config.theme_cls.primary_color
            self.fg_color = self.bg_color
            self.flag = True
        Clock.schedule_once(change, 0.5)
    



class StudyPage(Screen):
    last_answer = StringProperty()
    last_index = None
    back_event = None
    detail_event = None

    def __init__(self, category, **kwargs):
        """
        说明: 学习界面的初始化函数
        args{
            category: 选择的学习类别
        }
        return:
        """

        super().__init__(**kwargs)
        self.has_answer = 0
        appdata.ChangeSheet("user_" + category)  # 改变工作表
        # 获得数据
        max_row = appdata.MaxRow()

        self.contents = appdata.SelectWhere(
            where={"记录": 0}, num=config_dict["max_learn"]
        )

        while (
            len(self.contents) < config_dict["max_learn"]
            and len(self.contents) < max_row
        ):
            if config_dict["max_learn"] >= max_row:
                content = appdata.SelectRand(max_row)
            else:
                content = appdata.SelectRand(
                    config_dict["max_learn"] - len(self.contents)
                )
            for i in content:
                if i not in self.contents:
                    self.contents[i] = content[i]
        self.contents = appdata.MergeData(appdata.SelectIndex(index=1), self.contents)

        self.keys = list(self.contents.keys())
        self.no_answer = list(self.contents.keys())  #
        t = self.keys.copy()[::-1]
        i = 0
        for index in t:
            if i < 5:  # 最大界面数
                self.no_answer.remove(index)
                self.ids.show_list.add_widget(self.CrateQuestion(index))
                i += 1
            else:
                break

        self.right_answer = self.contents[int(self.ids.show_list.current)]["内容"]
        self.answer_false = 0

    def CrateQuestion(self, index):
        """
        说明: 生成问题界面
        args{
            index:为self.contents中的key值
        }
        return:
        """

        # 随机选择几个内容
        answer_list = list()
        answer_list.append(index)

        self.keys.remove(index)
        for i in range(3):
            answer_list.append(self.keys.pop(randint(0, len(self.keys) - 1)))
        for i in answer_list:
            self.keys.append(i)

        question = Question(name=str(index))  # 用正确答案的下标来作为标识
        question.cols = 2  # 设置答案行数

        question.text = text=self.contents[index]["含义"]
        while len(answer_list):
            question.ids.answer_box.add_widget(
                AnswerButton(
                    text=self.contents[
                        answer_list.pop(randint(0, len(answer_list) - 1))
                    ]["内容"],
                    size_hint=(0.5, 0.5),
                    click_event=self.Answer,
                )
            )
        return question

    def Answer(self, instance):
        """
        说明: 回答时间
        args{
            instance:事件产生的控件
        }
        return:
        """
        text = instance.text
        if text == self.right_answer:
            # 回答正确
            self.answer_false = 0
            def recoed(index, value):  # 这里的value是没有加一的
                value = int(value)
                if value == 0:
                    appdata.ChangeCellValue(2, 4, int(appdata.GetCellValue(2, 4)) + 1)
                appdata.ChangeCellValue(index, 1, int(value) + 1)
                config.SaveRecord(1)

            self.last_answer = text
            self.last_index = int(self.ids.show_list.current)
            self.contents[self.last_index]["has_answer"] = 1
            self.has_answer += 1
            threading.Thread(target=recoed, args=(self.last_index, self.contents[self.last_index]["记录"])).start()
            
            self.NextQuestion()  # 切换到下一个问题
        else:
            instance.on_error_click()
            question = self.ids.show_list.current_screen
            if question.text.find("\n") == -1:
                question.text += "\n[color=808080]{}[/color]".format(self.contents[int(question.name)]["拼音"])
            self.answer_false += 1
            if self.answer_false > 2:
                self.detail_event(self.contents[int(question.name)])

    def NextQuestion(self):
        """
        说明: 转换到下一个问题界面
        args{

        }
        return:
        """
        if len(self.ids.show_list.screen_names) == 1:  # 判断是否学习完毕

            self.back_event()
            return
        # 移除当前以回答的问题界面
        screen = self.ids.show_list.current_screen

        # 切换到下一个
        self.ids.show_list.current = self.ids.show_list.next()
        self.right_answer = self.contents[int(self.ids.show_list.current)][
            "内容"
        ]  # 并设置正确的答案
        self.ids.show_list.remove_widget(screen)

        def __add(screen):
            # 删除不需要的界面
            del screen
            # 如果还有更多就继续添加
            if len(self.no_answer):
                self.ids.show_list.add_widget(
                    self.CrateQuestion(self.no_answer.pop(0))
                )  # 生成并添加一个新的界面
        threading.Thread(target=__add, args=(screen,)).start()
