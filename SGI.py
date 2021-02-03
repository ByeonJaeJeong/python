from tkinter import filedialog
from tkinter import messagebox
import tkinter.ttk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
import time
import os
import tkinter as tk
import threading,queue

class MainFrame(tk.Tk):
    driver = None
    images = ''
    q = ''
    save_active=True
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("500x300+100+100")
        self.title("이미지 검색 툴")
        #저장위치 프레임
        saveFrame=tk.LabelFrame(self, text="저장위치설정", relief="solid", width="500", height="100", bd=1)
        saveFrame.pack(side="top", fill="both", expand=False, padx=5, pady=2)

        #위치 적히는 entry
        self.pathEntry = tk.Entry(saveFrame, bd=2, width=60)
        self.pathEntry.insert(0, os.path.dirname(__file__)[:-6])
        self.pathEntry.configure(state="readonly")
        self.pathEntry.pack(side="left", anchor="center", pady=7,padx=10)

        self.pathButton=tk.Button(saveFrame, command=self.path_click, text="...", width="3")
        self.pathButton.pack(side="left")
        #검색하는 프레임
        searchFrame=tk.LabelFrame(self, text="검색 옵션", relief="solid", width="500", height="200", bd=1)
        searchFrame.pack(side="top", fill="both", expand=False, padx=5, pady=2)

        attribute_Frame=tk.Frame(searchFrame, width="500")
        attribute_Frame.pack(side="top",fill="both", expand=True, padx=5, pady=10)
        #검색 속성
        #Img Size
        self.size_combobox=tk.ttk.Combobox(attribute_Frame, width=10, state="readonly", values=[
            "모든 크기", "큼", "중간", "아이콘"
        ])
        self.size_combobox.grid(column=0, row=0, padx=10, pady=5)
        self.size_combobox.current(0)
        #색상 빨주노초파남보분흰흑검갈
        self.color_combobox=tk.ttk.Combobox(attribute_Frame, width=10, state="readonly", values=[
            "모든 색상", "흑백", "투명", "빨강색", "주황색", "노랑색", "초록색",
            "청록색", "파랑색", "보라색", "분홍색", "흰색", "회색", "검정색", "갈색"
        ])

        self.color_combobox.grid(column=1, row=0, padx=10, pady=5)
        self.color_combobox.current(0)
        #유형 클립아트 선화 gif
        self.type_combobox=tk.ttk.Combobox(attribute_Frame, width=10, state="readonly",values=[
            "모든 유형", "클립아트", "선화", "GIF"
        ])
        self.type_combobox.grid(column=2, row=0, padx=10, pady=5)
        self.type_combobox.current(0)
        #기간 1일 , 1주 1달 1년
        self.time_combobox=tk.ttk.Combobox(attribute_Frame, width=10, state="readonly", values=[
            "모든 시간", "1일", "1주", "1달", "1년"
        ])
        self.time_combobox.grid(column=3, row=0, padx=10, pady=5)
        self.time_combobox.current(0)

        search_btnFrame=tk.Frame(searchFrame, width=500, height=50, relief="solid")
        search_btnFrame.pack(side="top", fill="both", expand=False, padx=5, pady=10)
        #검색창
        self.search_Entry=tk.Entry(search_btnFrame, width=45, bd=2)
        self.search_Entry.pack(side="left",padx=3)

        #정지버튼
        self.search_stopButton = tk.Button(search_btnFrame, text="정지", width="8", state=tk.DISABLED, command=self.search_stop_event)
        self.search_stopButton.pack(side="right", padx=3)
        #검색버튼
        self.search_startButton = tk.Button(search_btnFrame, text="검색", width="8", command=self.search_event)
        self.search_startButton.pack(side="right", padx=3)



        #진행상태 프레임
        stateFrame=tk.LabelFrame(self, text="상태", relief="solid", width="500", height="100", bd=1)
        stateFrame.pack(side="top", fill="both", expand=False, padx=5, pady=2, ipadx=2, ipady=2)
        #프로그레스 바
        self.progressbar = tk.ttk.Progressbar(stateFrame, maximum=2000, length=480)
        self.progressbar.grid(column=0, row=1, columnspan=20, pady=5, padx=5)
        #현재진행정도
        self.progressLabel=tk.Label(stateFrame,text="0")
        self.progressLabel.grid(column=0,row=0)
        #언더바
        underbarLabel=tk.Label(stateFrame,text="/")
        underbarLabel.grid(column=1,row=0)
        #전체 사진수
        self.progressMaxLabel=tk.Label(stateFrame,text="0")
        self.progressMaxLabel.grid(column=2,row=0)
        #시작 정지 버튼 프레임
        actionFrame=tk.Frame(self, relief="solid", width="500", height="50")
        actionFrame.pack(side="top", fill="both", expand=False, padx=4, pady=10)
        # 중지 버튼
        self.stopButton = tk.Button(actionFrame, text="정지", width="8", state=tk.DISABLED, command=self.download_stop)
        self.stopButton.pack(side="right", padx=3)
        # 시작 버튼
        self.startButton = tk.Button(actionFrame, text="다운로드", width="8", command=self.down_action)
        self.startButton.pack(side="right", padx=3, anchor="s")

    #저장위치 설정 클릭시 event 처리
    def path_click(self):
        filePath = filedialog.askdirectory(initialdir="/", title='Please select a directory')
        self.pathEntry.configure(state=tk.NORMAL)
        if not filePath =='':
            self.pathEntry.delete(0, "end")
            self.pathEntry.insert(0, filePath)
        self.pathEntry.configure(state="readonly")
    #검색 속성 가져오기
    def search_stop_event(self):
        global driver
        driver.quit()
        self.search_startButton.configure(state=tk.NORMAL)
        self.search_stopButton.configure(state=tk.DISABLED)

    def search_event(self):
        #옵션값
        size = self.size_combobox.get()
        color = self.color_combobox.get()
        type = self.type_combobox.get()
        _time = self.time_combobox.get()
        #검색할 내용
        search_name = self.search_Entry.get()
        #결과를 확인하기 위한 Queue
        q = queue.Queue()

        crawling_t = threading.Thread(target=MainFrame.crawling, args=(self,search_name, size, color, type, _time, q), daemon=True)
        crawling_t.start()
        self.search_startButton.configure(state=tk.DISABLED)
        self.search_stopButton.configure(state=tk.NORMAL)
    def crawling(self,name, size, color, type, _time, q):
        #옵션값 dict
        size_dict={"모든 크기": "", "큼": "isz:l", "중간": "isz:m", "아이콘": "isz:i"}
        type_dict={"모든 유형": "" , "클립아트": "itp:clipart%2C", "선화": "itp:lineart%2C", "GIF": "itp:animated%2C"}
        time_dict={"모든 시간": "", "1일": "qdr:d%2C", "1주": "qdr:w%2C", "1달": "qdr:m%2C", "1년": "qdr=y%2C"}
        color_dict={"모든 색상": "", "흑백": "ic:gray%2C" , "투명": "ic:trans%2C", "빨강색": "ic:specific%2Cisc:red%2C", "주황색": "ic:specific%2Cisc:orange%2C",
                    "노랑색": "ic:specific%2Cisc:yellow%2C", "초록색": "ic:specific%2Cisc:green%2C", "파랑색": "ic:specific%2Cisc:blue%2C",
                    "청록색": "ic:specific%2Cisc:teal%2C", "보라색": "ic:specific%2Cisc:purple%2C", "분홍색": "ic:specific%2Cisc:pink%2C",
                    "흰색": "white%2C", "회색": "ic:specific%2Cisc:gray%2C", "검정색": "ic:specific%2Cisc:black%2C", "갈색": "ic:specific%2Cisc:brown%2C"}
        #스크롤 이벤트
        options = webdriver.ChromeOptions()
        #options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")

        global driver
        driver = webdriver.Chrome(options=options)
        pageUrl="http://www.google.co.kr/search?q="+name+"&tbm=isch&hl=ko&tbs="+color_dict[color]+time_dict[_time]+type_dict[type]+size_dict[size]
        result = pageUrl[len(pageUrl)-3:len(pageUrl)]
        if result == "%2C":
            pageUrl=pageUrl[:-3]
        driver.get(pageUrl)

        # 검색명




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
        self.progressMaxLabel.configure(text=str(len(images)))
        self.search_startButton.configure(state=tk.NORMAL)
        self.search_stopButton.configure(state=tk.DISABLED)
        self.progressbar.configure(maximum=len(images))
        self.progressLabel.configure(text="0")
        self.progressbar['value']=0
        messagebox.showinfo("검색완료","총파일수 : "+str(len(images)))
    def down_action(self):
        outPath = self.pathEntry.get()
        keyName = self.search_Entry.get()
        down_t=threading.Thread(target=MainFrame.download, args=(self,outPath,keyName), daemon=True)
        down_t.start()
    def download_stop(self):
        global save_active
        save_active=False

    def download(self,outPath,keyName):

        print("save btn action 실행")
        q = queue.Queue()
        # 버튼 중지하기 버튼으로 변경
        self.startButton.configure(state=tk.DISABLED)
        self.stopButton.configure(state=tk.NORMAL)
        try:
            global save_active
            save_active = True
            # 폴더 생성
            if not os.path.isdir(outPath + "/" + keyName):  # 폴더 존재하지 않으면 생성
                os.makedirs(outPath + "/" + keyName)
            # download
            for idx, image in enumerate(images):
                if save_active == False:
                    return
                image.click()
                driver.implicitly_wait(20)

                imgUrl = driver.find_element_by_css_selector('.n3VNCb').get_attribute('src')
                urllib.request.urlretrieve(imgUrl, outPath + "/" + keyName + "/" + str(idx + 1) + ".jpg")
                self.progressLabel.configure(text=idx + 1)
                self.progressbar['value'] = idx + 1
                self.progressbar.update()
        except:
            return -1
        finally:
            self.startButton.configure(state=tk.NORMAL)
            self.stopButton.configure(state=tk.DISABLED)








#메인루프
if __name__ == "__main__":
    try:
        app = MainFrame()
        app.mainloop()
        app.driver.quit()
    except:
        print("정상종료 실패")