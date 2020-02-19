import pymysql
from movieInfoSpider import settings
from movieInfoSpider import items
from scrapy.exceptions import DropItem

class MovieItemPipeline(object):

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
        if isinstance(item, items.Movie):
            self._insert_movie(item)
            raise DropItem('Has Done')
        return item

    def _insert_movie(self, item):
        print('插入movie\n', item)
        sql = 'insert into movie' \
              '(name,area,cover_url,language,length,rate,rate_num,release_date,url_douban,url_imdb,id_douban,weight) ' \
              'value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
        self.cursor.execute(sql, (
            item['name'],
            item['area'],
            item['cover_url'],
            item['language'],
            item['length'],
            item['rate'],
            item['rate_num'],
            item['release_date'],
            item['url_douban'],
            item['url_imdb'],
            item['id_douban'],
            item['weight']
        ))
        self.connect.commit()
