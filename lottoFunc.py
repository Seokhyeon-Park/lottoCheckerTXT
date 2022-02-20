import re
import string
from tokenize import String
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

# custom log
def customLog(logName, log):
    if (logFlag):
        print("::::::::::::::::::::")
        print(logName, " : ", log)
