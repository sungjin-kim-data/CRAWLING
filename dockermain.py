from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

browser = webdriver.Remote(" http://172.17.0.2:4444/wb/hub", DesiredCapabilities.CHROME)
browser.get("https://naver.com")
print(browser.title)
browser.close()