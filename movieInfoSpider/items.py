# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class User(scrapy.Item):
    username = scrapy.Field()
    icon = scrapy.Field()
    url = scrapy.Field()
    id_douban = scrapy.Field()


class Movie(scrapy.Item):
    name = scrapy.Field()
    foreign_name = scrapy.Field()
    profile = scrapy.Field()
    length = scrapy.Field()
    language = scrapy.Field()
    area = scrapy.Field()
    release_date = scrapy.Field()
    rate = scrapy.Field()
    rate_num = scrapy.Field()
    weight = scrapy.Field()
    cover_url = scrapy.Field()
    id_douban = scrapy.Field()
    url_imdb = scrapy.Field()
    url_douban = scrapy.Field()


class DirectorScreenwriter(scrapy.Item):
    name = scrapy.Field()
    foreign_name = scrapy.Field()
    cover_url = scrapy.Field()
    isDirector = scrapy.Field()
    isScreenwriter = scrapy.Field()
    url_douban = scrapy.Field()
    url_imdb = scrapy.Field()


class MovieDirectorRelation(scrapy.Item):
    movie_id = scrapy.Field()
    url = scrapy.Field()
    director = scrapy.Field()
    ranking = scrapy.Field()


class MovieScreenwriterRelation(scrapy.Item):
    movie_id = scrapy.Field()
    url = scrapy.Field()
    screenwriter = scrapy.Field()
    ranking = scrapy.Field()


class Genre(scrapy.Item):
    name = scrapy.Field()
    foreign_name = scrapy.Field()
    description = scrapy.Field()


class MovieGenreRelation(scrapy.Item):
    movie_id = scrapy.Field()
    genre = scrapy.Field()


class Starring(scrapy.Item):
    name = scrapy.Field()
    foreign_name = scrapy.Field()
    cover_url = scrapy.Field()
    url_douban = scrapy.Field()
    url_imdb = scrapy.Field()


class MovieStarringRelation(scrapy.Item):
    ranking = scrapy.Field()
    url = scrapy.Field()
    movie_id = scrapy.Field()
    starring = scrapy.Field()


class Comment(scrapy.Item):
    user_id = scrapy.Field()
    movie_id = scrapy.Field()
    rate = scrapy.Field()
    content = scrapy.Field()
    date = scrapy.Field()
    votes = scrapy.Field()


class Review(scrapy.Item):
    user_id = scrapy.Field()
    movie_id = scrapy.Field()
    rate = scrapy.Field()
    content = scrapy.Field()
    votes = scrapy.Field()
    date = scrapy.Field()
    title = scrapy.Field()
