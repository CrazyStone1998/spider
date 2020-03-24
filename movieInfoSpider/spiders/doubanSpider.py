# -*- coding: UTF-8 -*-
import time
import scrapy
import json
import emoji
from movieInfoSpider import items
from scrapy.http import Request
from movieInfoSpider.tools.selenium_tool import SeleniumLogin


class doubanSpider(scrapy.Spider):
    name = 'doubanSpider'

    header = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0'
    }
    cookies = {'push_noty_num': '0', 'ap_v': '0,6.0', 'push_doumail_num': '0', '_pk_ses.100001.8cb4': '*', '_pk_ref.100001.8cb4': '%5B%22%22%2C%22%22%2C1583157816%2C%22https%3A%2F%2Faccounts.douban.com%2Fpassport%2Flogin%3Fsource%3Dmovie%22%5D', 'ck': 'VN6a', '_pk_id.100001.8cb4': 'b40b6dfae7b62813.1583157816.1.1583157816.1583157816.', 'dbcl2': '"208735309:iA10aJYXbsA"', 'bid': 'MNLa-qjjnOY'}

    def start_requests(self):

        # status, self.cookies = SeleniumLogin().login_douban('18340018316', 'doubanspider')
        # print("cookies\n", self.cookies)
        # https://movie.douban.com/j/new_search_subjects?sort=R&range=0,10&tags=电影&start=0&genres=剧情
        # sort = U,T,S,R

        sort = ['U', 'T', 'S']

        genre = ['剧情', '喜剧', '动作', '爱情', '科幻', '动画', '悬疑', '惊悚',
                 '恐怖', '犯罪', '同性', '音乐', '歌舞', '传记', '历史', '战争',
                 '西部', '奇幻', '冒险', '灾难', '武侠', '情色', ]
        starter_douban = 'https://movie.douban.com/j/new_search_subjects?sort={sort}&range=0,10&tags=电影&start={num}&genres={genre}'

        yield scrapy.Request(
            url='https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=电影&start=0&genres=剧情',
            callback=self.parse,
            headers=self.header,
        )

        # for s in sort:
        #     for g in genre:
        #         for n in range(1):
        #             yield scrapy.Request(
        #                 url=starter_douban.format(sort=s, genre=g, num=n * 20),
        #                 callback=self.parse,
        #                 headers=self.header,
        #             )

    def parse(self, response):

        print('-----------------------------电影界面 获取json列表-----------------------------')

        result = json.loads(response.text)

        # yield Request(
        #     url='https://movie.douban.com/subject/25887288/',
        #     meta={'data': result['data'][0]},
        #     callback=self.parse_movie_index_douban,
        #     headers=self.header,
        #     cookies=self.cookies,
        # )

        for movie in result['data']:
            yield Request(
                url=movie['url'],
                meta={'data': movie},
                callback=self.parse_movie_index_douban,
                headers=self.header,
                cookies=self.cookies,
            )

    def parse_movie_index_douban(self, response):

        print('----------------------进入电影界面，解析短评入口、影评入口，储存movie，genre等item------------------------------------')

        movie = response.meta['data']
        info = response.xpath('//*[@id="info"]/span')
        url_director = list(zip(info[0].xpath('.//*[@class="attrs"]/a/@href').extract(),
                                info[0].xpath('.//*[@class="attrs"]/a/text()').extract()))
        url_screenwriter = list(zip(info[1].xpath('.//*[@class="attrs"]/a/@href').extract(),
                                    info[1].xpath('.//*[@class="attrs"]/a/text()').extract()))
        url_starring = list(zip(info[2].xpath('.//*[@class="attrs"]/a/@href').extract(),
                                info[2].xpath('.//*[@class="attrs"]/a/text()').extract()))
        weight = response.xpath('//*[@class="rating_per"]/text()').extract()
        genre = response.xpath('//*[@property="v:genre"]/text()').extract()
        release_date = response.xpath('//*[@property="v:initialReleaseDate"]/text()').extract()[0].split('(')[0]
        length = int(response.xpath('//*[@property="v:runtime"]/@content').extract_first())
        url_imdb = response.xpath('//*[contains(@href,"imdb")]/@href').extract_first()
        rating_people = response.xpath('//*[@property="v:votes"]/text()').extract_first()
        language = response.xpath('//*[@id="info"]/text()').extract()[7 + len(genre)][1:]
        area = response.xpath('//*[@id="info"]/text()').extract()[5 + len(genre)]
        profile = response.xpath('//*[@property="v:summary"]/text()').extract()

        item_movie = items.Movie()
        item_movie['name'] = movie.get('title')
        item_movie['profile'] = ''.join(profile)
        item_movie['length'] = length
        item_movie['language'] = language
        item_movie['area'] = area
        item_movie['release_date'] = release_date
        item_movie['rate'] = movie.get('rate')
        item_movie['rate_num'] = rating_people
        item_movie['weight'] = ','.join(weight)
        item_movie['cover_url'] = movie.get('cover')
        item_movie['url_imdb'] = url_imdb
        item_movie['url_douban'] = movie.get('url')
        item_movie['id_douban'] = movie.get('id')
        yield item_movie

        for each in genre:
            item_movie_genre_relation = items.MovieGenreRelation()
            item_movie_genre_relation['movie_id'] = movie.get('id')
            item_movie_genre_relation['genre'] = each
            yield item_movie_genre_relation

        dict_DirectorScreenwriter = {}
        for url, name in url_screenwriter:
            dict_DirectorScreenwriter[url] = [name, False, True]
        for url, name in url_director:
            if dict_DirectorScreenwriter.get(url, None):
                dict_DirectorScreenwriter[url][1] = True
            else:
                dict_DirectorScreenwriter[url] = [name, True, False]

        # save item_DirectorScreenwriter
        for key, value in dict_DirectorScreenwriter.items():
            item_DirectorScreenwriter = items.DirectorScreenwriter()
            item_DirectorScreenwriter['url_douban'] = 'https://movie.douban.com' + key
            item_DirectorScreenwriter['name'] = value[0]
            item_DirectorScreenwriter['isDirector'] = value[1]
            item_DirectorScreenwriter['isScreenwriter'] = value[2]
            yield item_DirectorScreenwriter

        # item_movie_director_relation
        for index, (url, name) in enumerate(url_director):
            item_movie_director_relation = items.MovieDirectorRelation()
            item_movie_director_relation['movie_id'] = movie['id']
            item_movie_director_relation['url'] = 'https://movie.douban.com' + url
            item_movie_director_relation['director'] = name
            item_movie_director_relation['ranking'] = index
            yield item_movie_director_relation

        # save item_movie_screenwriter_relation
        for index, (url, name) in enumerate(url_screenwriter):
            item_movie_screenwriter_relation = items.MovieScreenwriterRelation()
            item_movie_screenwriter_relation['movie_id'] = movie['id']
            item_movie_screenwriter_relation['url'] = 'https://movie.douban.com' + url
            item_movie_screenwriter_relation['screenwriter'] = name
            item_movie_screenwriter_relation['ranking'] = index
            yield item_movie_screenwriter_relation

        for index, (url, name) in enumerate(url_starring):
            item_starring = items.Starring()
            item_starring['url_douban'] = 'https://movie.douban.com' + url
            item_starring['name'] = name
            yield item_starring
            item_movie_starring_relation = items.MovieStarringRelation()
            item_movie_starring_relation['movie_id'] = movie['id']
            item_movie_starring_relation['starring'] = name
            item_movie_starring_relation['url'] = 'https://movie.douban.com' + url
            item_movie_starring_relation['ranking'] = index
            yield item_movie_starring_relation

        # 解析 短评
        # https://movie.douban.com/subject/6981153/comments?start=20&limit=20&sort=new_score&status=P

        comment_url = 'https://movie.douban.com/subject/{id}/comments?start={num}&limit=20&sort=new_score&status=P'

        # yield Request(
        #     url=comment_url.format(id=movie.get('id'), num=0),
        #     meta={'movie': movie},
        #     callback=self.parse_movie_comment_douban,
        #     headers=self.header,
        #     cookies=self.cookies,
        # )

        for page in range(10):
            yield Request(
                url=comment_url.format(id=movie.get('id'), num=page * 20),
                meta={'movie': movie},
                callback=self.parse_movie_comment_douban,
                headers=self.header,
                cookies=self.cookies,
            )

        # 　解析　长评
        review_url = 'https://movie.douban.com/subject/{id}/reviews?start={num}'

        # yield Request(
        #     url=review_url.format(id=movie.get('id'), num=0),
        #     meta={'movie': movie},
        #     callback=self.parse_movie_review_douban,
        #     headers=self.header,
        #     cookies=self.cookies,
        # )

        for page in range(5):
            yield Request(
                url=review_url.format(id=movie.get('id'), num=page * 20),
                meta={'movie': movie},
                callback=self.parse_movie_review_douban,
                headers=self.header,
                cookies=self.cookies,
            )

    def parse_movie_comment_douban(self, response):
        print('------------------------------解析 短评界面，储存Comment、User等Item--------------------------------')

        movie = response.meta['movie']
        comment_list = response.xpath('//*[@class="comment-item"]')

        for each in comment_list:
            username = each.xpath('.//*[@class="avatar"]/a/@title').extract_first()
            url_douban = each.xpath('//*[@class="avatar"]/a/@href').extract_first()
            user_id_douban = url_douban.split('/')[-2]
            icon = each.xpath('.//*[@class="avatar"]/a/img/@src').extract_first()
            votes_raw = each.xpath('.//*[@class="votes"]/text()').extract_first()
            votes = int(votes_raw.strip()) if votes_raw else 0
            rate_raw = each.xpath('.//*[contains(@class,"allstar")]/@class').extract_first()
            rate = int(rate_raw[7]) if rate_raw else None
            comment_date = each.xpath('.//*[@class="comment-time "]/@title').extract_first().split(' ')[0]
            comment_content = each.xpath('.//*[@class="short"]/text()').extract_first()

            user = {
                'username': username,
                'icon': icon,
                'url': url_douban,
                'id_douban': user_id_douban,
            }

            item_user = items.User()
            item_user['username'] = username
            item_user['icon'] = icon
            item_user['url'] = url_douban
            item_user['id_douban'] = user_id_douban
            yield item_user

            yield Request(
                url=url_douban,
                meta={'user': user},
                callback=self.parse_user_index_douban,
                headers=self.header,
                cookies=self.cookies,
            )

            item_comment = items.Comment()
            item_comment['user_id'] = user_id_douban
            item_comment['movie_id'] = movie['id']
            item_comment['rate'] = rate
            item_comment['content'] = comment_content
            item_comment['date'] = comment_date
            item_comment['votes'] = votes
            yield item_comment

    def parse_movie_review_douban(self, response):
        print('------------------------------------解析 影评界面,储存User等item、跳转影评扩展界面--------------------------')

        movie = response.meta['movie']

        review_list = response.xpath('//*[@class="review-list  "]/div')
        for each in review_list:
            username_raw = each.xpath('.//*[@class="name"]/text()').extract_first()
            username = emoji.demojize(username_raw)
            url_douban = each.xpath('.//*[@class="avator"]/@href').extract_first()
            user_id_douban = url_douban.split('/')[-2]
            icon = each.xpath('.//*[contains(@src,"icon")]/@src').extract_first()

            review_href = each.xpath('.//*[contains(@href,"review")]/@href').extract_first()

            item_user = items.User()
            item_user['username'] = username
            item_user['icon'] = icon
            item_user['url'] = url_douban
            item_user['id_douban'] = user_id_douban
            yield item_user

            user = {
                'username': username,
                'icon': icon,
                'url': url_douban,
                'id_douban': user_id_douban,
            }

            yield Request(
                url=url_douban,
                meta={'user': user},
                callback=self.parse_user_index_douban,
                headers=self.header,
                cookies=self.cookies,
            )

            yield Request(
                url=review_href,
                meta={'user': user, 'movie_id': movie.get('id'), 'movie_url': movie.get('url')},
                callback=self.parse_review_detail_douban,
                headers=self.header,
                cookies=self.cookies,
            )

    def parse_user_index_douban(self, response):

        print('-------------------------------解析 用户界面，跳转短评list界面，跳转影评list界面----------------------------')

        user = response.meta['user']
        comment_url = 'https://movie.douban.com/people/{id}/collect?start={num}&sort=time&rating=all&filter=all&mode=grid'
        review_url = 'https://movie.douban.com/people/{id}/reviews'
        #
        # yield Request(
        #     url=comment_url.format(id=user['id_douban'], num=0),
        #     meta={'user': user},
        #     callback=self.parse_user_comment_douban,
        #     headers=self.header,
        #     cookies=self.cookies,
        # )
        # 处理短评
        for page in range(5):
            yield Request(
                url=comment_url.format(id=user['id_douban'], num=page * 15),
                meta={'user': user},
                callback=self.parse_user_comment_douban,
                headers=self.header,
                cookies=self.cookies,
            )

        # 跳转影评选项 （默认短评选项）
        yield Request(
            url=review_url.format(id=user['id_douban']),
            meta={'user': user},
            callback=self.parse_user_review_index_douban,
            headers=self.header,
            cookies=self.cookies,

        )

    def parse_user_review_index_douban(self, response):

        print('-------------------------------------用户界面解析影评list界面-------------------------')
        # 解析 影评
        user = response.meta['user']
        review_num = response.xpath('//*[@id="db-usr-profile"]/div[2]/h1/text()').extract_first().split('(')[1][:-1]
        review_url = 'https://movie.douban.com/people/{id}/reviews?start={num}'

        # 处理影评

        # yield Request(
        #     url=review_url.format(id=user['id_douban'], num=0),
        #     meta={'user': user},
        #     callback=self.parse_user_review_douban,
        #     headers=self.header,
        #     cookies=self.cookies,
        # )

        for page in range(1):
            yield Request(
                url=review_url.format(id=user['id'], num=page * 10),
                meta={'user': user},
                callback=self.parse_user_review_douban,
                headers=self.header,
                cookies=self.cookies,
            )

    def parse_user_review_douban(self, response):
        # 解析 用户影评
        print("---------------------------------解析 每一条影评，跳转详细内容界面----------------------")
        user = response.meta['user']

        review_list = response.xpath('//*[class="tlst clearfix"]')
        for each in review_list:
            review_url = each.xpath('.//*[contains(@href,"review")]/@href').extract_first()
            movie_url = each.xpath('.//*[contains(@href,"subject"]/href').extract_first()
            movie_id = movie_url.split('/')[-2]

            yield Request(
                url=review_url,
                meta={'user': user, 'movie_id': movie_id, 'movie_url': movie_url},
                callback=self.parse_review_detail_douban,
                headers=self.header,
                cookies=self.cookies,
            )

    def parse_user_comment_douban(self, response):

        print('---------------------------------解析 用户短评----------------------------')
        user = response.meta['user']

        comment_list = response.xpath('//*[@class="grid-view"]/div[@class="item"]')
        for each in comment_list:
            comment_content = each.xpath('.//*[@class="comment"]/text()').extract_first()
            comment_date = each.xpath('.//*[@class="date"]/text()').extract_first()
            rate_raw = each.xpath('.//*[contains(@class,"rating")]/@class').extract_first()
            rate = int(rate_raw[6]) if rate_raw else None

            movie_url = each.xpath(
                './/*[contains(@href,"subject")]/@href').extract_first()
            movie_id = movie_url.split('/')[-2]

            item_comment = items.Comment()
            item_comment['user_id'] = user['id_douban']
            item_comment['movie_id'] = movie_id
            item_comment['content'] = comment_content
            item_comment['date'] = comment_date
            item_comment['rate'] = rate
            item_comment['votes'] = 0
            yield item_comment

    def parse_review_detail_douban(self, response):
        print('---------------------------------------解析 影评内容界面，储存Review等Item-------------------------------')

        user = response.meta['user']
        movie_id = response.meta['movie_id']
        movie_url = response.meta['movie_url']

        title = response.xpath('//*[@id="content"]/div/div[1]/h1/span/text()').extract_first()
        rate_raw = response.xpath('//*[contains(@class,"allstar")]/@class').extract_first()
        rate = int(rate_raw[7]) if rate_raw else None
        content_raw = response.xpath('//*[@id="link-report"]/div[1]').extract_first()
        content = emoji.demojize(content_raw)
        votes_raw = response.xpath('//*[contains(@data-ad-ext,"有用")]/@data-ad-ext').extract_first().split(' ')[0][3:]
        votes = int(votes_raw.strip()) if votes_raw else 0
        date = response.xpath('/html/body/div[3]/div[1]/div/div[1]/div[1]/div/header/span[3]/@content').extract_first()

        item_review = items.Review()
        item_review['movie_id'] = movie_id
        item_review['user_id'] = user['id_douban']
        item_review['title'] = title
        item_review['rate'] = rate
        item_review['content'] = content
        item_review['votes'] = votes
        item_review['date'] = date
        yield item_review
