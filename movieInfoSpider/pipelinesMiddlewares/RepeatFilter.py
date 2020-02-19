import hashlib

import json
from scrapy.exceptions import DropItem

from movieInfoSpider import settings, items


class RepeatFilterPipeline(object):
    def __init__(self):
        # connect to database mysql
        self.movie_set = set()
        self.user_set = set()
        self.genre_set = set()
        self.starring_set = set()
        self.directorscreenwriter_set = set()
        self.comment_set = set()
        self.review_set = set()

    def md5_utf8(self, str):
        m = hashlib.md5()
        m.update(str.encode("utf8"))
        return m.hexdigest()

    def close_spider(self, spider):
        pass
        # with open('Duplicate.txt', 'w', encoding='utf8') as f:
        #     f.write(json.dumps(list(self.movie_set)))

    def process_item(self, item, spider):
        if isinstance(item, items.Movie):
            key = self.md5_utf8(item['id_douban'])
            if key in self.movie_set:
                raise DropItem('Movie : %s Repeat !!!' % (item['name']))
            else:
                self.movie_set.add(key)

        elif isinstance(item, items.Comment):
            key = self.md5_utf8((item['user_id'] + item['movie_id']))
            if key in self.comment_set:
                raise DropItem('Comment : %s -> %s Repeat !!!' % (item['user_id'], item['movie_id']))
            else:
                self.comment_set.add(key)

        elif isinstance(item, items.Review):
            key = self.md5_utf8((item['user_id'] + item['movie_id']))
            if key in self.review_set:
                raise DropItem('Review : %s -> %s Repeat !!!' % (item['user_id'], item['movie_id']))
            else:
                self.review_set.add(key)
        elif isinstance(item, items.User):
            key = self.md5_utf8(item['id_douban'])
            if key in self.user_set:
                raise DropItem('User: %s !!!' % (item['id_douban']))
            else:
                self.user_set.add(key)

        elif isinstance(item, items.Starring):
            key = self.md5_utf8(item['name'])
            if key in self.starring_set:
                raise DropItem('Starring: %s !!!' % (item['name']))
            else:
                self.starring_set.add(key)

        elif isinstance(item, items.Genre):
            key = self.md5_utf8(item['name'])
            if key in self.genre_set:
                raise DropItem('Genre : %s Repeat !!!' % (item['name']))
            else:
                self.genre_set.add(key)

        # elif isinstance(item, items.DirectorScreenwriter):
        #     print('**********************************directorscreenwriter')
        #     print(item)
        # elif isinstance(item, items.MovieStarringRelation):
        #     print('******************************m s r')
        #     print(item)
        # elif isinstance(item, items.MovieDirectorRelation):
        #     print('************************m d r')
        #     print(item)
        # elif isinstance(item, items.MovieGenreRelation):
        #     print('****************************m g')
        #     print(item)
        return item
