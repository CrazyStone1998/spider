import pymysql
from scrapy.exceptions import DropItem

from movieInfoSpider import settings, items


class OtherItemPipeline(object):
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
        if isinstance(item, items.User):
            self._insert_user(item)
            raise DropItem('Has Done')
        elif isinstance(item, items.Genre):
            self._insert_genre(item)
            raise DropItem('Has Done')
        elif isinstance(item, items.DirectorScreenwriter):
            self._insert_director_screenwriter(item)
            raise DropItem('Has Done')
        elif isinstance(item, items.Starring):
            self._insert_starring(item)
            raise DropItem('Has Done')
        elif isinstance(item, items.MovieGenreRelation):
            self._insert_movie_gener_relation(item)
            raise DropItem('Has Done')
        elif isinstance(item, items.MovieDirectorRelation):
            self._insert_movie_director_relation(item)
            raise DropItem('Has Done')
        elif isinstance(item, items.MovieScreenwriterRelation):
            self._insert_movie_screenwriter_relation(item)
            raise DropItem('Has Done')
        elif isinstance(item, items.MovieStarringRelation):
            self._insert_movie_starring_relation(item)
            raise DropItem('Has Done')
        else:
            return item

    def _insert_user(self, item):
        sql = 'insert into spider.user(id_douban,username,icon,url) ' \
              'value (%s,%s,%s,%s);'
        self.cursor.execute(sql, (
            item['id_douban'],
            item['username'],
            item['icon'],
            item['url']
        ))
        self.connect.commit()

    def _insert_genre(self, item):
        sql = 'insert into spider.genre(name) ' \
              'value (%s);'

        self.cursor.execute(sql, (
            item['name']
        ))
        self.connect.commit()

    def _insert_director_screenwriter(self, item):
        sql = 'insert into spider.director_screenwriter(is_director, is_screenwriter, name, url_douban) ' \
              'value (%s,%s,%s,%s);'
        self.cursor.execute(sql, (
            item['isDirector'],
            item['isScreenwriter'],
            item['name'],
            item['url_douban']
        ))
        self.connect.commit()

    def _insert_starring(self, item):
        sql = 'insert into spider.starring(name, url_douban) ' \
              'value (%s,%s);'
        self.cursor.execute(sql, (

            item['name'],
            item['url_douban'],

        ))
        self.connect.commit()

    def _insert_movie_gener_relation(self, item):
        sql = 'insert into spider.movie_genre_relation(genre, movie_id) ' \
              'value (%s,%s);'
        self.cursor.execute(sql, (
            item['genre'],
            item['movie_id']
        ))
        self.connect.commit()

    def _insert_movie_starring_relation(self, item):
        sql = 'insert into spider.movie_starring_relation(movie_id, starrring) ' \
              'value (%s,%s);'
        self.cursor.execute(sql, (
            item['movie_id'],
            item['starring']
        ))
        self.connect.commit()

    def _insert_movie_director_relation(self, item):
        sql = 'insert into spider.movie_director_relation(director, is_master, movie_id) ' \
              'value (%s,%s,%s);'
        self.cursor.execute(sql, (
            item['director'],
            True,
            item['movie_id']
        ))
        self.connect.commit()

    def _insert_movie_screenwriter_relation(self, item):
        sql = 'insert into spider.movie_screenwriter_relation(is_master, movie_id, screenwriter) ' \
              'value (%s,%s,%s);'
        self.cursor.execute(sql, (
            True,
            item['movie_id'],
            item['screenwriter']
        ))
        self.connect.commit()
