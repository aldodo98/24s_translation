# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from Celine.items import CategoryTree
from Celine.spiders.product import ProductSpider


class CelinePipeline:

    def open_spider(self, spider):
        """
        该方法用于创建数据库连接池对象并连接数据库
        """
        db = spider.settings.get('MYSQL_DB_NAME', 'dbo')
        host = spider.settings.get('MYSQL_HOST', 'localhost')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER', 'root')
        passwd = spider.settings.get('MYSQL_PASSWORD', 'root')

        self.db_conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset='utf8')
        self.db_cur = self.db_conn.cursor()

    def close_spider(self, spider):
        """
        该方法用于数据插入以及关闭数据库
        """
        self.db_conn.commit()
        self.db_conn.close()

    def process_item(self, item, spider):
        if isinstance(spider, ProductSpider):
            return item
        if item.__class__ == CategoryTree:
            self.insert_tree(item)
        else:
            self.insert_tasks(item)

    def insert_tree(self, item):
        values = (
            item.get('Id'),
            item.get('CategoryLevel1'),
            item.get('CategoryLevel2'),
            item.get('CategoryLevel3'),
            item.get('CategoryLevel4'),
            item.get('CategoryLevel5'),
            item.get('Level_Url'),
            item.get('CreateDateTime'),
            item.get('UpdateDateTime'),
            item.get('ManufacturerId'),
            item.get('CategoryId'),
        )
        sql = 'INSERT INTO spidercategorytrees(' \
              'Id, CategoryLevel1,CategoryLevel2,CategoryLevel3, CategoryLevel4,CategoryLevel5,' \
              'Level_Url, CreateDateTime, UpdateDateTime,' \
              'ManufacturerId, CategoryId) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        self.db_cur.execute(sql, values)
        self.db_conn.commit()

    def insert_tasks(self, item):
        """
        sql语句构造方法
        """
        values = (
            item.get('Id'),
            item.get('CategoryTreeId'),
            item.get('ProductName'),
            item.get('ProductUrl'),
            item.get('Price'),
            item.get('Seconds'),
            item.get('Enabled'),
            item.get('Status'),
        )
        sql = 'INSERT INTO spiderproductcrawltasks(Id,CategoryTreeId,ProductName,ProductUrl,Price,Seconds,Enabled,Status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'
        self.db_cur.execute(sql, values)
        self.db_conn.commit()
