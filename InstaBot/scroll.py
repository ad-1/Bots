from time import sleep
from random import randrange


class Scroll:

    def __init__(self, driver):
        """
        javascript scroller class
        :param driver: chrome driver
        """
        self.javascript_scroll = "window.scrollTo(0, document.body.scrollHeight);" \
                                 "var body = document.body, html = document.documentElement;" \
                                 "var height = Math.max(" \
                                 "body.scrollHeight, body.offsetHeight, html.clientHeight, html.scrollHeight, html.offsetHeight" \
                                 ");" \
                                 "return height"
        self.driver = driver

    def detect_end_of_scroll(self):
        """
        scroll down to the end of a web page using javascript
        """
        print('scrolling down to end of page...')
        len_of_page = self.execute_scroll()
        last_count = 0
        while last_count != len_of_page:
            last_count = len_of_page
            len_of_page = self.execute_scroll()
        print('...finished scroll')

    def scroll_x_times(self, x):
        """
        scroll down x amount of time
        :param x: number of times to scroll
        """
        print('scroll down {} times'.format(x))
        for _ in range(x):
            self.execute_scroll()

    def execute_scroll(self):
        """
        execute javascript scroll down method
        :return: current length of page
        """
        sleep(randrange(0, 3))
        len_of_page = self.driver.execute_script(self.javascript_scroll)
        return len_of_page

