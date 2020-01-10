import pymysql
from scrapy.exceptions import DropItem

from movieInfoSpider import settings, items
import hashlib


class CommentItemPipeline(object):
    def __init__(self):
        # connect to database mysql

        self.connect = pymysql.Connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWORD,
            charset=settings.MYSQL_CHARSET,
        )
        self.cursor = self.connect.cursor()



    def close_spider(self, spider):
        self.connect.close()

    def process_item(self, item, spider):
        if isinstance(item, items.Comment):
            self._insert_comment(item)
            raise DropItem('Has Done')
        return item

    def _insert_comment(self, item):
        print(type(item['rate']))
        print(type(item['votes']))
        print(item['votes'])

        sql = 'insert into spider.comment(user_id,movie_id,rate,votes,content,date) ' \
              'value (%s,%s,%s,%s,%s,%s)'
        self.cursor.execute(sql, (
            item['user_id'],
            item['movie_id'],
            item['rate'],
            item['votes'],
            item['content'],
            item['date']
        ))
        self.connect.commit()

