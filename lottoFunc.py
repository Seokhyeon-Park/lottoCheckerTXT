import telegram as tel
import key

# bot 생성
bot = tel.Bot(token=key.token)
logFlag = True

# message 가져오기
def echo(update, cb):
    # 업데이트된 파일과 해당 파일 채팅 유저
    chatId = update.message.chat_id
    userMessage = update.message.text
    # bot.sendMessage(chat_id=chatId, text=text)
    # 예외처리 및 던지기
    splitNum(chatId, userMessage);

# 
def splitNum(chatId, userMessage):
    if (userMessage):
        customLog("USER ID", chatId);
        customLog("userMessage", userMessage);
    else:
        print("userMessage is Null")

# custom log
def customLog(logName, log):
    if (logFlag):
        print("::::::::::::::::::::")
        print(logName, " : ", log);
