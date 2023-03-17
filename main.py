from cnu_alp import ALP
import gui
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

# Other const
ALP_TIMEOUT = 10

# Private variables
main_window: gui.MainWindow

# Global variables
classes:list[dict] = []
selects:list[int] = []
alp_container:list[ALP] = []
is_alp_on:list = [False]

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
    main_window.setStatus('opening')

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
    # Initialize list of classes
    classes.clear()

    is_alp_on[0] = True
    alp = ALP()
    alp_container.append(alp)

    main_window.setStatus('login')
    # self-login
    alp.cnu_self_login(LOGIN_URL, PORTAL_DOMAIN, events[1], main_window)
    # print(selects)

    # Enter the e-class homepage
    main_window.setStatus('loading')
    alp.get(ECLASS_URL)

    # Get lectures
    for c in alp.get_classes():
        classes.append(c)
    # print('획득')

    # Put information of classes to window's table
    main_window.updateClassTable(classes)
    # print(classes)

    # Auto play
    main_window.setStatus('select')
    events[0].wait()
    main_window.setStatus('playing')
    for idx in selects:
        # Goto class
        alp.get(classes[idx]['class_url'])

        # Get lectures
        lectures = alp.get_lectures()

        alp.play(lectures, VIEWER_URL)
    
    main_window.setButtonEnable(btn1=True, btn2=False)
    print("재생 완료")
    alp.quit()
    is_alp_on[0] = False
    main_window.setStatus('complete')

def alp_check():
    events[1].wait()
    try:
        while True:
            is_alive: bool = alp_container[0].is_alive()
            if not is_alive:
                break
            time.sleep(2)
            # print(is_alive)
    except:
        if is_alp_on[0]:
            print("ALP is off.")
            is_alp_on[0] = False
            alp_container.clear()
            main_window.setButtonEnable(btn1=True, btn2=False)
            main_window.setStatus('browser_error')

def alp_timeout():
    time.sleep(ALP_TIMEOUT)
    print('yeah')
    print(events[1].is_set())
    if not events[1].is_set():
        events[1].set()

app = gui.init()

main_window = gui.MainWindow(selects)
main_window.setFunc('btn_start', open_browser)
main_window.setFunc('btn_play', play_lectures)

gui.start(app)

# End of program
time.sleep(1)
if is_alp_on[0]:
    alp_container[-1].quit()
exit()