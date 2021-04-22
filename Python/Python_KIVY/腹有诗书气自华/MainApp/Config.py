# -*- encoding: utf-8 -*-
'''
@文件:Config.py
@说明:配置文件
{
    theme_cls_primary_palette=Amber
    text_font=./zushi.ttf
    widget_font=./siyuan.ttf
    widget_name=./siyuan.ttf
    choose_category=
    all_category=小学成语,常用成语,
    max_learn=10
}
'''

import time
from calendar import Calendar


default_config ='''theme_cls_primary_palette=Brown
theme_cls_accent_palette=Blue
choose_category=
all_category=小学成语,常用成语,
max_learn=10
difficulty=1
ID=
username=
'''


class Config():
    def __init__(self):
        self.config = {}
        self.record = {}
        self.time_show = "%Y-%m-%d"
        self.font = None #app的字体列表
        self.theme_cls = None#app的颜色类
        self.ReadConfig()
        self.ReadRecord()
    
    def ReadConfig(self):
        try:
            config_file = open("./config.dat","r",encoding="utf-8")
            config = config_file.read().split("\n")
            while '' in config:
                config.remove('')
            for line in config:
                config = line.split("=")
                if len(config) == 1:
                    config.append(None)
                if config[0] in ['all_category']:
                    if config[1]:
                        config[1] = config[1].split(',')
                        try:
                            config[1].remove('')
                        except:
                            pass
                    else:
                        config[1] = list()
                if config[0] in ['max_learn']:
                    config[1] = int(config[1])
                self.config[config[0]] = config[1]
                
            #print("Config: ", self.config)
        except FileNotFoundError:
            config_file = open("./config.dat","w",encoding="utf-8")
            config_file.write(default_config)
            config_file.close()
            self.ReadConfig()
        except Exception as e:
            print("[{}][Error] {}".format(self.__class__,e))
            raise(e)

    def ReadRecord(self):
        try:
            record_file = open("./record.dat","r",encoding="utf-8")
            record = record_file.read().split("\n")
            while "" in record:
                record.remove('')
            for line in record:
                record = line.split("=")
                if len(record) == 1:
                    record.append(None)
                self.record[record[0]] = int(record[1])
                
            #print("Record: ", self.record)
        except FileNotFoundError:
            record_file = open("./record.dat","w",encoding="utf-8")
            record_file.close()
            self.ReadRecord()
        except Exception as e:
            print("[{}][Error] {}".format(self.__class__,e))
            raise(e)
    
    def SaveConfig(self):
        config = ''
        for key in self.config:
            if key in ['all_category']:
                c = ''
                for cc in self.config[key]:
                    c += cc + ','
            else:
                c = self.config[key]
            config += "{}={}\n".format(key, c if c else '')
        config_file = open("./config.dat","w",encoding="utf-8")
        config_file.write(config)
        config_file.close()

    def SaveRecord(self, record = None):
        '''
        先得到今天的日期,然后在与最后一行的日期做比较,相同则+1,不相同则添加
        '''
        if record:
            now = self.Today()
            if now in self.record:
                self.record[now] += record
            else:
                self.record[now] = record
        record_str = ''
        for key in self.record:
            line = "{}={}\n".format(key, self.record[key])
            record_str += line
        record_file = open("./record.dat","w",encoding="utf-8")
        record_file.write(record_str)
        record_file.close()
    def Yesterday(self):
        return time.strftime(self.time_show, time.localtime(time.time() - 24*60*60))

    def Today(self):
        return time.strftime(self.time_show, time.localtime())
    
    def GetRecord(self, year, month):
        '''
        mode: 获得year年month月的数据
        '''

        result = {}
        calendar = Calendar(firstweekday=7)
        now_time = time.localtime()
        now_year = now_time.tm_year
        now_month = now_time.tm_mon
        now_month_day = now_time.tm_mday
        all_week = calendar.monthdayscalendar(year= year, month=month)
        #print(all_week)

        for week in all_week:
            if 0 in week:#清空日期为0的
                while 0 in week:
                    week.remove(0)
            #将日期格式转化为目标格式
            for day in week:
                if year >= now_year and month >= now_month and day > now_month_day:
                    return result
                day_str = "%d-%02d-%02d"%(year, month, day)
                
                if day_str in self.record:
                    result["%d月%d日"%(month, day)] = self.record[day_str]
                else:
                    result["%d月%d日"%(month, day)] = 0
        return result


config = Config()
config_dict = config.config
record_dict = config.record
if __name__ == "__main__":
    print(config_dict)
    #c.config['theme_cls_primary_palette'] = '123'
    #c.config['widget_name'] = './siyuan.ttf'
    #c.SaveConfig()
    #print(c.GetRecord(2021,1))

    '''
    f = open("./record.dat","w",encoding="utf-8")
    calendar = Calendar(firstweekday=7)
    i = 0
    for month in range(1, 13):
        for week in calendar.monthdayscalendar(2021,month):
            for day in week:
                if day != 0:
                    s = "%d-%02d-%02d=%d\n"%(2021, month, day, i)
                    f.write(s)
                    i += 1 
    f.close()
    '''
