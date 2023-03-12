import user
from cnu_alp import ALP
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

### Preprocessing for test
IS_TEST = False
#if IS_TEST
import test
#endif

### Default parameters
DEFUALT_LECTURE_NAME = 'lecture_name'
# Class name what you want to play automatically
if IS_TEST:
    user_info = test.login_info
else:
    user_info = user.login_info
class_name = user.class_name
start_lecture_name = user.start_lecture_name

# URLs set proceding
# If program is not working, check these.
LOGIN_URL = 'https://sso.jnu.ac.kr/Idp/Login.aspx'
ECLASS_URL = 'https://sel.jnu.ac.kr/Rathon/Php/lms_sso.php'
VIEWER_URL = 'https://sel.jnu.ac.kr/mod/vod/viewer.php?id='

# X-path of Elements for click
LOGIN_XPATH = '/html/body/main/form/section/div[1]/div/div[1]/div[5]/button'
PLAY_BUTTON_CLASS = 'video-js'



# Start
alp = ALP()

# Login with user data
alp.cnu_login(LOGIN_URL, LOGIN_XPATH, user_info)

# Enter the e-class homepage
alp.get(ECLASS_URL)

# Get Classes
classes = alp.get_classes(class_name)

# Enter the class what you want
alp.get(classes[0]['class_url'])

# Get lectures
lectures = alp.get_lectures()

# Play video
is_started = False
if start_lecture_name in ' ' or start_lecture_name is DEFUALT_LECTURE_NAME:
    is_started = True
alp.play(lectures, start_lecture_name, VIEWER_URL, PLAY_BUTTON_CLASS, is_started)