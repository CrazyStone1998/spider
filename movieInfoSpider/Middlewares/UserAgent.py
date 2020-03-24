import random

from movieInfoSpider import settings


class UserAgentMiddleWare(object):

    def __init__(self):
        self.userAgentsPool = settings.USER_AGENTS_POOL

    def process_request(self, request, spider):
        print('*******************')
        request.headers['User-Agent'] = random.choice(self.userAgentsPool)
