import re
import json
import requests
import telegram as tel
import key

# bot 생성
bot = tel.Bot(token=key.token)
lottoLine = ["A", "B", "C", "D", "E"]
logFlag = True

# message 가져오기
def echo(update, cb):
    # 업데이트된 파일과 해당 파일 채팅 유저
    chatId = update.message.chat_id
    userMessage = update.message.text
    # bot.sendMessage(chat_id=chatId, text=text)
    # lotto 번호 분리
    saveLotto(chatId, userMessage)

# lotto 번호 분리
def saveLotto(chatId, userMessage):
    if (userMessage):
        open("data/"+str(chatId)+".txt", "w").close()
        customLog("USER ID", chatId)
        customLog("userMessage", userMessage)
        # 로또 번호 추출
        for line in userMessage.splitlines():
            for chk in lottoLine:
                if line.find(chk) != -1:
                    lottoNumber = re.sub('[^0-9]', '', line)
                    customLog("lottoNumber", lottoNumber)
                    # 파일 저장
                    f = open("data/"+str(chatId)+".txt", "a")
                    f.write(lottoNumber+"\n")
                    f.close()
    else:
        text = "메시지를 다시 확인해주세요."
        bot.sendMessage(chat_id=chatId, text=text)
        customLog("Error", "userMessage is Null")
        customLog("USER ID(Error)", chatId)

# lotto 번호 가져오기
def getLottoNum():
    # 회차
    drwNo = 1003
    # 로또 번호 가져오기
    url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=" + str(drwNo)

    # post : 로또번호
    jsonText = requests.post(url).text
    json = json.loads(jsonText)
    # 로또 번호 저장
    lottoNum = []

    # 숫자만 저장
    for data in json:
        if data.find('No') != -1 and len(str(json[data])) < 3:
            lottoNum.append(json[data])

    # 로또번호
    print(lottoNum)


# custom log
def customLog(logName, log):
    if (logFlag):
        print("::::::::::::::::::::")
        print(logName, " : ", log)
