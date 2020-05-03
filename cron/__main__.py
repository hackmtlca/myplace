from selenium import webdriver
import random
import jwt
import time

def visit_as_random_user():
    chrome_options=webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("window-size=640,480") 
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("user-data-dir=selenium")
    browser = webdriver.Chrome(chrome_options=chrome_options)

    def loop():
        browser.get('http://server/api/users/random/Dn92meSg5p')
        time.sleep(1)
        loop()

    loop()

if __name__ == '__main__':
    visit_as_random_user()