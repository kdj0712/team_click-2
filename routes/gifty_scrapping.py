# 웹스크롤링을 위한 코드로 크롤링 이외의 상황에 사용되지는 않음

from selenium import webdriver

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# mongodb 연결
from pymongo import MongoClient
mongoclient = MongoClient("mongodb://192.168.10.235:27017")
database = mongoclient['click_tech']
coll = database['gifty_info']

browser = webdriver.Chrome()
browser.get(str("https://www.giftishow.com/brand/brandList.mhows"))

coll.delete_many({})

# 각 항목에 대한 요소들
list_element = browser.find_elements(by=By.CSS_SELECTOR, value="#swiperWrapper > li")
for style_list in list_element[1:] :
    # 항목 클릭하기
    style_list.find_element(by=By.CSS_SELECTOR, value="li > a").click()
    gifty_style = style_list.find_element(by=By.CSS_SELECTOR, value="#swiperWrapper > li > a > p").text # 스타일

    # 마지막까지 스크롤하기
    element_body = browser.find_element(by=By.CSS_SELECTOR, value="body")
    previous_scrollHeight = 0
    while True : 
        element_body.send_keys(Keys.END)

        current_scrollHeight = browser.execute_script("return document.body.scrollHeight")
        if previous_scrollHeight >= current_scrollHeight:
            break
        else : 
            previous_scrollHeight = current_scrollHeight
            time.sleep(1)
    
    # 아이템 선택해서 저장하기

    gifty_list = browser.find_elements(by=By.CSS_SELECTOR, value="#goodsSection > li ")
    for gifty in gifty_list :
        try : 
            gifty.find_element(by=By.CSS_SELECTOR, value="#goodsSection > li > a").click()
            browser.implicitly_wait(10)
            # wait = WebDriverWait(browser, 2)
            # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.txtWrap > div.txtWrap-min > div.itemPrice")))
            # 데이터 뽑아오기
            gifty_image =  browser.find_element(by=By.CSS_SELECTOR, value="#renewal > div.itemDetail.comp > div > div.imgWrap > img").get_attribute('src') #이미지
            gifty_brand = browser.find_element(by=By.CSS_SELECTOR, value="div.txtWrap-min > a > div > span").text #브랜드
            gifty_name =  browser.find_element(by=By.CSS_SELECTOR, value="div.txtWrap > div.txtWrap-min > div.itemNm").text #제품 이름
            gifty_price =  browser.find_element(by=By.CSS_SELECTOR, value="div.txtWrap-min > div.itemPrice > span").text #가격

            # 상세 정보 이미지
            gifty_detail = browser.find_element(by=By.CSS_SELECTOR, value="#cont1 > pre").text

            #주의사항
            browser.find_element(by=By.CSS_SELECTOR, value="div.detailtabArea > div:nth-child(1) > div > div:nth-child(2)").click()
            gifty_caution = browser.find_element(by=By.CSS_SELECTOR, value="#cont2 > p").text # 주의사항 저장
            
            coll.insert_one({'gifty_style' : gifty_style, 'gifty_image' : gifty_image, 'gifty_brand' : gifty_brand, 'gifty_name' : gifty_name, 'gifty_price' : gifty_price,'gifty_detail' : gifty_detail, 'gifty_cautioin' : gifty_caution})

            browser.back()
            browser.implicitly_wait(10)
        except NoSuchElementException :
            pass






