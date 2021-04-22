import pymysql


class DataBase():
    def __init__(self):
        self.conn = pymysql.connect(host='localhost',
            user='chengyu',
            passwd='cshf123456..',
            db='chengyu',
            port=3306,
            charset='utf8')

        self.cursor=self.conn.cursor()

        sql_init_table="""CREATE TABLE IF NOT EXISTS `user_date` (
            `id` bigint(20) NOT NULL AUTO_INCREMENT,
            `username` varchar(255) NOT NULL,
            `num` int(11) NOT NULL,
            PRIMARY KEY (`id`)
            ) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1"""
        self.cursor.execute(sql_init_table)
        self.conn.commit()

    def AddUser(self, username):
        add_user_sql = "insert into `user_date` (username, num) values('{}',0)".format(username)

        insert=self.cursor.execute(add_user_sql)
        last_id = self.cursor.lastrowid
        print('添加语句受影响的行数：',insert, last_id)
        self.conn.commit()
        return {"id":last_id, "username":username}

    def AlterNum(self, _id, num):
        
        update_user_sql = "update `user_date` set num={} where id={};".format(int(num), int(_id))
        insert=self.cursor.execute(update_user_sql)
        print('修改语句受影响的行数：',insert)
        self.conn.commit()
        return {"result" : True if insert else False}
    
    def AlterName(self, _id, name):
        
        update_user_sql = "update `user_date` set username='{}' where id={};".format(name, _id)
        insert=self.cursor.execute(update_user_sql)
        print('修改语句受影响的行数：',insert)
        self.conn.commit()
        return {"result" : True if insert else False}
    
    def GetTop(self, top = 2):
        select_user_sql = "select (@rowno:=@rowno+1) as rowno,`username`,`num`, `id` from `user_date`,(select (@rowno:=0)) b  order by num desc limit {};".format(top)
        self.cursor.execute(select_user_sql)
        results = dict()
        while True:
            result = self.cursor.fetchone()
            if result == None:
                break
            else:
                results[int(result[0])] = result[1:]
        return results
    
    def GetIdSort(self, _id):
        select_user_sql = "select rowno, username, num, id from (select `id`,(@rowno:=@rowno+1) as rowno,`username`,`num` from `user_date`,(select (@rowno:=0)) b order by num desc) t where id = {}".format(_id)
        self.cursor.execute(select_user_sql)

        results = dict()
        while True:
            result = self.cursor.fetchone()
            if result == None:
                break
            else:
                results[int(result[0])] = result[1:]
        return results
    def __del__(self):
        self.cursor.close()
        self.conn.commit()
        self.conn.close()

if __name__ == "__main__":
    
    database.AddUser("hahah")
    database.AlterNum(10,10)
    database.GetTop()
    database.GetIdSort(6)