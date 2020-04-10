# Instagram Auto Like

""" Automation of liking images on Instagram """

from scroll import Scroll
from random import randrange, randint
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


class AutoLike:

    def __init__(self, usrname, pssword):
        """
        initialise auto like class
        :param usrname: username for instagram user
        :param pssword: password for instagram user

        WARNING: using this program is against Instagram terms of use
        """
        self.instagram_url = 'https://www.instagram.com'
        self.driver = webdriver.Chrome(options=self.configure_driver_options(headless=False))
        self.driver.get(self.instagram_url)
        self.driver_login(usrname, pssword)
        self.like_count = 0
        self.scroller = Scroll(self.driver)

    @staticmethod
    def configure_driver_options(headless=True):
        """
        configure chrome driver options
        :param headless: running headless will not open browser
        :return: chrome options
        """
        options = Options()
        options.add_argument("--disable-extensions")  # disable chrome extensions
        options.add_argument("--disable-gpu")  # disable gpu
        if headless:
            options.add_argument("--headless")  # running headless will not display window
        options.add_experimental_option('prefs', {
            'credentials_enable_service': False,
            'profile': {
                'password_manager_enabled': False
            }
        })
        return options

    def driver_login(self, username, password):
        """
        login to instagram using chrome driver
        :param username: instagram username
        :param password: user password
        """
        login_switcher_xpath = '/html/body/span/section/main/article/div[2]/div[2]/p/a'
        login_switcher_href = '/accounts/login/?source=auth_switcher'
        login_switcher = self.driver.find_element_by_xpath(login_switcher_xpath + "[@href='" + login_switcher_href + "']")
        login_switcher.click()
        self.sleep()
        username_xpath = '//input[@name="username"]'
        username_elem = self.driver.find_element_by_xpath(username_xpath)
        username_elem.send_keys(username)
        password_xpath = '//input[@name="password"]'
        password_elem = self.driver.find_element_by_xpath(password_xpath)
        password_elem.send_keys(password)
        self.sleep()
        password_elem.send_keys(Keys.ENTER)
        self.sleep()
        self.click_button(btn_class_name='HoLwm')
        self.sleep()

    def click_button(self, btn_class_name):
        """
        find a button using class name and click
        :param btn_class_name: class name for button to click
        """
        if self.driver.find_elements_by_class_name(btn_class_name):
            qc_cmp_buttons = self.driver.find_elements_by_class_name(btn_class_name)
            for button in qc_cmp_buttons:
                button.click()

    def close_driver(self):
        """ quit selenium webdriver - close chrome """
        self.driver.quit()

    def get_post_hrefs(self):
        """
        get list of post urls available on the current page
        :return: list of post urls
        """
        response = self.driver.execute_script("return document.documentElement.outerHTML")
        soup = BeautifulSoup(response, "html.parser")
        a = soup.find_all('a')
        post_hrefs = set()
        for href in a:
            try:
                h = href.get('href')
                if '/p/' in h:
                    post_hrefs.add(h)
            except Exception as e:
                print(e)
        return post_hrefs

    def click_like_button(self):
        """
        find like button on page and click. increment like counter if successful
        """
        like_class_name = 'glyphsSpriteHeart__outline__24__grey_9'
        try:
            like_buttons = self.driver.find_elements_by_class_name(like_class_name)
            for like_button in like_buttons:
                label = like_button.get_attribute("aria-label")
                if label == 'Like':
                    like_button.click()
                    self.like_count += 1
        except Exception as e:
            print(e)

    def like_posts(self, post_hrefs):
        """
        like posts
        :param post_hrefs: href attribute specifies the URL of the post to like
        """
        for href in post_hrefs:
            self.driver.get(self.instagram_url + href)
            self.click_like_button()
            self.sleep()

    def explore(self):
        """
        recursive method to load explore page and start liking posts
        """
        self.driver.get(self.instagram_url + '/explore')
        self.scroller.scroll_x_times(randrange(0, 2))
        post_hrefs = self.get_post_hrefs()
        post_count = len(post_hrefs)
        if post_count == 0:
            return
        like_x_posts = randrange(0, post_count)
        posts_to_like = randint(0, post_count - 1, like_x_posts)
        for i, post in enumerate(post_hrefs):
            if i in posts_to_like:
                self.like_posts([post_hrefs[i]])
            else:
                self.driver.get(self.instagram_url + post_hrefs[i])
        self.explore()

    def like_tags(self, tags, likes_per_tag):
        """
        like posts from a given list of hashtags
        :param tags: hashtags of posts to like
        :param likes_per_tag: maximum number of posts to like
        """
        for i, tag in enumerate(tags):
            self.like_count = 0
            while self.like_count < likes_per_tag[i]:
                self.driver.get(self.instagram_url + '/explore/tags/' + tag + '/')
                self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'r')
                self.like_posts(self.get_post_hrefs())

    def infinite_likes_for_tag(self, tag):
        """
        infinite likes for a given tag
        :param tag: the hashtag to like posts from
        """
        while True:
            self.driver.get(self.instagram_url + '/explore/tags/' + tag + '/')
            self.sleep()
            self.like_posts(self.get_post_hrefs())

    @staticmethod
    def sleep():
        """ sleep random amount of seconds between from_ and to_ """
        sleep(randrange(1, 5))


# Program driver
if __name__ == '__main__':
    u, p = 'test@gmail.com', '123456'
    bot = AutoLike(usrname=u, pssword=p)
