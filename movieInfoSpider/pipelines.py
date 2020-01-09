# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from movieInfoSpider import settings
from movieInfoSpider import items

from movieInfoSpider import settings


class MovieinfospiderPipeline(object):
    pass
    #
    # def __init__(self):
    #     # connect to database mysql
    #     self.connect = pymysql.connect(
    #         host=settings.MYSQL_HOST,
    #         db=settings.MYSQL_DBNAME,
    #         user=settings.MYSQL_USER,
    #         passed=settings.MYSQL_PASSWORD,
    #         charset=settings.MYSQL_CHARSET,
    #         use_unicode=True,
    #     )
    #
    #     self.cursor = self.connect.cursor()
    #
    # def _insert_movie(self, item):
    #     sql = 'insert into recommendsystem.movie' \
    #           '(name,' \
    #           'foreign_name,' \
    #           'area,' \
    #           'cover_url,' \
    #           'language,' \
    #           'length,' \
    #           'rate,' \
    #           'rate_num,' \
    #           'release_date,' \
    #           'url_douban,' \
    #           'url_imdb)'
    #     self.cursor.execute(sql, (
    #         item['name'],
    #         item['foreign_name'],
    #         item['area'],
    #         item['cover_url'],
    #         item['language'],
    #         item['length'],
    #         item['rate'],
    #         item['rate_num'],
    #         item['release_date'],
    #         item['url_douban'],
    #         item['url_imdb']
    #     ))
    #
    # def process_item(self, item, spider):
    #
    #     try:
    #         if isinstance(item, items.Movie):
    #             # 查重处理
    #             self.cursor.execute(
    #                 '''
    #                 select * from recommendsystem.movie
    #                 where name = %s;
    #                 ''',
    #                 item['name']
    #             )
    #
    #             # 是否有重复数据
    #             repetition = self.cursor.fetchone()
    #
    #             # 重复
    #             if repetition:
    #                 pass
    #             else:
    #                 # 插入数据
    #                 self._insert_movie(item)
    #                 self.connect.commit()
    #                 print('------------------------------------------------------------')
    #     except Exception as e:
    #         print(e)
    #     return item
    #
    # def close_spider(self, spider):
    #     self.connect.close()
