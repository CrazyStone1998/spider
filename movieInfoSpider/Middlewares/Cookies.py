import random

from movieInfoSpider import settings
from movieInfoSpider.tools.selenium_tool import SeleniumLogin


class CookiesMiddleWare(object):

    def __init__(self):
        self.cookiesPool = [
            {'push_noty_num': '0', 'push_doumail_num': '0', '__yadk_uid': '0efPxtNekkt04eMAnOdVVXcDeDUGz9cw',
             '__gads': 'ID=8ce536830d059575:T=1583162295:S=ALNI_Mb9Pb1EtmZzK5FmEYYbcJ_NiReBiw',
             '_pk_ses.100001.8cb4': '*', 'ap_v': '0,6.0',
             '_pk_id.100001.8cb4': 'be742f344e1b400f.1583162294.1.1583162294.1583162294.',
             '_pk_ref.100001.8cb4': '%5B%22%22%2C%22%22%2C1583162294%2C%22https%3A%2F%2Faccounts.douban.com%2Fpassport%2Flogin%3Fsource%3Dmovie%22%5D',
             'ck': 'CZIX', 'dbcl2': '"208735309:XhvRwIpk2ik"', 'bid': 'oNKv3hP3PSQ'},
            {'push_noty_num': '0', 'push_doumail_num': '0', '__yadk_uid': 'QBkLbx0BDMwt2yIwjTL1uLDwJykofBUl',
             '__gads': 'ID=c9531911d9dfc48a:T=1583162308:S=ALNI_MYfgidCEICQYMa8t6xFLtiuciu0Bw',
             '_pk_ses.100001.8cb4': '*', 'ap_v': '0,6.0',
             '_pk_id.100001.8cb4': '7bc852db63bcc28d.1583162308.1.1583162308.1583162308.',
             '_pk_ref.100001.8cb4': '%5B%22%22%2C%22%22%2C1583162308%2C%22https%3A%2F%2Faccounts.douban.com%2Fpassport%2Flogin%3Fsource%3Dmovie%22%5D',
             'ck': 'kFCm', 'dbcl2': '"188523178:gplCVp2qu+A"', 'bid': 'DAzgQN2_Vwc'}]
        # with open('cookies.txt','w') as f:
        #
        #     for item in settings.ACCOUNTS:
        #         status, cookies = SeleniumLogin().login_douban(item['user'], item['password'])
        #         f.write(str(cookies))
        #         f.write(',')
        #         self.cookiesPool.append(cookies)

    def process_request(self, request, spider):
        request.cookies = random.choice(self.cookiesPool)
        return None
