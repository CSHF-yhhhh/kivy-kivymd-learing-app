from random import randint
import threading
from kivy.lang import Builder

from kivy.uix.screenmanager import Screen
from kivymd.uix.snackbar import Snackbar
from kivy.uix.button import Button
from kivy.properties import StringProperty, ColorProperty

from AppData import appdata
from Config import config_dict,config

from Challenge.MazeCreate import Map

KV_Challenge = open("./Challenge/Challenge.kv", "r", encoding="utf-8").read()
Builder.load_string(KV_Challenge)


class ClickButton(Button):
    bg_color = ColorProperty()
    mypos = [0, 0]

class Challenge(Screen):
    click_color = ColorProperty()
    unclick_color = ColorProperty()
    user_answer = StringProperty()
    last_color = ColorProperty()
    win = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max_len = int(config_dict["difficulty"]) * 4 + 1
        print("Challenge: ", self.max_len)
        self.answer = ""
        self.flag = True
        self.contents = dict()
        self.last_click = []
        self.pos_list = []
        self.snackbar = Snackbar(duration = 0.8)#提示窗
        
        while len(self.answer) < self.max_len:
            appdata.ChangeSheet(
                "user_"
                + config_dict["all_category"][
                    randint(0, len(config_dict["all_category"]) - 1)
                ]
            )
            contents = appdata.MergeData(appdata.SelectIndex(1), appdata.SelectRand(1))

            for index, content in contents.items():
                if content["内容"] not in self.contents:
                    content["has_answer"] = 1
                    self.contents[content["内容"]] = content
                    self.answer += content["内容"]

        self.map, self.true_way = Map().CreateMaze(self.answer, 9)
        print(self.true_way)
        self.Refresh()
        
    def CheckAnswer(self, btn):
        #回答按钮点击事件,btn为产生事件的按钮对象
        if self.flag:
            self.flag = False
        else:
            return
        if len(self.last_click):
            if self.last_click[-1].mypos == btn.mypos:#点击的是最后一个按钮
                self.last_click.pop()
                self.pos_list.remove(btn.mypos)
                if len(self.last_click):
                    self.last_click[-1].bg_color = self.last_color
                btn.bg_color = self.unclick_color
                self.user_answer = self.user_answer[:-1]
            elif btn.mypos in self.pos_list:
                if not self.snackbar.parent:
                    self.snackbar.text = "已经点击过该按钮"
                    self.snackbar.show()
            elif abs(self.last_click[-1].mypos[0] - btn.mypos[0]) + abs(self.last_click[-1].mypos[1] - btn.mypos[1]) == 1:#点击的是周围的按钮
                new_color = []
                t = len(self.last_click)
                for i in range(3):
                    new_color.append(self.click_color[i] - 0.005 * t)
                new_color.append(1)

                self.last_click[-1].bg_color = new_color
                self.last_click.append(btn)
                self.pos_list.append(btn.mypos)
                btn.bg_color = self.last_color
                self.user_answer += btn.text
            else:
                if not self.snackbar.parent:
                    self.snackbar.text = "请点击上一个点击周围的按钮"
                    self.snackbar.show()
        else:
            self.last_click.append(btn)
            self.pos_list.append(btn.mypos)
            btn.bg_color = self.last_color
            self.user_answer += btn.text
        if len(self.user_answer) < len(self.answer):
            #未回答完
            pass
        elif self.answer == self.user_answer:
            #回答正确
            print("righr")
            self.ids.righr_answer_btn.text = "点此查看相关信息"
            self.snackbar.text = "回答正确"
            self.snackbar.show()
            return
        else:
            #回答错误
            if not self.snackbar.parent:
                self.snackbar.text = "回答错误"
                self.snackbar.show()
        self.flag = True
    
    def Refresh(self):
        #self.ids.grid.clear_widgets()
        i = 0
        for line in self.map:
            j = 0
            for word in line:
                self.ids["pos_{}_{}".format(i,j)].text = word
                self.ids["pos_{}_{}".format(i,j)].bg_color = self.unclick_color
                #btn = ClickButton(text = word, size_hint = (0.1, 0.1), on_release = self.CheckAnswer)#这里是动态生成的控件
                #btn.mypos = [i, j]
                #self.ids.grid.add_widget(btn)
                j += 1
            i += 1
        self.pos_list.clear()
        self.last_click.clear()
        self.last_click.clear()
        self.user_answer = ""
        self.ids.righr_answer_btn.text = "查看正确答案"
        self.flag = True


    def ShowTrueWay(self):
        if self.flag:
            self.Refresh()
            for pos in self.true_way:
                self.CheckAnswer(self.ids["pos_{}_{}".format(pos[0],pos[1])])
        else:
            self.win()
