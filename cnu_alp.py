import time
import re
import socket
import http.client
from gui import MainWindow
from threading import Event
from bs4 import BeautifulSoup as bs
from bs4 import element as bs_element
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.command import Command
from webdriver_manager.chrome import ChromeDriverManager

WAIT_SECONDS = 3
TIME_DISPLAY_CLASS = 'vjs-remaining-time-display'
PLAY_BUTTON_CLASS = 'video-js'
ALERT_CLASS = 'alert-max-move'

def set_chrome_driver() -> WebDriver:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

class ALP:

    def __init__(self) -> None:
        self.driver: WebDriver = set_chrome_driver()
    
    def get(self, url) -> None:
        self.driver.get(url)

    def wait(self, wait:float=WAIT_SECONDS):
        self.driver.implicitly_wait(wait)

    def is_enabled(self):
        print(self.driver.get_log('browser'))

    def cnu_login(self, login_url:str, login_xpath:str, user_info:dict) -> None:
        self.get(login_url)
        self.wait()
        self.driver.find_element(By.NAME, 'UserID').send_keys(user_info['id'])
        self.driver.find_element(By.NAME, 'UserPWD').send_keys(user_info['pw'])
        self.driver.find_element(By.XPATH, login_xpath).click()
    
    def cnu_self_login(self, login_url:str, portal_domain:str, event_login_completed:Event, window:MainWindow):
        self.get(login_url)
        self.wait()
        event_login_completed.set()
        while True:
            try:
                WebDriverWait(self.driver, 0.5).until(EC.alert_is_present())
                window.setStatus('login_error')
            except: # No alert
                # info = self.driver.execute_script("return document.querySelector('info')")
                # if info is None:
                self.driver.execute_script("""
                if (!document.querySelector('info')) {
                    const info = document.createElement('info');
                    const info_title = document.createElement('h4');
                    const info_text = document.createElement('h1');
                    info_title.textContent = 'CNU ALP와 함께합니다.';
                    info_text.textContent = '로그인을 진행해주세요.';
                    info.appendChild(info_title);
                    info.appendChild(info_text);
                    document.body.appendChild(info);
                    info.style = `
                        position: fixed;
                        display: block;
                        top: 32px;
                        left: 32px;
                        z-index: 1000;
                        background: #FFFA;
                        border-radius: 30px;
                        padding: 15px;`
                }""")
                current_url = self.driver.current_url
                if current_url == login_url:
                    continue
                if portal_domain in current_url:
                    break
        print('Login completed.')

    def get_classes(self) -> list[dict]:
        self.wait()
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
            classes.append(dict_class)
        return classes

    def get_lectures(self) -> list[dict]:
        self.wait()
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

    def check_completed(self):
        self.driver.execute_script('''
        const video = document.querySelector('video')
        video.currentTime = video.duration;
        ''')
        # time.sleep(1)
        try:
            msg_danger = self.driver.find_element(By.CLASS_NAME, ALERT_CLASS)
            return False
        except:
            # print('ALP Error: check_completed() is called in improper situation.')
            return True

    def play(self, lectures, viewer_url):
        for lecture in lectures:
            
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
                # print('no alert')
                pass

            play_button = self.driver.find_element(By.CLASS_NAME, PLAY_BUTTON_CLASS)
            play_button.click()

            time_display = self.driver.find_element(By.CLASS_NAME, PLAY_BUTTON_CLASS)

            time.sleep(5)
            if not self.check_completed():
                while True:
                    # Check video ended
                    time.sleep(1)
                    p = re.compile('[0-9]{1,2}:[0-9]{2}')
                    p_find = p.findall(time_display.text)
                    if len(p_find) == 0:
                        continue
                    remain_time = p.findall(time_display.text)[0]
                    # print(remain_time)
                    if remain_time == '0:00':
                        time.sleep(1)
                        break
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            time.sleep(1)
        self.driver.back()
    
    def is_alive(self) -> bool:
        try:
            self.driver.execute(Command.GET_WINDOW_RECT)
            return True
        except (socket.error, http.client.CannotSendRequest):
            return False

    def quit(self):
        self.driver.quit()