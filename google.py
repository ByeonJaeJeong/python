'''
    Thread 를 이용해 같은 함수로 사용하면서 따로 작업할수 있게 할예정
'''
#라이브러리 import
from tkinter import filedialog
import tkinter.ttk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
import time
import os
import tkinter as tk
import threading,queue
#검색프레임 부터 들고옴
class SearchFrame(tk.Tk):
    # define
    driver=''
    images=''
    outPath=''
    keyName=''

    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("320x150+100+100")
        self.title("이미지 검색 툴")
        self.resizable(False, False)

        # 프레임 나누기
        searchframe = tk.Frame(self, relief="solid", width="320", height="300")
        searchframe.pack(side="top", fill="both", expand=True)
        # 이미지 저장 경로
        self.pathEntry = tk.Entry(searchframe, bd=5, width=30)
        pathLabel = tk.Label(searchframe, text="저장할 경로 :")
        pathLabel.grid(column=0, row=0, padx=5)
        self.pathEntry.bind("<Button-1>", self.get_file_path)
        self.pathEntry.grid(column=1, row=0, columnspan=2, pady=5)

        # 검색내용
        searchLabel = tk.Label(searchframe, text="검색할 내용 : ")
        searchLabel.grid(column=0, row=1)
        self.searchEntry = tk.Entry(searchframe, bd=5)
        self.searchEntry.grid(column=1, row=1)
        searchButton = tk.Button(searchframe, text="검색", width=8, command=self.start_crawling)
        searchButton.grid(column=2, row=1)
        # 저장하기 버튼
        self.saveButton = tk.Button(searchframe, text="저장하기", width="40", command=self.save_button)
        self.saveButton.grid(column=0, row=2, columnspan=4, pady=10, padx=10)

        progressframe = tk.Frame(self, relief="solid", width="320", height="20")
        progressframe.pack(side="bottom")
        self.progressLabel = tk.Label(progressframe, text="0")
        self.progressLabel.grid(column=17, row=0)
        progressbar = tk.Label(progressframe, text="/")
        progressbar.grid(column=18, row=0)
        self.progressmaxLabel = tk.Label(progressframe, text="0")
        self.progressmaxLabel.grid(column=19, row=0)
        self.progressbar = tk.ttk.Progressbar(progressframe, maximum=2000, length=320)
        self.progressbar.grid(column=0, row=1, columnspan=20)

    def get_file_path(self, event):

        filePath = filedialog.askdirectory(initialdir="/", title='Please select a directory')
        self.pathEntry.delete(0, "end")
        self.pathEntry.insert(0, filePath)

    def start_crawling(self):
        global keyName
        keyName = self.searchEntry.get()
        global outPath
        outPath = self.pathEntry.get()
        q = queue.Queue()
        t1 = threading.Thread(target=SearchFrame.crawling, args=(keyName, q), daemon=True)
        t2 = threading.Thread(target=SearchFrame.splash, args=(self, t1,q), daemon=True)
        t1.start()
        t2.start()


    def splash(self, t, q):
        toplevel = tk.Toplevel(self)
        print("작동1")
        toplevel.geometry("350x200+100+100")
        toplevel.overrideredirect(True)

        frameCnt = 22
        frames = [tk.PhotoImage(file='img/332.gif', format='gif -index %i' % (i)) for i in range(frameCnt)]

        def update(ind):
            frame = frames[ind % frameCnt]
            ind += 1
            label.configure(image=frame)
            if not t.is_alive():
                self.progress_max(q.get())
                toplevel.destroy()
            toplevel.after(100, update, ind)

        label = tk.Label(toplevel)
        label.pack()
        toplevel.after(0, update, 0)




    #다운로드 한 벨류값을 저장
    def donwload_value(self, idx):
        self.progressLabel.configure(text=idx)
        self.progressbar['value'] = idx
        self.progressbar.update()
    #검색해서 총갯수를 업데이트
    def progress_max(self, length):
        print(length)
        self.progressmaxLabel.configure(text=length)
        self.progressbar.configure(maximum=length)
    #저장버튼 클릭 event

    def save_button(self):
        outPath = self.pathEntry.get()
        KeyName= self.searchEntry.get()
        #버튼 중지하기 버튼으로 변경
        self.saveButton.configure(text="중지하기", command=self.stop_button())
        alive=True
        # 폴더 생성
        if not os.path.isdir(outPath + "/" + keyName):  # 폴더 존재하지 않으면 생성
            os.makedirs(outPath + "/" + keyName)
        # download
        for idx, image in enumerate(images):
            image.click()
            driver.implicitly_wait(20)

            imgUrl = driver.find_element_by_css_selector('.n3VNCb').get_attribute('src')
            urllib.request.urlretrieve(imgUrl, outPath + "/" + keyName + "/" + str(idx+1) + ".jpg")
            SearchFrame.donwload_value(self, idx+1)

    #크롤링 이벤트
    def stop_button(self):
        alive=False
        #self.saveButton.configure(text="저장하기", command=self.save_button())
    def crawling(name, q):
        #스크롤 이벤트

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        global driver
        driver = webdriver.Chrome()
        driver.get("http://www.google.co.kr/imghp?hl=ko&tab=wi&ogbl")
        elem = driver.find_element_by_name("q")
        # 검색명

        elem.send_keys(name)
        elem.send_keys(Keys.RETURN)
        # 스크롤
        def scroll(driver):
            SCROLL_PAUSE_TIME = 1

            # Get scroll height
            last_height = driver.execute_script("return document.body.scrollHeight")

            while True:
                # Scroll down to bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)
                # driver.implicitly_wait(20)
                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")
                # 내린후 스크롤과 현재스크롤 비교
                if new_height == last_height:
                    try:
                        # 더보기 클릭 오류나면 종료
                        driver.find_element_by_css_selector('.mye4qd').click()
                        continue
                    except:
                        print("스크롤 끝")
                    break
                last_height = new_height
        scroll(driver)

        # 이미지 위치정보
        global images
        images = driver.find_elements_by_css_selector('.isv-r.PNCib.MSM1fd.BUooTd')
        print("스레드종료 반환값 : "+str(len(images)))
        q.put(len(images))


#메인루프 시작
if __name__ == "__main__":
    app = SearchFrame()
    app.mainloop()