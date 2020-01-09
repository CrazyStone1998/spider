import cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import random
import time


class SeleniumLogin(object):

    CHROME_DRIVER_PATH = \
        '/home/stone/Documents/Code/remote/spider/movieInfoSpider/drivers/chromedriver'
    DOUBAN_LOGIN_URL = \
        'https://accounts.douban.com/passport/login?source=movie'

    def __init__(self, browser_enable=True):
        # 服务器禁用图形化界面 默认开启
        chrome_options = webdriver.ChromeOptions()
        if not browser_enable:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument(('--disable-gpu'))
        # 初始化
        self.driver = webdriver.Chrome(self.CHROME_DRIVER_PATH, options=chrome_options)

    def login_douban(self, username, password):

        self.driver.get(self.DOUBAN_LOGIN_URL)
        # 切换帐号密码登录
        btn_account = self.driver.find_element_by_class_name('account-tab-account')
        btn_account.click()
        # 输入帐号密码
        input_username = self.driver.find_element_by_id('username')
        input_password = self.driver.find_element_by_id('password')

        input_username.send_keys(username)
        input_password.send_keys(password)

        time.sleep(1)

        #
        url_before_login = self.driver.current_url
        print('url_befor_login:', url_before_login)

        btn_login = self.driver.find_element_by_class_name('btn-active')
        btn_login.click()
        time.sleep(2)

        url_after_login = self.driver.current_url
        print('url_after_login:', url_after_login)

        if url_after_login != url_before_login:
            print('login success')
            return self._after_login(True)
        else:
            print('need captcha')
            return self._after_login(self._captcha(url_before_login, 2))

    def _douban_distence(self, img_url, small_shape, top, left=12):
        # 计算 移动距离
        top = int(top * 2)
        bottom = top + small_shape[0]

        img = cv2.imread(img_url, cv2.IMREAD_GRAYSCALE)[238:628, 134:814]
        x, y = img.shape
        img_crop = img[top:bottom, int(y / 2):y]

        ret, img_binary = cv2.threshold(img_crop, 240, 0, cv2.THRESH_TOZERO)

        target = img_binary.sum(axis=0)
        column_1 = np.where(target == max(target))[0][0]
        target[np.where(target == max(target))[0][0]] = 0
        column__2 = np.where(target == max(target))[0][0]
        column = column_1 if column_1 < column__2 else column__2
        # 不知为什么 多出10px 这里多减去 10
        target = int((column + int(y / 2)) / 2 - left - 10)
        print('distence:', target)

        return target

    def _captcha(self, url_before_login, times):
        captcha_frame = self.driver.find_element_by_id('tcaptcha_popup')
        self.driver.switch_to.frame(captcha_frame)
        #
        bg_img = self.driver.find_element_by_class_name('tcaptcha-bg-img')
        drop_img = self.driver.find_element_by_id('slideBlock')
        #
        top = float(drop_img.get_attribute('style').split(';')[2].split(':')[1][1:-2])
        bg_img_url = bg_img.get_attribute('src')
        #
        js = 'window.open("' + bg_img_url + '");'
        self.driver.execute_script(js)
        time.sleep(1)
        #
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[1])
        time.sleep(1)

        img_url = '/home/stone/Documents/Code/remote/spider/movieInfoSpider/tools/captcherImages/img.png'
        self.driver.get_screenshot_as_file(img_url)
        #
        self.driver.switch_to.window(windows[0])
        self.driver.switch_to.frame(captcha_frame)
        time.sleep(1)
        #
        dist = self._douban_distence(img_url, (136, 136), top)

        print('douban_distence', dist)
        #
        has_gone_dist = 0
        remaining_dist = dist
        # 按下鼠标左键
        btn_drop = self.driver.find_element_by_id('tcaptcha_drag_button')
        ActionChains(self.driver).click_and_hold(btn_drop).perform()

        while remaining_dist > 0:
            ratio = remaining_dist / dist
            if ratio < 0.2:
                # 结束阶段移动较慢
                span = random.randint(5, 8)
            elif ratio > 0.8:
                # 开始阶段移动较慢
                span = random.randint(5, 8)
            else:
                # 中间部分移动快
                span = random.randint(10, 16)
            ActionChains(self.driver).move_by_offset(span, random.randint(-5, 5)).perform()
            remaining_dist -= span
            has_gone_dist += span
            time.sleep(random.randint(5, 20) / 100)

        ActionChains(self.driver).move_by_offset(remaining_dist, random.randint(-5, 5)).perform()
        ActionChains(self.driver).release(on_element=btn_drop).perform()
        time.sleep(5)

        if self.driver.current_url() != url_before_login:
            return True
        elif times == 0:
            return False
        else:
            times = times - 1
            self._captcha(url_before_login, times)

    def _after_login(self, status):
        # get cookie， return
        if status:
            print('login success')
            # 把cookie转化为字典
            cookies_dict = {
                cookie['name']: cookie['value'] for cookie in self.driver.get_cookies()
            }
            return True, cookies_dict

        else:
            return False, None


# wd = webdriver.Chrome('home/stone/Documents/Code/remote/spider/movieInfoSpider/drivers/chromedriver')
# wd.get('https://accounts.douban.com/passport/login?source=movie')
#
# # 模拟登录
# btn_account = wd.find_element_by_class_name('account-tab-account').click()
# input_username = wd.find_element_by_id('username')
# input_passwd = wd.find_element_by_id('password')
# input_username.send_keys('13653399918')
# input_passwd.send_keys('136Shijunyu@6')
#
# btn_login = wd.find_element_by_class_name('btn-active').click()
# time.sleep(2)
#
# # 验证码
#
# captcha_frame = wd.find_element_by_id('tcaptcha_popup')
# wd.switch_to.frame(captcha_frame)
#
# bg_img = wd.find_element_by_class_name('tcaptcha-bg-img')
# drop_img = wd.find_element_by_id('slideBlock')
#
# top = float(drop_img.get_attribute('style').split(';')[2].split(':')[1][1:-2])
# back_url = bg_img.get_attribute('src')
#
# js = 'window.open("' + back_url + '");'
# wd.execute_script(js)
# time.sleep(1)
#
# windows = wd.window_handles
#
# wd.switch_to.window(windows[1])
# time.sleep(1)
# img_url = '/home/stone/Documents/Code/remote/spider/movieInfoSpider/tools/img.png'
# wd.get_screenshot_as_file(img_url)
#
# wd.switch_to.window(windows[0])
# wd.switch_to.frame(captcha_frame)
# time.sleep(1)
#
# dist = douban_distence(img_url, (136, 136), top, )
# print('douban_distence', dist)
#
# has_gone_dist = 0
# remaining_dist = dist
# # 按下鼠标左键
# btn_drop = wd.find_element_by_id('tcaptcha_drag_button')
# ActionChains(wd).click_and_hold(btn_drop).perform()
# while remaining_dist > 0:
#     ratio = remaining_dist / dist
#     if ratio < 0.2:
#         # 结束阶段移动较慢
#         span = random.randint(5, 8)
#     elif ratio > 0.8:
#         # 开始阶段移动较慢
#         span = random.randint(5, 8)
#     else:
#         # 中间部分移动快
#         span = random.randint(10, 16)
#     ActionChains(wd).move_by_offset(span, random.randint(-5, 5)).perform()
#     remaining_dist -= span
#     has_gone_dist += span
#     time.sleep(random.randint(5, 20) / 100)
#
# ActionChains(wd).move_by_offset(remaining_dist, random.randint(-5, 5)).perform()
# ActionChains(wd).release(on_element=btn_drop).perform()
