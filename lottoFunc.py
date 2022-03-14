#-*- coding: utf-8 -*-

import re
import os
import key
import json
import time
import math
import requests
import threading
import telegram as tel

# bot 생성
bot = tel.Bot(token=key.token)
lottoLine = ["A", "B", "C", "D", "E"]
logFlag = True

# message 가져오기
def echo(update, cb):
    # 업데이트된 파일(메시지)과 해당 파일 채팅 유저
    chatId = update.message.chat_id
    userMessage = update.message.text
    # bot.sendMessage(chat_id=chatId, text=text)
    # lotto 번호 분리
    saveLotto(chatId, userMessage)

# lotto 번호 분리
def saveLotto(chatId, userMessage):
    # 메세지를 수신한 경우
    if(userMessage):
        open("data/"+str(chatId)+".txt", "w").close()
        custLog("USER ID", chatId)
        custLog("userMessage", userMessage)
        # 로또 번호 추출
        for line in userMessage.splitlines():
            for chk in lottoLine:
                if line.find(chk) != -1:
                    userNumber = re.sub('[^0-9]', '', line)
                    # 파일 저장
                    f = open("data/"+str(chatId)+".txt", "a")
                    f.write(userNumber+"\n")
                    f.close()
    else:
        text = "메시지를 다시 확인해주세요."
        bot.sendMessage(chat_id=chatId, text=text)
        custLog("Error", "userMessage is Null")
        custLog("USER ID(Error)", chatId)

# lotto 번호 가져오기
# *loop 필요
def getLottoNumber():
    # [토요일 21시 기준]
    # 1회 : 1039261500
    # 일주일 : 604800
    # time.localtime()
        # 20:45분 기준
        # first = 1039261500
    week = 604800
    first = 1039262400
    date = (time.time() + week - first) / 604800
    # custLog("first", time.localtime(first))
    # custLog("now (full)", time.localtime(time.time()))

    now = math.trunc(date)
    custLog("now", now)

    # 토요일 20시 45분이 되면... -> 9시로 변경
    if now != int(open("itsme.txt", "r").readline()):
        # 갱신
        open("itsme.txt", "w").close()
        f = open("itsme.txt", "a")
        f.write(str(now))
        f.close()

        # 로또번호 조회 url
        url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=" + str(now)

        # 로또번호 요청
        jsonText = requests.post(url).text
        jsonConv = json.loads(jsonText)
        lottoNumber = {'drwtNo' : [], 'bnusNo' : []}

        custLog("jsonConv", jsonConv)

        # 번호만 추출
        for data in jsonConv:
            if(data == 'bnusNo'):
                lottoNumber['bnusNo'].append(jsonConv[data])
            elif data.find('drwtNo') != -1:
                lottoNumber['drwtNo'].append(jsonConv[data])

        # 유저에게 당첨여부 전달
        sendResultToUser(lottoNumber)

    threading.Timer(60, getLottoNumber).start()

# 유저에게 당첨여부 전달
def sendResultToUser(lottoNumber):
    userId = ''
    userData = getUserData()
    custLog("lottoNumber", lottoNumber)
    custLog("UserData", userData)

    # 번호확인
    for data in userData:
        if data.find('.txt') != -1:
            userId = data
        else:
            result = matchLottoNumber(data, lottoNumber)
            bot.sendMessage(chat_id=userId, text=result)
    # 유저 데이터 삭제
    deleteUserData()

def matchLottoNumber(data, lottoNumber):
    count = 0
    bCount = 0
    resultText = ''
    userLottoNum = data
    userNumber = []
    result = ''
    # bResult = ''

    # 유저 로또번호 번호 분리
    for depth in range(1, 7):
        comp = 12 - (depth)
        if(len(userLottoNum) == (comp)):
            custLog("comp", comp)
            # 1. depth 수 만큼 앞자리 한자리 자르기
            for d in range(depth):
                userNumber.append(int(userLottoNum[d:d+1]))
            # 2. 나머지 연산 (두자리 자르기)
            for c in range(int(comp/2)):
                if userLottoNum[depth+(c*2):depth+((c+1)*2)] != '':
                    userNumber.append(int(userLottoNum[depth+(c*2):depth+((c+1)*2)]))
    # 유저 로또 번호
    custLog("userNumber", userNumber)
    for uNum in userNumber:
        chk = 0
        for lNum in lottoNumber['drwtNo']:
            if uNum == lNum:
                result = result + ' [' + str(uNum) + '] '
                count += 1
                chk = 1
            elif uNum == lottoNumber['bnusNo'][0]:
                result = result + ' (' + str(uNum) + ') '
                bCount += 1
                chk = 1
        if chk == 0:
            result = result + ' ' + str(uNum) + ' '

    if count == 3:
        resultText = '5등'
    elif count == 4:
        resultText = '4등'
    elif count == 5 and bCount == 0:
        resultText = '3등'
    elif count == 5 and bCount == 1:
        resultText = '2등'
    elif count == 6:
        resultText = '1등'
    else:
        resultText = '꽝'

    # if bCount == 0:
    #     bResult = 'X'
    # else:
    #     bResult = 'O'

    # result = result + '\n- ' + str(count) + '개 번호 일치\n- 보너스 일치 여부 : ' + bResult + '\n- 결과 : ' + resultText

    result = result + '\n- 당첨 여부 : ' + resultText
    return result


# 유저 계정 정보, 유저 로또 번호 가져오기
def getUserData():
    userData = []
    fileList = os.listdir("./data")
    # 유저 계정, 로또 번호 불러오기
    for fileNm in fileList:
        if fileNm != ".DS_Store":
            custLog("fileNm", fileNm)
            userData.append(fileNm)
            f = open("./data/"+fileNm, 'r')
            while True:
                line = f.readline()
                if not line: break
                # custLog("lottoNum",line[:-1])
                userData.append(line[:-1])
            f.close()
    # 유저 정보 return
    return userData

# 유저 계정 정보, 유저 로또 번호 삭제
def deleteUserData():
    fileList = os.listdir("./data")
    for fileNm in fileList:
        if fileNm != ".DS_Store":
            os.remove("./data/"+fileNm)

# custom log
def custLog(logName, log):
    if (logFlag):
        print("::::::::::::::::::::")
        print(logName, " : ", log)
