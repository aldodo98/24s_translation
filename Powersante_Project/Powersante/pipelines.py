# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from Powersante.items import CategoryTree
from Powersante.items import ProductInfo
from Powersante.items import Product
from scrapy_redis.pipelines import RedisPipeline
from Powersante.items import CategoryTree
# import pymysql

class RedisPipeline(RedisPipeline):

    def _process_item(self, item, spider):
        if item.__class__ == CategoryTree:
            hName = 'RootTaskSpider:TaskResult'
            hKey = item['Id']
            hValue = self.serialize(item)
            self.server.hset(name=hName, key=hKey, value=hValue)
            return item
        elif item.__class__ == ProductInfo:
            hName = 'GetTreeProductListTaskSpider:TaskResult'
            hKey = item['Id']
            hValue = self.serialize(item)
            self.server.hset(name=hName, key=hKey, value=hValue)
            return item
        elif item.__class__ == Product:
            hName = 'ProductTaskSpider:TaskResult'
            hKey = item['TaskId']
            hValue = self.serialize(item)
            self.server.hset(name=hName, key=hKey, value=hValue)
            return item

# class PowersantePipeline:
#
#     def open_spider(self, spider):
#         """
#         该方法用于创建数据库连接池对象并连接数据库
#         """
#         db = spider.settings.get('MYSQL_DB_NAME', 'dbo')
#         host = spider.settings.get('MYSQL_HOST', 'localhost')
#         port = spider.settings.get('MYSQL_PORT', 3306)
#         user = spider.settings.get('MYSQL_USER', 'root')
#         passwd = spider.settings.get('MYSQL_PASSWORD', 'root')
#
#         self.db_conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset='utf8')
#         self.db_cur = self.db_conn.cursor()
#
#     def close_spider(self, spider):
#         """
#         该方法用于数据插入以及关闭数据库
#         """
#         self.db_conn.commit()
#         self.db_conn.close()
#
#     def process_item(self, item, spider):
#         if item.__class__ == CategoryTree:
#             self.insert_tree(item)
#         else:
#             self.insert_tasks(item)
#
#     def insert_tree(self, item):
#         values = (
#             item.get('Id'),
#             item.get('CategoryLevel1'),
#             item.get('CategoryLevel2'),
#             item.get('CategoryLevel3'),
#             item.get('CategoryLevel4'),
#             item.get('CategoryLevel5'),
#             item.get('Level_Url'),
#             item.get('CategoryId'),
#             item.get('RootId'),
#             item.get('ProjectName')
#         )
#         sql = 'INSERT INTO spidercategorytrees(' \
#               'Id, CategoryLevel1,CategoryLevel2,CategoryLevel3, CategoryLevel4,CategoryLevel5,' \
#               'Level_Url, CategoryId, RootId, ProjectName) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
#         self.db_cur.execute(sql, values)
#         self.db_conn.commit()
#
#     def insert_tasks(self, item):
#         """
#         sql语句构造方法
#         """
#         values = (
#             item.get('Id'),
#             item.get('CategoryTreeId'),
#             item.get('ProductId'),
#             item.get('ProductName'),
#             item.get('ProductUrl'),
#             item.get('Price'),
#             item.get('ProjectName'),
#         )
#         sql = 'INSERT INTO spiderproductcrawltasks(Id,CategoryTreeId,ProductId,ProductName,ProductUrl,Price,ProjectName) VALUES(%s,%s,%s,%s,%s,%s,%s)'
#         self.db_cur.execute(sql, values)
#         self.db_conn.commit()
