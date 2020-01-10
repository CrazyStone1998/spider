import pymysql
from scrapy.exceptions import DropItem

from movieInfoSpider import settings, items


class ReviewItemPipeline(object):
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
        if isinstance(item, items.Review):
            self._insert_review(item)
            raise DropItem('Has Done')
        return item


    def _insert_review(self, item):

        print(item['movie_id'])
        print(item['rate'])


        sql = 'insert into spider.review(content, date, movie_id, rate, title, user_id, votes) ' \
              'values (%s,%s,%s,%s,%s,%s,%s);'
        self.cursor.execute(sql, [
            item['content'],
            item['date'],
            item['movie_id'],
            item['rate'],
            item['title'],
            item['user_id'],
            item['votes']
        ])
        self.connect.commit()
