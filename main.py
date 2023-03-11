import user
import time
import re
from bs4 import BeautifulSoup as bs
from bs4 import element as bs_element
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from pypreprocessor import pypreprocessor

IS_TEST = True
#if IS_TEST
import test
#endif

### Default parameters
# Class name what you want to play automatically
if IS_TEST:
    user_info = test.login_info
else:
    user_info = user.login_info
class_name = user.class_name
start_lecture_name = user.start_class_name

# URLs set proceding
# If program is not working, check these.
LOGIN_URL = 'https://sso.jnu.ac.kr/Idp/Login.aspx'
ECLASS_URL = 'https://sel.jnu.ac.kr/Rathon/Php/lms_sso.php'
VIEWER_URL = 'https://sel.jnu.ac.kr/mod/vod/viewer.php?id='

# X-path of Elements for click
LOGIN_X_PATH = '/html/body/main/form/section/div[1]/div/div[1]/div[5]/button'
PLAY_BUTTON_CLASS = 'video-js'

### Functions
def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub(' ', str(data))

def get_crawl(URL):
    response = driver.get(URL)
    html = driver.page_source
    soup7 = bs(html, 'html.parser')
    divs = soup7.findAll('div')
    # crawl_data = remove_html_tags(divs)
    return divs

### Login with infomation in user.py
driver = set_chrome_driver()
driver.implicitly_wait(3)
driver.get(LOGIN_URL)
driver.find_element(By.NAME, 'UserID').send_keys(user_info['id'])
driver.find_element(By.NAME, 'UserPWD').send_keys(user_info['pw'])
driver.find_element(By.XPATH, LOGIN_X_PATH).click()

### Enter the e-class homepage
driver.get(ECLASS_URL)

### Enter the class what you want
class_url = ''
driver.execute_script("document.querySelectorAll('.new').forEach((e) => e.remove())")
html = driver.page_source
soup7 = bs(html, 'html.parser')
tags = soup7.findAll('a', class_='course_link')
for tag in tags:
    tag_class = tag.find(class_='course-title')
    tag_class_name = tag.find(class_='course-title').string
    if tag_class_name == None:
        continue
    print(tag_class_name)
    if class_name in tag_class_name:
        class_url = tag['href']
driver.get(class_url)

### Get lectures
driver.execute_script("document.querySelector('.course_box_current').remove()")
lectures = []
html = driver.page_source
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

# Play video
for lecture in lectures:
    print('Play the \'%s\'.' % lecture['name'])

    link = VIEWER_URL + lecture['id']
    driver.execute_script(f'window.open("{link}");')
    driver.implicitly_wait(3)

    driver.switch_to.window(driver.window_handles[-1])

    try:
        WebDriverWait(driver, 1).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
    except:
        print('no alert')

    play_button = driver.find_element(By.CLASS_NAME, PLAY_BUTTON_CLASS)
    play_button.click()

    time.sleep(lecture['during'])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)

print('Completed auto play.')
driver.quit()