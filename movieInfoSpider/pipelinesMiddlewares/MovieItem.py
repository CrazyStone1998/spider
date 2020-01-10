import pymysql
from movieInfoSpider import settings
from movieInfoSpider import items


class MovieItemPipeline(object):

    def __init__(self):
        # connect to database mysql
        self.connect = pymysql.Connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passed=settings.MYSQL_PASSWORD,
            charset=settings.MYSQL_CHARSET,
        )
        self.cursor = self.connect.cursor()

    def close_spider(self, spider):
        self.connect.close()

    def process_item(self, item, spider):

        return item

    def _insert_movie(self, item):

        pass

