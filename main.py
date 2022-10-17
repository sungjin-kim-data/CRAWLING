from selenium import webdriver
import time

browser = webdriver.Chrome("./chromedriver")
browser.get("https://naver.com/")
url_list = []
content_list = ""
text = "마녀2 리뷰"

for i in range(1, 100):
    url = 'https://search.naver.com/search.naver?query=%EB%A7%88%EB%85%802%20%EB%A6%AC%EB%B7%B0&nso=&where=view&sm=tab_nmr&mode=normal'
    browser.get(url)
    time.sleep(0.5)

    for j in range(1, 3): # 각 블로그 주소 저장
        titles = browser.find_element("xpath", '/html/body/ui-view/div/main/div/div/section/div[2]/div['+str(j)+']/div/div[1]/div[1]/a[1]')
        title = titles.get_attribute('href')
        url_list.append(title)


print("url 수집 끝, 해당 url 데이터 크롤링")

browser.switch_to.frame('mainFrame')
overlays = ".se-component.se-text.se-l-default"  # 내용 크롤링
contents = browser.find_elements("selector", overlays)

for content in contents:
    content_list = content_list + content.text  # content_list 라는 값에 + 하면서 점점 누적

time.sleep(10)
browser.close()