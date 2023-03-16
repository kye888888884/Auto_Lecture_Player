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

# Private variables
main_window: gui.MainWindow
event = threading.Event()

# Global variables
classes:list[dict] = []
selects:list[int] = []
alp_container:list[ALP] = []


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
    alp_container.append(alp)
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
    main_window.updateClassTable(classes)
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

# End of program
alp_container[-1].quit()
exit()