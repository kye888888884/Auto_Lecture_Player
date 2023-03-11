# 전남대학교 자동 강의 플레이어

### CNU Auto Lecture Player

---

## 개요

-   전남대학교 e클래스의 강의를 자동으로 시청하는 프로그램입니다. 처음 강의를 시청하면 반드시 원래 속도로 들어야 하는 불편함 때문에 제작했습니다. 강의를 배속하거나, 넘겨가며 듣는 학생들에게 유용합니다.
-   파이썬으로 실행할 수 있으며, 현재는 터미널에서 직접 실행해야 합니다. 추후에 GUI가 있는 응용프로그램으로 제작할 예정입니다.
-   `Visual Studio Code`같은 코드 편집 프로그램에서 실행하는 것을 추천합니다.

---

## 사용 방법 (`v1.0`)

###### ※ Visual Studio Code를 기준으로 설명합니다.

1. Python 3.6 이상의 버전과 Visual Studio Code, Chrome 브라우저를 설치합니다.
    - [Python 설치 방법](https://medium.com/@psychet_learn/python-%EA%B8%B0%EC%B4%88-2%EC%9E%A5-python-%EC%84%A4%EC%B9%98-%EB%B0%8F-%ED%99%98%EA%B2%BD%EC%84%A4%EC%A0%95-windows-ver-b030d96bcbd0) - medium.com/@psychet_learn
    - [Visual Studio Code 설치 방법](https://crazykim2.tistory.com/748) - crazykim2.tistory.com
    - [Chrome 브라우저 다운로드](https://www.google.com/intl/ko_kr/chrome/) - google.com
2. 프로젝트를 다운로드(또는 Clone) 받습니다.
3. main.py 파일이 있는 경로에서 Visual Studio Code를 실행합니다.
4. 터미널을 실행한 후 `pip install -r requirements.txt`를 입력합니다.
    - 필요한 파이썬 라이브러리를 다운로드 받는 명령어입니다.
    - 파이썬 가상환경 설정을 추천합니다.
5. user.py 파일을 열어 편집합니다.

```python
login_info = {
    'id': "your_id",    # 본인의 전남대학교 포털 ID를 입력합니다.
    'pw': "your_pw"     # 본인의 전남대학교 포털 비밀번호를 입력합니다.
}
# 아이디 또는 비밀번호가 잘못 설정되었을 경우, 프로그램이 도중에 종료됩니다.
```

```python
class_name = "your_class"   # 자동재생을 원하는 과목명을 입력합니다.
# 존재하지 않는 과목명을 입력했을 경우, 프로그램이 종료됩니다.

start_lecture_name = "start_lecture_name"   # 첫번째로 재생하고 싶은 과목명을 입력합니다.
# 존재하지 않는 강의명을 입력했을 경우, 프로그램이 종료됩니다.
# 기본값으로 두거나, 공백으로 설정했을 경우 첫번째 강의부터 재생합니다.
```

6. 터미널에 `python main.py`를 입력해 main.py 파일을 실행합니다.
7. 잠시 후 Chrome 브라우저가 실행되고, 자동으로 강의를 재생합니다.

---

## 이슈

-   설정에서 입력하는 개인정보는 전남대학교 전산시스템 외 타 경로로 전송되지 않습니다.
-   이 프로그램의 사용으로 인한 책임은 사용자에게 있습니다.

---

## 변경사항

-   `v1.0`: GUI 없이 커맨드라인으로 실행하는 버전입니다. 기본적인 기능만 갖추고 있습니다.
    -   강의 자동 재생 - 시작하기 원하는 강의를 설정할 수 없습니다.
