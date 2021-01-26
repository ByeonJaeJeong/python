from tkinter import filedialog
import tkinter.ttk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
import time
import os
import tkinter as tk
import threading
import queue




class SearchFrame(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("320x150")
        self.title("이미지 검색 툴")
        self.resizable(False, False)
        #프레임 나누기
        searchframe=tk.Frame(self,relief="solid", width="320", height="300")
        searchframe.pack(side="top",fill="both",expand=True)
        # 이미지 저장 경로
        self.pathEntry = tk.Entry(searchframe, bd=5, width=30)
        self.pathLabel = tk.Label(searchframe, text="저장할 경로 :")
        self.pathLabel.grid(column=0, row=0)
        self.pathEntry.bind("<Button-1>", self.get_file_path)
        self.pathEntry.grid(column=1, row=0, columnspan=2)

        # 검색내용
        self.searchLabel = tk.Label(searchframe, text="검색할 내용 : ")
        self.searchLabel.grid(column=0, row=1)
        self.searchEntry = tk.Entry(searchframe, bd=5)
        self.searchEntry.grid(column=1, row=1)
        self.searchButton = tk.Button(searchframe, text="검색", width=8, command=self.start_crawling)
        self.searchButton.grid(column=2, row=1)
        progressframe=tk.Frame(self, relief="solid", width="320", height="20")
        progressframe.pack(side="bottom")
        self.max=100
        self.progressbar=tk.ttk.Progressbar(progressframe, maximum=2000,length=320)
        self.progressbar.grid(column=0, row=0)


    def get_file_path(self,event):
        filePath = filedialog.askdirectory(initialdir="/", title='Please select a directory')
        self.pathEntry.delete(0, "end")
        self.pathEntry.insert(0, filePath)

    def start_crawling(self):
        self.queue=queue.Queue()
        name = self.searchEntry.get()
        path = self.pathEntry.get()
        crawling=Crawling(self.queue,name, path)
        crawling.run()
    def progressbar_update(idx):
        SearchFrame.progressbar['value']=idx
        SearchFrame.progressbar.update()
        print(SearchFrame.progressbar['value'])
    def progressbar_max(max):
        SearchFrame.max=max

class Crawling(threading.Thread):
    # keyName = "갱플랭크"
    # outPath = ""  # 이미지 저장폴더
    def __init__(self,q, key, path):
        threading.Thread.__init__(self)
        self.__queue = q
        self.keyName = key
        self.outPath = path

    '''
    #검색어 패스 변경 메소드
    def setKey(self,Name,path):
        self.keyName=Name
        self.outPath=path
    '''

    # 프로그램 시작
    def run(self):
        driver = webdriver.Chrome()
        driver.get("http://www.google.co.kr/imghp?hl=ko&tab=wi&ogbl")
        elem = driver.find_element_by_name("q")
        # 검색명

        elem.send_keys(self.keyName)
        elem.send_keys(Keys.RETURN)
        #스크롤
        self.scroll(driver)
        # 폴더 생성

        if not os.path.isdir(self.outPath + "/" + self.keyName):  # 폴더 존재하지 않으면 생성
            os.makedirs(self.outPath + "/" + self.keyName)
        # 이미지 위치정보
        images = driver.find_elements_by_css_selector('.isv-r.PNCib.MSM1fd.BUooTd')
        # 반복문 시작
        SearchFrame.progressbar_max(len(images))
        for idx, image in enumerate(images):
            SearchFrame.progressbar_update(idx)
            image.click()
            driver.implicitly_wait(20)
            imgUrl = driver.find_element_by_css_selector('.n3VNCb').get_attribute('src')
            urllib.request.urlretrieve(imgUrl, self.outPath + "/" + self.keyName + "/" + str(idx) + ".jpg")

        # 드라이버 종료
        driver.quit()



    def scroll(self,driver):
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



if __name__ == "__main__":
    app = SearchFrame()
    app.mainloop()
