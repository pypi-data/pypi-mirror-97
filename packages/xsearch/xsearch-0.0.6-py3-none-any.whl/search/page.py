import os
import json
import time
import re
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urlparse
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class SearchPage:

    def __init__(self, domain):
        self.domain = re.sub(r"http://|https://|www.", "", domain)
        self.search_box_file = os.getcwd().replace('\\', '/') + "/param/searchbox_of_searchpage.json"
        with open(self.search_box_file, encoding='utf-8') as json_file:
            self.search_box_dict = json.load(json_file)
        self.search_method = self.search_box_dict.get(self.domain, {}).get('method')
        self.search_name = self.search_box_dict.get(self.domain, {}).get('name')
        self.driver = None

    @classmethod
    def user_input(cls):
        domains = ['google.com', 'google.com.hk', 'baidu.com', 'bing.com', 'sogou.com', 'weixin.sogou.com',
                   '36kr.com', 'huxiu.com', 'iyiou.com', 'qbitai.com', 'pingwest.com', 'awtmt.com',
                   'kejilie.com', 'leiphone.com', 'csdn.net', '51cto.com', 'woshipm.com', 'qianzhan.com']
        while 1:
            domain = input("请输入搜索域名")
            if domain in domains:
                break
            else:
                print('暂不支持，请重新输入')
        return cls(domain)

    def startup(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get('https://' + self.domain)

    @staticmethod
    def get_search_element(driver, method, name):
        """给定网页浏览器和查找方法，返回搜索框对象
        :param driver: selenium.webdriver.chrome.webdriver.WebDriver
        :param method: str 支持name/class/id/placeholder
        :param name: str
        :return:
        """
        if method == 'name':
            element = driver.find_element_by_name(name)
        elif method == 'class':
            element = driver.find_element_by_class_name(name)
        elif method == 'id':
            element = driver.find_element_by_id(name)
        elif method == 'placeholder':
            element = driver.find_element(By.XPATH, "//input[@placeholder='{}']".format(name))
        else:
            element = None
        return element

    def submit_keyword(self, keyword):
        search_box = self.get_search_element(self.driver, self.search_method, self.search_name)
        search_box.clear()
        search_box.send_keys(keyword)
        time.sleep(0.5)
        search_box.send_keys(Keys.ENTER)


class IndexPage:

    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(10)
        self.domain = urlparse(self.driver.current_url).netloc.replace('www.', '')

        self.search_box_file = os.getcwd().replace('\\', '/') + '/param/searchbox_of_indexpage.json'
        with open(self.search_box_file, encoding='utf-8') as file1:
            self.search_box_dict = json.load(file1)
        self.search_method = self.search_box_dict.get(self.domain, {}).get('method')
        self.search_name = self.search_box_dict.get(self.domain, {}).get('name')

        self.search_result_file = os.getcwd().replace('\\', '/') + '/param/search_result.json'
        with open(self.search_result_file, encoding='utf-8') as file2:
            self.search_result_dict = json.load(file2)
        self.result_tag = self.search_result_dict.get(self.domain, {}).get('tag')
        self.result_class = self.search_result_dict.get(self.domain, {}).get('class_name')

    @staticmethod
    def get_search_element(driver, method, name):
        """给定网页浏览器、查找方法、查找内容，返回搜索框对象
        :param driver: selenium.webdriver.chrome.webdriver.WebDriver
        :param method: str 支持name/class/id/placeholder
        :param name: str
        :return:
        """
        if method == 'name':
            element = driver.find_element_by_name(name)
        elif method == 'class':
            element = driver.find_element_by_class_name(name)
        elif method == 'id':
            element = driver.find_element_by_id(name)
        elif method == 'placeholder':
            element = driver.find_element(By.XPATH, "//input[@placeholder='{}']".format(name))
        else:
            element = None
        return element

    def submit_keyword(self, keyword):
        search_box = self.get_search_element(self.driver, self.search_method, self.search_name)
        search_box.clear()
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.ENTER)
        time.sleep(1)

    def get_search_result(self):

        def convert_wechat_link(link):
            b = int(random.random() * 100) + 1
            a = link.find("url=")
            converted_link = 'https://weixin.sogou.com' + link + "&k=" + str(b) + "&h=" + link[a + 25 + b]
            return converted_link

        res_list = []
        if self.domain == 'google.com' or self.domain == 'google.com.hk':
            content = self.driver.page_source.encode('utf-8')
            soup = BeautifulSoup(content, 'lxml')
            ele_list = soup.find_all('div', 'g')
            for ele in ele_list:
                try:
                    res_list.append([ele.find('h3').text, ele.find('a').get('href'), ele.find('span', 'aCOpRe').text])
                except AttributeError:
                    continue

        elif self.domain == 'baidu.com':
            element = WebDriverWait(self.driver, 10).\
                until(ec.presence_of_element_located((By.CLASS_NAME, "search_tool")))
            content = self.driver.page_source.encode('utf-8')
            soup = BeautifulSoup(content, 'lxml')
            ele_list = soup.find_all('div', 'result c-container new-pmd')
            for ele in ele_list:
                try:
                    res_list.append([ele.find('h3').text, ele.find('a').get('href'),
                                     ele.find('div', 'c-abstract').text])
                except AttributeError:
                    continue

        elif self.domain == 'bing.com':
            content = self.driver.page_source.encode('utf-8')
            soup = BeautifulSoup(content, 'lxml')
            ele_list = soup.find_all('li', 'b_algo')
            for ele in ele_list:
                try:
                    res_list.append([ele.find('h2').text, ele.find('a').get('href'), ele.find('p').text])
                except AttributeError:
                    continue

        elif self.domain == 'sogou.com':
            content = self.driver.page_source.encode('utf-8')
            soup = BeautifulSoup(content, 'lxml')
            ele_list = soup.find_all('div', 'vrwrap')
            for ele in ele_list:
                try:
                    res_list.append([ele.find('h3').text, ele.find('a').get('href'),
                                     ele.find('div', 'strBox').text])
                except AttributeError:
                    continue

        elif self.domain == 'weixin.sogou.com':
            content = self.driver.page_source.encode('utf-8')
            soup = BeautifulSoup(content, 'lxml')
            ele_list = soup.find('ul', 'news-list').find_all('li')
            for ele in ele_list:
                try:
                    res_list.append([ele.find('h3').text.strip(), convert_wechat_link(ele.find('a').get('href')),
                                     ele.find('p', 'txt-info').text])
                except AttributeError:
                    continue

        else:
            ele_list = self.driver.find_elements_by_class_name(self.result_class)
            for ele in ele_list:
                try:
                    res_list.append([ele.find_element_by_tag_name('a').get_attribute('href'), ele.text])
                except NoSuchElementException:
                    continue

        return res_list
