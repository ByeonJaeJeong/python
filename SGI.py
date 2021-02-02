from tkinter import filedialog
import tkinter.ttk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
import time
import os
import tkinter as tk
import threading,queue

class MainFrame(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("500x300+100+100")
        self.title("이미지 검색 툴")

        #저장위치 프레임
        saveFrame=tk.LabelFrame(self, text="저장위치설정", relief="solid", width="500", height="100", bd=1)
        saveFrame.pack(side="top", fill="both", expand=False, padx=5, pady=2,)

        #위치 적히는 entry
        pathEntry = tk.Entry(saveFrame, bd=2, width=60)
        pathEntry.pack(pady=5)

        #검색하는 프레임
        searchFrame=tk.LabelFrame(self, text="검색 옵션", relief="solid", width="500", height="200", bd=1)
        searchFrame.pack(side="top", fill="both", expand=False, padx=5, pady=2)

        attribute_Frame=tk.Frame(searchFrame, width="500")
        attribute_Frame.pack(side="top",fill="both", expand=True, padx=5, pady=10)
        #검색 속성
        #Img Size
        size_combobox=tk.ttk.Combobox(attribute_Frame, width=10, state="readonly", values=[
            "모든크기", "큼", "중간", "아이콘"
        ])
        size_combobox.grid(column=0, row=0, padx=10, pady=5)
        size_combobox.current(0)
        #색상 빨주노초파남보분흰흑검갈
        color_combobox=tk.ttk.Combobox(attribute_Frame, width=10, state="readonly", values=[
            "모든색상", "흑백", "투명", "빨강", "주황", "노랑", "초록",
            "파랑", "남색", "보라색", "분홍색", "흰색", "회색", "검정색", "갈색"
        ])

        color_combobox.grid(column=1, row=0, padx=10, pady=5)
        color_combobox.current(0)
        #유형 클립아트 선화 gif
        type_combobox=tk.ttk.Combobox(attribute_Frame, width=10, state="readonly",values=[
            "모든유형", "클립아트", "선화", "GIF"
        ])
        type_combobox.grid(column=2, row=0, padx=10, pady=5)
        type_combobox.current(0)
        #기간 1일 , 1주 1달 1년
        time_combobox=tk.ttk.Combobox(attribute_Frame, width=10, state="readonly", values=[
            "모든시간", "1시간", "1일", "1달", "1년"
        ])
        time_combobox.grid(column=3, row=0, padx=10, pady=5)
        time_combobox.current(0)

        search_btnFrame=tk.Frame(searchFrame, width=500, height=50, relief="solid")
        search_btnFrame.pack(side="top", fill="both", expand=False, padx=5, pady=10)
        #검색버튼
        search_stopButton = tk.Button(search_btnFrame, text="정지", width="8", state=tk.DISABLED)
        search_stopButton.pack(side="right", padx=3)
        #중지버튼
        search_startButton = tk.Button(search_btnFrame, text="검색", width="8")
        search_startButton.pack(side="right", padx=3)



        #진행상태 프레임
        stateFrame=tk.LabelFrame(self, text="상태", relief="solid", width="500", height="100", bd=1)
        stateFrame.pack(side="top", fill="both", expand=False, padx=5, pady=2, ipadx=2, ipady=2)
        #프로그레스 바
        progressbar = tk.ttk.Progressbar(stateFrame, maximum=2000, length=480)
        progressbar.grid(column=0, row=1, columnspan=20, pady=5, padx=5)
        #현재진행정도
        progressLabel=tk.Label(stateFrame,text="0")
        progressLabel.grid(column=0,row=0)
        #언더바
        underbarLabel=tk.Label(stateFrame,text="/")
        underbarLabel.grid(column=1,row=0)
        #전체 사진수
        progressMaxLabel=tk.Label(stateFrame,text="0")
        progressMaxLabel.grid(column=2,row=0)
        #시작 정지 버튼 프레임
        actionFrame=tk.Frame(self, relief="solid", width="500", height="50")
        actionFrame.pack(side="top", fill="both", expand=False, padx=4, pady=10)
        # 중지 버튼
        stopButton = tk.Button(actionFrame, text="정지", width="8", state=tk.DISABLED)
        stopButton.pack(side="right", padx=3)
        # 시작 버튼
        startButton = tk.Button(actionFrame, text="다운로드", width="8")
        startButton.pack(side="right", padx=3, anchor="s")





#메인루프
if __name__ == "__main__":
    app = MainFrame()
    app.mainloop()