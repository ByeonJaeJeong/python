from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
import time
import os
def scroll():
    SCROLL_PAUSE_TIME = 1

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        #driver.implicitly_wait(20)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        #내린후 스크롤과 현재스크롤 비교
        if new_height == last_height:
            try:
                #더보기 클릭 오류나면 종료
                driver.find_element_by_css_selector('.mye4qd').click()
                continue
            except:
                print("오류")
            break
        last_height = new_height

driver= webdriver.Chrome()
driver.get("http://www.google.co.kr/imghp?hl=ko&tab=wi&ogbl")
elem=driver.find_element_by_name("q")
#검색명
keyName="갱플랭크"
elem.send_keys(keyName)
elem.send_keys(Keys.RETURN)
scroll()
#폴더 생성
outPath="C:/Users/Jeong/Desktop/" #이미지 저장폴더
if not os.path.isdir(outPath+"/"+keyName): #폴더 존재하지 않으면 생성
    os.makedirs(outPath+"/"+keyName)
#이미지 위치정보
images=driver.find_elements_by_css_selector('.isv-r.PNCib.MSM1fd.BUooTd')
#반복문 시작
for idx,image in enumerate(images):

    image.click()
    driver.implicitly_wait(20)
    imgUrl=driver.find_element_by_css_selector('.n3VNCb').get_attribute('src')
    urllib.request.urlretrieve(imgUrl, outPath+keyName+"/"+str(idx)+".jpg")

#드라이버 종료
driver.quit()


