from cnu_alp import ALP
import gui
from gui import Msg
import threading
import time

# URLs set proceding
# If program is not working, check these.
LOGIN_URL = 'https://sso.jnu.ac.kr/Idp/Login.aspx'
PORTAL_DOMAIN = 'portal.jnu.ac.kr'
ECLASS_URL = 'https://sel.jnu.ac.kr/Rathon/Php/lms_sso.php'
VIEWER_URL = 'https://sel.jnu.ac.kr/mod/vod/viewer.php?id='

# X-path of Elements for click
LOGIN_XPATH = '/html/body/main/form/section/div[1]/div/div[1]/div[5]/button'

# Timeout to close browser when if browser is not responding in ALP_TIMEOUT
# Browser will not be responding in some situations.
# 1. Network unstable or absent.
# 2. Error in downloading chrome driver.
# 3. User immediately close browser as soon as the browser is turned on.
ALP_TIMEOUT = 15

# Private variables
main_window: gui.MainWindow

# Global variables to be accessed by any thread.
classes:list[dict] = []
selects:list[int] = []
is_alp_on = False
alp: ALP = None
events: list[threading.Event] = [False, False]
# [0]: wait to play
# [1]: wait to load in login page

def start_thread(target:callable):
    t = threading.Thread(target=target)
    t.daemon = True
    t.start()

def open_browser():
    # ALP thread start
    events[0] = threading.Event()
    events[1] = threading.Event()

    main_window.setButtonEnable(btn1=False)
    main_window.setStatus(Msg.OPENING)

    start_thread(alp_start)
    start_thread(alp_check)
    start_thread(alp_timeout)

def play_lectures():
    # Save information what lectures are selected
    main_window.getSelects()
    # Resume ALP thread
    events[0].set()
    main_window.setButtonEnable(btn2=False)

def alp_start():
    global is_alp_on, alp, classes
    # Initialize list of classes
    classes.clear()

    is_alp_on = True
    alp = ALP()

    main_window.setStatus(Msg.LOGIN)
    # self-login
    login = alp.cnu_self_login(LOGIN_URL, PORTAL_DOMAIN, events[1], main_window)
    if not login:
        events[1].set()
        return

    # Enter the e-class homepage
    main_window.setStatus(Msg.LOADING)
    alp.get(ECLASS_URL)

    # Get lectures
    # for c in alp.get_classes():
    #     classes.append(c)
    classes = alp.get_classes().copy()

    # Put information of classes to window's table
    main_window.updateClassTable(classes)
    # print(classes)

    # Auto play
    main_window.setStatus(Msg.SELECT)
    events[0].wait()
    main_window.setStatus(Msg.PLAY)
    for idx in selects:
        # Goto class
        alp.get(classes[idx]['class_url'])

        # Get lectures
        lectures = alp.get_lectures()

        alp.play(lectures, VIEWER_URL)
    
    main_window.setButtonEnable(btn1=True, btn2=False)
    print("ALP completed.")
    alp.quit()
    is_alp_on = False
    main_window.setStatus(Msg.COMPLETE)

def alp_check():
    global is_alp_on
    events[1].wait()

    while True:
        if alp == None:
            break
        is_alive: bool = alp.is_alive()
        if not is_alive:
            if is_alp_on:
                is_alp_on = False
            print("[t_check] ALP is off.")
            alp = None
            main_window.setButtonEnable(btn1=True, btn2=False)
            main_window.setStatus(Msg.BROWSER_ERROR)
            break
        time.sleep(1)

def alp_timeout():
    time.sleep(ALP_TIMEOUT)
    print('[t_timeout] ALP_TIMEOUT: ' + str(events[1].is_set()))
    if not events[1].is_set():
        events[1].set()

app = gui.init()

main_window = gui.MainWindow(selects)
main_window.setFunc('btn_start', open_browser)
main_window.setFunc('btn_play', play_lectures)

gui.start(app)

# End of program
time.sleep(1)
if is_alp_on:
    alp.quit()
# exit()