from cnu_alp import ALP
import gui
import threading

# URLs set proceding
# If program is not working, check these.
LOGIN_URL = 'https://sso.jnu.ac.kr/Idp/Login.aspx'
PORTAL_DOMAIN = 'portal.jnu.ac.kr'
ECLASS_URL = 'https://sel.jnu.ac.kr/Rathon/Php/lms_sso.php'
VIEWER_URL = 'https://sel.jnu.ac.kr/mod/vod/viewer.php?id='

# X-path of Elements for click
LOGIN_XPATH = '/html/body/main/form/section/div[1]/div/div[1]/div[5]/button'

main_window: gui.MainWindow

classes:list[dict] = []
selects:list[int] = []

event = threading.Event()

def open_browser():
    # ALP thread start
    t_alp = threading.Thread(target=alp_start)
    t_alp.daemon = True
    t_alp.start()

def play_lectures():
    # Save information what lectures are selected
    main_window.getSelects()
    # Resume ALP thread
    event.set()

def alp_start():
    # Initialize list of classes
    classes.clear()

    alp = ALP()
    # self-login
    alp.cnu_self_login(LOGIN_URL, PORTAL_DOMAIN)
    print(selects)
    # Enter the e-class homepage
    alp.get(ECLASS_URL)
    # Get lectures
    for c in alp.get_classes():
        classes.append(c)
    print('획득')
    # Put information of classes to window's table
    main_window.createClassTable(classes)
    print(classes)

    # Auto play
    event.wait()
    for idx in selects:
        # Goto class
        alp.get(classes[idx]['class_url'])

        # Get lectures
        lectures = alp.get_lectures()

        alp.play(lectures, VIEWER_URL)
    
    print("재생 완료")
    alp.quit()

app = gui.init()

main_window = gui.MainWindow(selects)
# window.set_func('btn_start', alp_start)
main_window.setFunc('btn_start', open_browser)
main_window.setFunc('btn_play', play_lectures)

gui.start(app)

while True:
    pass


# Start
# alp = ALP()

# # Login with user data
# alp.cnu_login(LOGIN_URL, LOGIN_XPATH, user_info)

# # Enter the e-class homepage
# alp.get(ECLASS_URL)

# # Get Classes
# classes = alp.get_classes(class_name)

# # Enter the class what you want
# alp.get(classes[0]['class_url'])

# # Get lectures
# lectures = alp.get_lectures()

# # Play video
# is_started = False
# if start_lecture_name in ' ' or start_lecture_name is DEFUALT_LECTURE_NAME:
#     is_started = True
# alp.play(lectures, start_lecture_name, VIEWER_URL, PLAY_BUTTON_CLASS, is_started)