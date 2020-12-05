import pymysql

host = 'localhost'
port = 3306
user = 'root'
passwd = 'root'
db = 'dbo'
sql = 'select ProductUrl from spiderproductcrawltasks'


class SelectMySQL():

    def __init__(self):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db

    def select_data(self, sql):
        conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db)
        cursor = conn.cursor()
        global effect_row
        effect_row = cursor.execute(sql)
        result = cursor.fetchall()
        new_result = list(result)
        for t_new_result in new_result:
            with open('products.json', 'a+', encoding='utf-8') as f:
                f.write(str(t_new_result[0]))

        conn.commit()
        conn.close()


s = SelectMySQL()
s.select_data(sql)
