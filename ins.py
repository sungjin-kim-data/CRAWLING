from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import getpass
import requests
import pymysql
import pandas as pd

browser = webdriver.Chrome("./chromedriver.exe")
browser.set_window_position(0,0)
browser.set_window_size(1920, 1000)

browser.get("https://www.instagram.com/accounts/login/")
browser.maximize_window()

# username = getpass.getpass("Input ID : ") #User ID
# password = getpass.getpass("Input PWD : ") #User PWD

# insta ID, PW
instagram_id = '{USERID}'
instagram_pw = '{PASSWORD}'

# 데이터 저장할 인플루언서 ID
_keyword_id = '{INFLUENCERID}'

time.sleep(200)

_id = browser.find_element(By.NAME, 'username')
_id.send_keys(instagram_id)
time.sleep(2)

_password = browser.find_element(By.NAME, 'password')
_password.send_keys(instagram_pw)
time.sleep(2)

# 로그인 버튼 클릭
login_button = browser.find_element(By.CSS_SELECTOR, '.sqdOP.L3NKy.y3zKF')
login_button.click()
time.sleep(7)

# 나중에 하기(정보 저장)
browser.find_element(By.CSS_SELECTOR, 'div.cmbtv').click()

time.sleep(4)

# 나중에 하기(알림 받기)
browser.find_element(By.CSS_SELECTOR, '._a9--._a9_1').click()
time.sleep(4)

# 업로드 한 계정 접속
browser.get('https://www.instagram.com/' + _keyword_id + '/')
time.sleep(5)

insta_dict = {
    'id': [],
    'date': [],
    'like': [],
    'text': [],
    'hashtag': []
}

first_post = browser.find_element(By.CSS_SELECTOR, 'div._aagw')
first_post.click()

seq = 0
start = time.time()

while True:
    try:
        if browser.find_element(By.CSS_SELECTOR, 'button._abl-'):
            if seq % 20 == 0:
                print('{}번째 수집 중'.format(seq), time.time() - start, sep='\t')

            ## id 정보 수집
            try:
                info_id = browser.find_element(By.CSS_SELECTOR, 'a.oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9').text
                insta_dict['id'].append(info_id)
            except:
                info_id = browser.find_element(By.CSS_SELECTOR, 'a.oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9').text.split()[0]
                insta_dict['id'].append(info_id)

            ## 시간정보 수집
            date = browser.find_element(By.XPATH, '//*[@id="mount_0_0_BL"]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[3]/div/div/div[2]/div/div/a/div/time').get_attribute(
                'datetime')

            ## like 정보 수집
            try:
                browser.find_element(By.CSS_SELECTOR, 'button.sqdOP.yWX7d._8A5w5')
                like = browser.find_element(By.CSS_SELECTOR, 'button.sqdOP.yWX7d._8A5w5').text
                insta_dict['like'].append(like)

            except:
                insta_dict['like'].append('영상')

            ##text 정보수집
            raw_info = browser.find_element(By.CSS_SELECTOR, 'div.C4VMK').text.split()
            text = []
            for i in range(len(raw_info)):
                ## 첫번째 text는 아이디니까 제외
                if i == 0:
                    pass
                ## 두번째부터 시작
                else:
                    if '#' in raw_info[i]:
                        pass
                    else:
                        text.append(raw_info[i])
            clean_text = ' '.join(text)
            insta_dict['text'].append(clean_text)

            ##hashtag 수집
            raw_tags = browser.find_elements(By.CSS_SELECTOR, 'a.xil3i')
            hash_tag = []
            for i in range(len(raw_tags)):
                if raw_tags[i].text == '':
                    pass
                else:
                    hash_tag.append(raw_tags[i].text)

            insta_dict['hashtag'].append(hash_tag)

            seq += 1

            if seq == 10:
                break

            browser.find_element(By.CSS_SELECTOR, 'button._abl-').click()
            time.sleep(1.5)


        else:
            break

    except:
        browser.find_element(By.CSS_SELECTOR, 'button._abl-').click()
        time.sleep(2)

test = pd.DataFrame.from_dict(insta_dict)

time.sleep(3)

test.head()

# browser.close()