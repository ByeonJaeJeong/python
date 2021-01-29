from tkinter import filedialog, TOP, BOTH, YES
import tkinter.ttk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
import time
import os
import tkinter as tk
import threading



class SearchFrame(tk.Tk):
    #define
    crawling = ''
    splash=''
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("320x150")
        self.title("이미지 검색 툴")
        self.resizable(False, False)


        #프레임 나누기
        searchframe=tk.Frame(self,relief="solid", width="320", height="300")
        searchframe.pack(side="top",fill="both",expand=True)
        # 이미지 저장 경로
        self.pathEntry = tk.Entry(searchframe, bd=5, width=30 )
        pathLabel = tk.Label(searchframe, text="저장할 경로 :")
        pathLabel.grid(column=0, row=0, padx=5)
        self.pathEntry.bind("<Button-1>", self.get_file_path)
        self.pathEntry.grid(column=1, row=0, columnspan=2,pady=5)

        # 검색내용
        searchLabel = tk.Label(searchframe, text="검색할 내용 : ")
        searchLabel.grid(column=0, row=1)
        self.searchEntry = tk.Entry(searchframe, bd=5)
        self.searchEntry.grid(column=1, row=1)
        searchButton = tk.Button(searchframe, text="검색", width=8, command=self.start_crawling)
        searchButton.grid(column=2, row=1)
        #저장하기 버튼
        saveButton = tk.Button(searchframe,text="저장하기", width="40" ,command=self.save_button)
        saveButton.grid(column=0, row=2, columnspan=4, pady=10,padx=10)


        progressframe=tk.Frame(self, relief="solid", width="320", height="20")
        progressframe.pack(side="bottom")
        self.progressLabel = tk.Label(progressframe,text="0")
        self.progressLabel.grid(column=17,row=0)
        progressbar = tk.Label(progressframe, text="/")
        progressbar.grid(column=18, row=0)
        self.progressmaxLabel = tk.Label(progressframe, text="0")
        self.progressmaxLabel.grid(column=19, row=0)
        self.progressbar =tk.ttk.Progressbar(progressframe, maximum=2000,length=320)
        self.progressbar.grid(column=0, row=1, columnspan=20)


    def get_file_path(self,event):
        filePath = filedialog.askdirectory(initialdir="/", title='Please select a directory')
        self.pathEntry.delete(0, "end")
        self.pathEntry.insert(0, filePath)

    def start_crawling(self):
        name = self.searchEntry.get()
        path = self.pathEntry.get()
        self.crawling = Crawling(self, name, path)
        #idx=self.crawling.start()
        splash = Splash(self)


        #self.crawling.join()

        #self.progress_max(idx)



    def donwload_value(self,idx):
        self.progressLabel.configure(text=idx)
        self.progressbar['value']=idx
        self.progressbar.update()
    def progress_max(self,length):
        print(length)
        self.progressmaxLabel.configure(text=length)
        self.progressbar.configure(maximum=length)
        #self.splash.destroy()
    def save_button(self):
        self.crawling.download(self)



#스플레쉬 화면
class Splash(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.title("검색중")

        def update(x):
            img = tk.PhotoImage(file='img/giphy.gif', format='gif -index ' + str(x), )
            x += 1
            if x > 32: x = 0
            label.configure(image=img)
            label.img = img
            self.after(32, update, x)


        label=tk.Label(self)
        label.pack()
        self.after(0,update,0)

        ## required to make window show before the program gets to the mainloop
        self.mainloop()


class Crawling(threading.Thread):
    driver=''
    images=''
    # keyName = "갱플랭크"
    # outPath = ""  # 이미지 저장폴더
    def __init__(self,parent, key, path):
        threading.Thread.__init__(self)
        self.parent=parent
        self.keyName = key
        self.outPath = path

    '''
    #검색어 패스 변경 메소드
    def setKey(self,Name,path):
        self.keyName=Name
        self.outPath=path
    '''

    # 프로그램 시작
    def run(self) ->int:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        global driver
        driver = webdriver.Chrome()
        driver.get("http://www.google.co.kr/imghp?hl=ko&tab=wi&ogbl")
        elem = driver.find_element_by_name("q")
        # 검색명

        elem.send_keys(self.keyName)
        elem.send_keys(Keys.RETURN)
        #스크롤
        self.scroll(driver)

        # 이미지 위치정보
        global images
        images = driver.find_elements_by_css_selector('.isv-r.PNCib.MSM1fd.BUooTd')
        # 반복문 시작
        #SearchFrame.progressbar_max(len(images))
        print(len(images))
        return len(images)


        # 드라이버 종료
        #driver.quit()

    def download(self,frame):
        # 폴더 생성
        if not os.path.isdir(self.outPath + "/" + self.keyName):  # 폴더 존재하지 않으면 생성
            os.makedirs(self.outPath + "/" + self.keyName)
        #download
        for idx, image in enumerate(images):
            image.click()
            driver.implicitly_wait(20)

            imgUrl = driver.find_element_by_css_selector('.n3VNCb').get_attribute('src')
            urllib.request.urlretrieve(imgUrl, self.outPath + "/" + self.keyName + "/" + str(idx) + ".jpg")
            SearchFrame.donwload_value(frame,idx)


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
