#!/usr/bin/python
# -*- coding: UTF-8 -*-
import speech_recognition as sr
import webbrowser as wb
import os
import winsound
import win32com.client
import re
import requests
from bs4 import BeautifulSoup



shell = win32com.client.Dispatch("WScript.Shell")   #為了要送快捷鍵   對照表 http://www.361way.com/windows-python-sendkeys/5182.html
r = sr.Recognizer()

def youtube():
    print ("您想搜尋什麼?")
    winsound.PlaySound("audio/google.wav", winsound.SND_FILENAME)
    #winsound.PlaySound("youtube.wav", winsound.SND_FILENAME)
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=10,phrase_time_limit=6)
            qq = r.recognize_google(audio,language='zh-TW')
            print("您所說的話: " + qq)
        if 'homepage' in qq:
            wb.open("https://www.youtube.com/?gl=TW&hl=zh-TW")
            winsound.PlaySound("audio/mission.wav", winsound.SND_FILENAME)
        else:  #這裡搜尋所講的話 並且可以選擇要挑哪個網址開啟
            url_you="https://www.youtube.com/results?search_query=" + qq
            wb.open(url_you)
            winsound.PlaySound("audio/mission.wav", winsound.SND_FILENAME)

            # 這邊把搜尋到的結果網址一個一個揪出來
            res = requests.get(url_you, verify=False)
            soup = BeautifulSoup(res.text, 'html.parser')
            last = None

            myList = []
            for entry in soup.select('a'):  # soup.select('a')得到了很多條網址字串  for每個字串一個一個處理
                m = re.search("v=(.*)", entry['href'])  # 網址篩選條件
                if m:
                    target = m.group(1)  # 這邊引進得到的網址字串
                    if target == last:
                        continue
                    if re.search("list", target):
                        continue
                    last = target
                    myList.append(target)
                    #print(target)

            def you_film():  # 這個FN是用來選影片  #跟you_film不在同一個 def裡面 因此抓不到def
                winsound.PlaySound("audio/choose.wav", winsound.SND_FILENAME)
                try:

                    print("請選擇您要觀看哪一則影片，第一部請說第一部，第二部說第二部以此類推...")
                    with sr.Microphone() as source:
                        r.adjust_for_ambient_noise(source)
                        audio = r.listen(source, timeout=10, phrase_time_limit=5)
                        choose = r.recognize_google(audio, language='zh-TW')
                        print("你所說的話: " + choose)
                        if '一' in choose:
                            wb.open("https://www.youtube.com/watch?v=" + myList[0])
                            print("https://www.youtube.com/watch?v=" + myList[0])
                            print("第一部影片已開啟")

                        elif '二' in choose:
                            wb.open("https://www.youtube.com/watch?v=" + myList[1])
                            print("第二部影片已開啟")

                        elif '三' in choose:
                            wb.open("https://www.youtube.com/watch?v=" + myList[2])
                            print("第二部影片已開啟")

                        elif '四' in choose:
                            wb.open("https://www.youtube.com/watch?v=" + myList[3])
                            print("第二部影片已開啟")

                        elif '五' in choose:
                            wb.open("https://www.youtube.com/watch?v=" + myList[4])
                            print("第二部影片已開啟")

                        elif '關掉' in choose:
                            close1()
                        else:
                            print("對不起我沒聽清楚，請再說一次。")
                            winsound.PlaySound("audio/again.wav", winsound.SND_FILENAME)
                            you_film()

                except:
                    print("對不起我沒聽清楚，麻煩再說一次。")
                    winsound.PlaySound("audio/again.wav", winsound.SND_FILENAME)
                    you_film()

        you_film()


            #print(myList)
            #you_film()  #執行選影片的fn

    except:
        print("我真的聽不懂抱歉，請再說一次。")
        winsound.PlaySound("audio/again.wav", winsound.SND_FILENAME)
        youtube()



def close1():
    browserExe = "chrome.exe"
    os.system("taskkill /f /im " + browserExe)
    print("Chrome已經關閉。")

var = 1

while var == 1:  # 此條件永遠true，將無限循環行下去  可以使用 CTRL+C 來中斷。
    r = sr.Recognizer()


    try:
        with sr.Microphone() as source:
            print("Speak:")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=60,phrase_time_limit=3)

        data = r.recognize_google(audio, language='zh-TW')
        print("您所說的話: " + data )
        if '啟動' in data or 'Google' in data:
            winsound.PlaySound("audio/sound.wav", winsound.SND_FILENAME)
            winsound.PlaySound("audio/jarvis.wav", winsound.SND_FILENAME)
        elif '播放' in data:
            shell.SendKeys("^%{HOME}", 0)
        elif '下' in data:
            shell.SendKeys("^%{RIGHT}", 0)
        elif '大' in data:
            shell.SendKeys("^%{UP}", 0)#;shell.SendKeys("^%{UP}", 0);shell.SendKeys("^%{UP}", 0)
            winsound.PlaySound("audio/dong.wav", winsound.SND_FILENAME);winsound.PlaySound("audio/dong.wav", winsound.SND_FILENAME)
        elif '小' in data:
            shell.SendKeys("^%{DOWN}", 0)#;shell.SendKeys("^%{DOWN}", 0);shell.SendKeys("^%{DOWN}", 0)
            winsound.PlaySound("audio/dong.wav", winsound.SND_FILENAME);winsound.PlaySound("audio/dong.wav", winsound.SND_FILENAME)
        elif 'mail' in data:
            wb.open('https://www.facebook.com/')
        elif '翻譯' in data or '翻' in data:
            wb.open('https://translate.google.com.tw/?hl=zh-TW')
        elif 'YouTube' in data:
            youtube()
        elif '關掉' in data or '關閉' in data:
            close1()

    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except:
        pass





