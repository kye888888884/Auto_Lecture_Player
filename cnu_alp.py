import time
import re
from bs4 import BeautifulSoup as bs
from bs4 import element as bs_element
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

def set_chrome_driver() -> WebDriver:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

class ALP:

    def __init__(self) -> None:
        self.driver: WebDriver = set_chrome_driver()

    def cnu_login(self, login_url:str, login_xpath:str, user_info:dict) -> None:
        self.driver.implicitly_wait(3)
        self.driver.get(login_url)
        self.driver.find_element(By.NAME, 'UserID').send_keys(user_info['id'])
        self.driver.find_element(By.NAME, 'UserPWD').send_keys(user_info['pw'])
        self.driver.find_element(By.XPATH, login_xpath).click()

    def get(self, url) -> None:
        self.driver.get(url)

    def get_classes(self, main_class:str=None) -> list[dict]:
        classes = []
        self.driver.execute_script("document.querySelectorAll('.new').forEach((e) => e.remove())")
        html = self.driver.page_source
        soup7 = bs(html, 'html.parser')
        tags = soup7.findAll('a', class_='course_link')
        for tag in tags:
            tag_class_name = tag.find(class_='course-title').string
            if tag_class_name == None:
                continue
            dict_class = {
                'class_name': tag_class_name,
                'class_url' : tag['href']
            }
            if main_class != None and main_class in tag_class_name:
                return [dict_class]
            classes.append(dict_class)
        return classes

    def get_lectures(self) -> list[dict]:
        self.driver.execute_script("document.querySelector('.course_box_current').remove()")
        lectures = []
        html = self.driver.page_source
        soup7 = bs(html, 'html.parser')
        tags = soup7.findAll('div', class_='activityinstance')
        tag: bs_element.Tag
        for tag in tags:
            tag_displayoptions = tag.find(class_='displayoptions')
            if tag_displayoptions == None:
                continue

            tag_instancename: bs_element.Tag = tag.find(class_='instancename')
            lecture_name = tag_instancename.contents[0]
            lecture_url = tag.find('a')
            if lecture_url == None:
                continue
            
            p = re.compile('[0-9]{5,7}')
            lecture_id = p.findall(lecture_url['href'])[0]

            p = re.compile('[0-9]{2}:[0-9]{2}')
            lecture_during_text = tag.find(class_='text-info').string
            lecture_during = p.findall(lecture_during_text)[0]
            
            lecture_minute = int(lecture_during[:2])
            lecture_second = int(lecture_during[3:])
            lecture_seconds = lecture_minute * 60 + lecture_second

            lectures.append({
                'name': lecture_name,
                'id': lecture_id,
                'during': lecture_seconds
            })
        return lectures

    def play(self, lectures, start_lecture_name, viewer_url, play_button_class, is_started=False):
        for lecture in lectures:
            if not is_started:
                if start_lecture_name not in lecture['name']:
                    continue
                else:
                    is_started = True
            
            print('Play the \'%s\'.' % lecture['name'])

            link = viewer_url + lecture['id']
            self.driver.execute_script(f'window.open("{link}");')
            self.driver.implicitly_wait(3)

            self.driver.switch_to.window(self.driver.window_handles[-1])

            try:
                WebDriverWait(self.driver, 1).until(EC.alert_is_present())
                alert = self.driver.switch_to.alert
                alert.accept()
            except:
                print('no alert')

            play_button = self.driver.find_element(By.CLASS_NAME, play_button_class)
            play_button.click()

            time.sleep(lecture['during'])
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            time.sleep(1)

        print('Completed auto play.')
        self.driver.quit()